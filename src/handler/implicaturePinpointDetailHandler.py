from ..utils.searchTools import requestSearch
from ..utils.responseTools import addBreak, wrapSpeak, googleResponse


def implicaturePinpointDetailHandler(data):
    searchContext = [
        c for c in data['queryResult']['outputContexts'] \
            if c['name'].endswith('/search')
    ][0]['parameters']

    result = requestSearch(
        searchContext['implicatureType'], 
        device=None if searchContext['device'] == "" else searchContext['device'],
        skipCount=searchContext['count']
    )
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

    ruleDescription = '{0} because {1}'.format(
        action.type.language['past'].format(**action.values).capitalize(),
        trigger.type.language['past'].format(**trigger.params)
    )
    infoDescription = ['and it may cause you feel that {}.'.format(
        implicatureResponse[searchContext['implicatureType'].lower()]
    ), 'Would you like to modify the action', 'or search for another action?']

    return {
        'fulfillmentText': ruleDescription + ', ' + ' '.join(infoDescription),
        'payload': googleResponse(
            ssml=wrapSpeak(
                addBreak(
                    addBreak(ruleDescription, infoDescription[0], comma=True), 
                    addBreak(infoDescription[1], infoDescription[2], strength='weak', comma=True)
                )),
            text=ruleDescription + ', ' + ' '.join(infoDescription),
        )
    }
    
    
