from logger import get_logger
from ..utils.encodeTools import decodeObj
from ..utils.searchTools import requestTypeCheck
from ..utils.responseTools import *

log = get_logger('triggerActionHandler')

def modifyTriggerActionHandler(data):
    action = data['queryResult']['action']
    params, searchContext, isDetail, noneParams = None, None, False, None

    for c in data['queryResult']['outputContexts']:
        if c['name'].endswith('/search'):
            searchContext = c['parameters']
        elif c['name'].endswith('/modify-params'):
            params = c['parameters']
        elif c['name'].endswith('/detail'):
            isDetail = True
        elif c['name'].endswith('/none-params'):
            noneParams = c['parameters']

    # logging for development purpose
    log.debug('Requested action: {}'.format(action))
    log.debug('Given params: {}'.format(params))

    # FIRST STEP - check which position to modify -- trigger or action?
    modifyPosition = None
    if 'trigger-action' in params and params['trigger-action'] != '':
        # user's explicit keywords are always the top priority
        modifyPosition = params['trigger-action']
    elif noneParams and noneParams['trigger-action-none'] != '':
        # user's previous spoken keywords
        modifyPosition = noneParams['trigger-action']
    else:
        if not isDetail:
            # if user did not listen to the trigger detail
            modifyPosition = 'action'
        else:
            # otherwise, ask the user
            fulfillmentText = [
                'Do you want to modify the trigger section',
                'or the action section?'
            ]
            followupContext = {
                'name': '{}/contexts/trigger-action-followup'.format(data['session']),
                'lifespanCount': 2,
                'parameters': {
                    'intent': action
                }
            }

            return {
                'fulfillmentText': ', '.join(fulfillmentText),
                'outputContexts': [
                    followupContext, 
                    *data['queryResult']['outputContexts']
                ],
                'payload': googleResponse(
                    ssml=wrapSpeak(addBreak(fulfillmentText[0], fulfillmentText[1], comma=True)),
                    text=', '.join(fulfillmentText)
                )
            }
    
    log.debug('User modify position: {}'.format(modifyPosition))

    # SECOND STEP - check replace or append
    modifyType = None
    devicesKeyword = params['devices'] \
        if 'devices' in params and params['devices'] != '' \
        else params['network-devices']
    typeResult = requestTypeCheck(
        '{}#{}'.format(action, devicesKeyword),
        searchContext['implicatureType'],
        device=None if searchContext['device'] == '' else searchContext['device'],
        skipCount=searchContext['count']
    )
    try:
        intentObjects = decodeObj(typeResult['intentData'])
    except Exception as e:
        log.error(e)
        return genericErrorResponse(data, whileWhat='while trying to recognize your command')

    intentObject = intentObjects[0]
    if len(intentObjects) > 1 and intentObjects[1].name.endswith(modifyPosition.capitalize()):
        intentObject = intentObjects[1]
    intentLanguage = 'when ' + intentObject.language['present'] \
        if modifyPosition == 'trigger' else intentObject.language['gerund']

    formatDict = {}
    for k, v in params.items():
        if modifyPosition == 'trigger' and k in intentObject.params:
            formatDict[k] = v
        if modifyPosition == 'action' and k in intentObject.values:
            formatDict[k] = v
    
    intentLanguage = intentLanguage.format(**formatDict)

    # the process itself is identical to that of modifyTriggerOnlyHandler
    if 'add-change' in params and params['add-change'] != '':
        # if user explicitly uttered either to replace or to append,
        # follow the utterance.
        modifyType = params['add-change']
    else:
        if typeResult[modifyPosition]:
            # if same type, assume that user input is to replace
            modifyType = 'replace'
        else:
            # otherwise, ask the user
            fulfillmentText = [
                'Do you want to replace the original {}'.format(modifyPosition),
                'or append it to the original one?'
            ]
            followupContext = {
                'name': '{}/contexts/add-change-followup'.format(data['session']),
                'lifespanCount': 2,
                'parameters': {
                    'isTriggerOnly': False,
                    'intent': action
                }
            }

            return {
                'fulfillmentText': ', '.join(fulfillmentText),
                'outputContexts': [
                    followupContext, 
                    *data['queryResult']['outputContexts']
                ],
                'payload': googleResponse(
                    ssml=wrapSpeak(addBreak(fulfillmentText[0], fulfillmentText[1], comma=True)),
                    text=', '.join(fulfillmentText)
                )
            }
    
    log.debug('User modify type: {}'.format(modifyType))

    # retrieve final confirmation
    fulfillmentText = [
        'Replacing the original {modifyPosition} to {intentLanguage}' if modifyType == 'replace' \
            else 'Appending {intentLanguage} to the original {modifyPosition}',
        'is that right?'
    ]
    fulfillmentText[0] = fulfillmentText[0].format(
        modifyPosition=modifyPosition,
        intentLanguage=intentLanguage
    )
    followupContext = {
        'name': '{}/contexts/confirm'.format(data['session']),
        'lifespanCount': 1,
        'parameters': {
            'modifyType': modifyType,
            'trigger-action': modifyPosition,
            'intent': '{}#{}'.format(action, devicesKeyword),
            'searchContext': searchContext,
            'params': params
        }
    }

    return {
        'fulfillmentText': ', '.join(fulfillmentText),
        'outputContexts': [
            followupContext,
            *data['queryResult']['outputContexts']
        ],
        'payload': googleResponse(
            ssml=wrapSpeak(addBreak(fulfillmentText[0], fulfillmentText[1], comma=True)),
            text=', '.join(fulfillmentText)
        )
    }


    return {}
