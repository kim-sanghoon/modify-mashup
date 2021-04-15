from logger import get_logger
from ..utils.encodeTools import decodeObj
from ..utils.searchTools import requestTypeCheck
from ..utils.responseTools import *
from ..utils.datetimeParser import *

log = get_logger('triggerOnlyHandler')

def modifyTriggerOnlyHandler(data):
    action = data['queryResult']['action']
    params, searchContext = None, None

    for c in data['queryResult']['outputContexts']:
        if c['name'].endswith('/search'):
            searchContext = c['parameters']
        elif c['name'].endswith('/modify-params'):
            params = c['parameters']

    # logging for development purpose
    log.debug('Requested action: {}'.format(action))
    log.debug('Given params: {}'.format(params))

    modifyType = None
    typeResult = requestTypeCheck(
        action,
        searchContext['implicatureType'],
        device=None if searchContext['device'] == '' else searchContext['device'],
        skipCount=searchContext['count']
    )
    try:
        intentTriggerObject = decodeObj(typeResult['intentData'])[0]
    except Exception as e:
        log.error(e)
        return genericErrorResponse(data, whileWhat='while trying to recognize your command')
    triggerLanguage = 'when ' + intentTriggerObject.language['present']

    # we need a special handling for modify.date and modify.time
    if action == 'modify.date':
        params.update(parseDate(params['date']))
    if action == 'modify.time':
        params.update({'time': parseTime(params['time'])})

    formatDict = {}
    for k, v in params.items():
        if k in intentTriggerObject.params:
            formatDict[k] = v
    
    triggerLanguage = triggerLanguage.format(**formatDict)

    if 'add-change' in params and params['add-change'] != '':
        # if user explicitly uttered either to replace or to append,
        # follow the utterance.
        modifyType = params['add-change']
    else:
        if typeResult['trigger']:
            # if same type, assume that user input is to replace
            modifyType = 'replace'
        else:
            # otherwise, ask the user
            fulfillmentText = [
                'Do you want to replace the original trigger',
                'or append it to the original one?'
            ]
            followupContext = {
                'name': '{}/contexts/add-change-followup'.format(data['session']),
                'lifespanCount': 2,
                'parameters': {
                    'isTriggerOnly': True,
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

    # retrieve final confirmation
    fulfillmentText = [
        'Replacing the original trigger to {}' if modifyType == 'replace' \
            else 'Appending {} to the original trigger',
        'is that right?'
    ]
    fulfillmentText[0] = fulfillmentText[0].format(triggerLanguage)
    followupContext = {
        'name': '{}/contexts/confirm'.format(data['session']),
        'lifespanCount': 1,
        'parameters': {
            'modifyType': modifyType,
            'trigger-action': 'trigger',
            'intent': action,
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