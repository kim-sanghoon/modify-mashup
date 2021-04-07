from random import choice

from logger import get_logger
from ..utils.searchTools import requestSearch
from ..utils.responseTools import addBreak, wrapSpeak, googleResponse

log = get_logger('rejectHandler')


def implicaturePinpointRejectHandler(data):
    searchContext = [
        c for c in data['queryResult']['outputContexts'] \
            if c['name'].endswith('/search')
    ][0]['parameters']
    
    # logging for development purpose
    log.debug('Rejection context: {}'.format(searchContext))

    result = requestSearch(
        searchContext['implicatureType'], 
        device=None if searchContext['device'] == "" else searchContext['device'],
        skipCount=searchContext['count'] + 1  # increase the skipCount by 1
    )

    # if nothing found
    if result['historyData'] is None:
        fulfillmentText = [
            "Sorry, but I couldn't find more actions about it.",
            "You can go back to the previous one, or start over by saying the problem again."
        ]
        outputContexts = data['queryResult']['outputContexts']
        for c in outputContexts:
            if c['name'].endswith('/search'):
                c['parameters']['count'] += 1

        return {
            'fulfillmentText': ' '.join(fulfillmentText),
            'outputContexts': outputContexts,
            'payload': googleResponse(
                ssml=wrapSpeak(addBreak(fulfillmentText[0], fulfillmentText[1])),
                text=' '.join(fulfillmentText)
            )
        }

    _, trigger, action, *_ = result['historyData']

    implicatureResponse = {
        "lowairquality": "the air quality's bad",
        "lowbrightness": "it's too dark",
        "lowhumidity": "it's dry",
        "lownoise": "it's too quiet",
        "lowsecurity": "it's not secure",
        "lowtemperature": "it's cold",
        "highairquality": "the air quality's too high",
        "highbrightness": "it's too bright",
        "highhumidity": "it's humid",
        "highnoise": "it's noisy",
        "highsecurity": "it's too secure",
        "hightemperature": "it's hot"
    }

    mainResponse = [
        '{}, {}'.format(
            choice([
                'Before the action',
                'Before that',
                'Another possibility is',
                'Besides',
                'In addition'
            ]),
            action.type.language['past'].format(**action.values)
        ), 
        'and it may also affected you feel that {}.'.format(
            implicatureResponse[searchContext['implicatureType'].lower()]
        )
    ]
    subResponse = [
        'Would you like to check the details about it', 
        'or change it?'
    ]

    # increase the skipCount by 1
    outputContexts = data['queryResult']['outputContexts']
    for c in outputContexts:
        if c['name'].endswith('/search'):
            c['parameters']['count'] += 1

    return {
        'fulfillmentText': ', '.join(mainResponse) + ' ' + ', '.join(subResponse),
        'outputContexts': outputContexts,
        'payload': googleResponse(
            ssml=wrapSpeak(
                addBreak(
                    addBreak(mainResponse[0], mainResponse[1], strength='weak', comma=True), 
                    addBreak(subResponse[0], subResponse[1], strength='weak', comma=True)
                )),
            text=', '.join(mainResponse) + ' ' + ', '.join(subResponse)
        )
    }