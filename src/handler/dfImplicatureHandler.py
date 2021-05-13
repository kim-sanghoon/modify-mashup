def dfImplicatureHandler(data):
    # A raw action string is composed of three words such as
    # 'implicature.noise.low' or 'implicature.temperature.high'
    actionString = data['queryResult']['action'].split('.')

    implicatureType = actionString[2] + actionString[1]
    implicatureResponse = {
        'lowairquality': 'the air quality is bad',
        'lowbrightness': 'the room is too dark',
        'lowhumidity': 'the air is too dry',
        'lownoise': 'the room is too quiet',
        'lowsecurity': 'the room is not secure',
        'lowtemperature': 'the room is cold',
        'highairquality': 'the air quality is too high',
        'highbrightness': 'the room is too bright',
        'highhumidity': 'the air is humid',
        'highnoise': 'the room is noisy',
        'highsecurity': 'the room is too secure',
        'hightemperature': 'the room is hot'
    }

    # Craft the agent response
    fulfillmentText = "Sorry to hear that {}.".format(implicatureResponse[implicatureType])
    fulfillmentText += " Could you allow me to find out why?"

    # Capitalize the implicature with the exception of "AirQuality"
    if actionString[1] == 'airquality':
        actionString[1] = 'AirQuality'
    else:
        actionString[1] = actionString[1].capitalize()

    # Set the follow-up context
    followupContext = {
        'name': '{}/contexts/implicature-followup'.format(data['session']),
        'lifespanCount': 1,
        'parameters': {
            'implicatureType': actionString[2].capitalize() +
                               actionString[1]
        }
    }

    return {
        'fulfillmentText': fulfillmentText,
        'outputContexts': [followupContext]
    }
