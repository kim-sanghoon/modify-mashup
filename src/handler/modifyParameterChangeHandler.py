import json
from logger import get_logger
from ..utils.encodeTools import decodeObj
from ..utils.searchTools import requestParam
from ..utils.responseTools import *
from .modifyTriggerActionHandler import *

log = get_logger('parameterChangeHandler')

def _askTriggerAction(data):
    fulfillmentText = [
        'Do you want to modify the trigger section',
        'or the action section?'
    ]
    followupContext = {
        'name': '{}/contexts/trigger-action-followup'.format(data['session']),
        'lifespanCount': 2,
        'parameters': {
            'intent': data['queryResult']['action'],
            'isParamChange': True
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

def modifyParameterChangeHandler(data):
    action = data['queryResult']['action']
    params, searchContext = None, None

    for c in data['queryResult']['outputContexts']:
        if c['name'].endswith('/search'):
            searchContext = c['parameters']
        elif c['name'].endswith('/modify-params'):
            params = c['parameters']

    userEnvType = action.split('.')[-1]
    userEnvType = userEnvType if userEnvType in ['brightness', 'humidity', 'temperature', 'volume'] else None

    searchResult = requestParam(
        searchContext['implicatureType'],
        device=None if searchContext['device'] == "" else searchContext['device'],
        skipCount=searchContext['count']
    )
    
    whereToEdit = None

    if userEnvType == None:
        if searchResult['trigger']['hasParameter']:
            if searchResult['action']['hasParameter']:
                if 'trigger-action' in params:
                    whereToEdit = params['trigger-action']
                    userEnvType = searchResult[whereToEdit]['parameterEnv']
                else:    
                    # ask the user to select trigger part or action part
                    return _askTriggerAction(data)
            
            whereToEdit = 'trigger'
            userEnvType = searchResult['trigger']['parameterEnv']
        else:
            if searchResult['action']['hasParameter']:
                whereToEdit = 'action'
                userEnvType = searchResult['action']['parameterEnv']
            else:
                # ask the user to clarify which type of parameter
                fulfillmentText = [
                    "Sorry, but I couldn't understand the type of parameter you said",
                    'Could you say that again with exact parameter type?'
                ]

                return {
                    'fulfillmentText': ', '.join(fulfillmentText),
                    'payload': googleResponse(
                        ssml=wrapSpeak(addBreak(fulfillmentText[0], fulfillmentText[1], comma=True)),
                        text=', '.join(fulfillmentText)
                    )
                }
    else:
        if searchResult['trigger']['hasParameter'] and \
            userEnvType == searchResult['trigger']['parameterEnv']:
            if searchResult['action']['hasParameter'] and \
                userEnvType == searchResult['action']['parameterEnv']:
                if 'trigger-action' in params:
                    whereToEdit = params['trigger-action']
                    userEnvType = searchResult[whereToEdit]['parameterEnv']
                else:    
                    # ask the user to select trigger part or action part
                    return _askTriggerAction(data)
            
            whereToEdit = 'trigger'
        else:
            if searchResult['action']['hasParameter'] and \
                userEnvType == searchResult['action']['parameterEnv']:
                whereToEdit = 'action'
    
    # logging for development purpose
    log.debug('Requested action: {}'.format(action))
    log.debug('Given params: {}'.format(params))
    log.debug('Resolved whereToEdit: {}'.format(whereToEdit))

    if whereToEdit == None:
        return modifyTriggerActionHandler(data, paramData=searchResult)
    
    oldValue = searchResult[whereToEdit]['parameterValue'][
        searchResult[whereToEdit]['parameterEnv']
    ]
    newValue = None
    if 'final-value' in params and params['final-value'] != '':
        newValue = int(params['final-value'])
    else:
        if 'decrease' in action:
            newValue = oldValue - int(params['change-value'])
        else:
            newValue = oldValue + int(params['change-value'])
    
    # retrieve final confirmation
    fulfillmentText = [
        'Replacing the {whereToEdit} {userEnvType} value from {oldValue} to {newValue}',
        'is that right?'
    ]
    fulfillmentText[0] = fulfillmentText[0].format(
        whereToEdit=whereToEdit,
        userEnvType=userEnvType,
        oldValue=oldValue,
        newValue=newValue
    )
    followupContext = {
        'name': '{}/contexts/confirm'.format(data['session']),
        'lifespanCount': 1,
        'parameters': {
            'modifyType': 'replace',
            'trigger-action': whereToEdit,
            'intent': action,
            'searchContext': searchContext,
            'params': params,
            'param-change': {
                'whereToEdit': whereToEdit,
                'userEnvType': userEnvType,
                'oldValue': oldValue,
                'newValue': newValue
            }
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