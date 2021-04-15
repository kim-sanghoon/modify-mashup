from random import choice

from logger import get_logger
from ..utils.searchTools import requestModify
from ..utils.responseTools import addBreak, wrapSpeak, googleResponse

log = get_logger('modifyHandler')

def modifyFollowupYesHandler(data):
    modifyContext = [
        c for c in data['queryResult']['outputContexts'] \
            if c['name'].endswith('/confirm')
    ][0]['parameters']
    
    # logging for development purpose
    log.debug('Modify context: {}'.format(modifyContext))

    result = requestModify(
        modifyContext['modifyType'],
        modifyContext['searchContext']['implicatureType'], 
        device=None if modifyContext['searchContext']['device'] == '' \
            else modifyContext['searchContext']['device'],
        skipCount=modifyContext['searchContext']['count'],
        modifyData={
            'trigger-action': modifyContext['trigger-action'],
            'intent': modifyContext['intent'],
            'params': modifyContext['params']
        }
    )

    mainResponse = [
        choice([
            'The rule has been successfully modified',
            'Successfully modified'
        ]),
        'You can tell me other commands to modify, search for other actions affected, or finish this modification'
    ]

    followupContext = {
        'name': '{}/contexts/finish'.format(data['session']),
        'lifespanCount': 2
    }

    return {
        'fulfillmentText': mainResponse[0] + '. ' + mainResponse[1] + '.',
        'outputContexts': [
            followupContext,
            *data['queryResult']['outputContexts']
        ],
        'payload': googleResponse(
            ssml=wrapSpeak(addBreak(mainResponse[0], mainResponse[1])),
            text=mainResponse[0] + '. ' + mainResponse[1] + '.'
        )
    }