from logger import get_logger
from ..utils.responseTools import googleResponse, wrapSpeak
from .modifyTriggerActionHandler import *

log = get_logger('devicesParameterHandler')

def modifyDevicesParameterHandler(data, fromFollowup=False):
    action = data['queryResult']['action']
    params = [
        c for c in data['queryResult']['outputContexts'] \
            if c['name'].endswith('/modify-params')
    ][0]['parameters']

    if 'devices' in params and params['devices'] != '':
        return modifyTriggerActionHandler(data)
    
    if 'network-devices' in params and params['network-devices'] != '':
        return modifyTriggerActionHandler(data)
    
    # if both 'devices' and 'network-devices' not present, ask the user.
    log.debug('Requested action: {}'.format(action))
    log.debug('Given params: {}'.format(params))
    log.debug('Params does not exist, crafting follow-up context...')
    
    actionLanguage = {
        'enable': 'turn on',
        'disable': 'turn off',
        'close-lock': 'close or lock',
        'open-unlock': 'open or unlock',
    }
    fulfillmentText = 'Which device do you want to {}?'.format(
        actionLanguage[action.split('.')[-1]]
    )
    followupContext = {
        'name': '{}/contexts/all-devices-followup'.format(data['session']),
        'lifespanCount': 2,
        'parameters': {
            'intent': action
        }
    }

    if fromFollowup:
        fulfillmentText = "Sorry, but I couldn't hear the device you said."

    return {
        'fulfillmentText': fulfillmentText,
        'outputContexts': [
            followupContext, 
            *data['queryResult']['outputContexts']
        ],
        'payload': googleResponse(
            ssml=wrapSpeak(fulfillmentText),
            text=fulfillmentText
        )
    }