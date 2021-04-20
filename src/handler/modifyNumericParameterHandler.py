from logger import get_logger
from ..utils.responseTools import googleResponse, wrapSpeak
from .modifyParameterChangeHandler import *

log = get_logger('modifyParameterHandler')

def modifyNumericParameterHandler(data):
    action = data['queryResult']['action']
    params = [
        c for c in data['queryResult']['outputContexts'] \
            if c['name'].endswith('/modify-params')
    ][0]['parameters']

    if 'final-value' in params and params['final-value'] != '':
        return modifyParameterChangeHandler(data)
    
    if 'change-value' in params and params['change-value'] != '':
        return modifyParameterChangeHandler(data)
    
    # if both 'devices' and 'network-devices' not present, ask the user.
    log.debug('Requested action: {}'.format(action))
    log.debug('Given params: {}'.format(params))
    log.debug('Params does not exist, crafting follow-up context...')
    
    paramTypes = ['brightness', 'humidity', 'temperature', 'volume']
    paramType = action.split('.')[-1]
    fulfillmentText = 'Sorry, could you say that again with exact {} value?'.format(
        paramType if paramType in paramTypes else 'parameter'
    )
    outputContexts = data['queryResult']['outputContexts']
    for c in outputContexts:
        try:
            c['lifespanCount'] += 1
        except:
            pass
    
    return {
        'fulfillmentText': fulfillmentText,
        'outputContexts': outputContexts,
        'payload': googleResponse(
            ssml=wrapSpeak(fulfillmentText),
            text=fulfillmentText
        )
    }