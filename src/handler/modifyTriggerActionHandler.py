from logger import get_logger
from ..utils.encodeTools import decodeObj
from ..utils.searchTools import requestTypeCheck
from ..utils.responseTools import *

log = get_logger('triggerActionHandler')

def modifyTriggerActionHandler(data, paramData=None):
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

    # for param-change intents, we have to modify the param name
    if paramData is not None:
        newValue = None
        if 'final-value' in params and params['final-value'] != '':
            newValue = int(params['final-value'])
        else:
            # there is not an old value, so we use the "middle" of possible values
            oldValue = {
                'temperature': 24,
                'brightness': 45,
                'humidity': 45,
                'volume': 50,
            }[action.split('.')[-1]]
            if 'decrease' in action:
                newValue = oldValue - int(params['change-value'])
            else:
                newValue = oldValue + int(params['change-value'])
        
        params[action.split('.')[-1]] = str(int(newValue))

    # FIRST STEP - check which position to modify -- trigger or action?
    modifyPosition = None
    if 'trigger-action' in params and params['trigger-action'] != '':
        # user's explicit keywords are always the top priority
        modifyPosition = params['trigger-action']
    elif noneParams and noneParams['trigger-action-none'] != '':
        # user's previous spoken keywords
        modifyPosition = noneParams['trigger-action-none']
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
    devicesKeyword = None
    if 'devices' in params and params['devices'] != '':
        devicesKeyword = params['devices']
    elif 'network-devices' in params and params['network-devices'] != '':
        devicesKeyword = params['network-devices']
    
    # cornor-case handling for modify.set.volume
    if action == 'modify.set.volume':
        if params['final-value'] > 50:
            action = 'modify.increase.volume'
        else:
            action = 'modify.decrease.volume'
    
    typeResult = requestTypeCheck(
        '{}#{}'.format(action, devicesKeyword) if devicesKeyword \
            else action,
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
    
    print(params)
    intentLanguage = intentLanguage.format(**formatDict)

    # the process itself is identical to that of modifyTriggerOnlyHandler
    if 'add-change' in params and params['add-change'] != '':
        # if user explicitly uttered either to replace or to append,
        # follow the utterance.
        modifyType = params['add-change']
    elif noneParams and noneParams['add-change-none'] != '':
        # user's previous spoken keywords
        modifyType = noneParams['add-change-none']
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
