import requests

from random import choice

from logger import get_logger
from ..utils.responseTools import addBreak, wrapSpeak, googleResponse

def modifyUndoYesHandler(data):
    response = requests.post('http://localhost:445/undo')
    response = response.json()

    if response['status'] == 'error':
        log = get_logger('undoHandler')
        log.error('Mashup module returned error - ' + response['what'])
        raise RuntimeError(response['what'])

    mainResponse = [
        choice([
            'Your last modification has been undone',
            'Successfully undone',
            'The last modification has been undone'
        ]),
        'You can make further modification by telling me, or finish it'
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
