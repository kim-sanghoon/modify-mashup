from ..Implicature import implicature

def expressionHandler(data):
    query = str(data['queryResult']['queryText'])
    predict = implicature(query)

    implicatureResponse = {
        'LowAirQuality': 'the air quality is bad',
        'LowBrightness': 'the room is too dark',
        'LowHumidity': 'the air is too dry',
        'LowNoise': 'the room is too quiet',
        'LowSecurity': 'the room is not secure',
        'LowTemperature': 'the room is cold',
        'HighAirQuality': 'the air quality is too high',
        'HighBrightness': 'the room is too bright',
        'HighHumidity': 'the air is humid',
        'HighNoise': 'the room is noisy',
        'HighSecurity': 'the room is too secure',
        'HighTemperature': 'the room is hot'
    }

    ret = {'fulfillmentText': "Sorry to hear that {}.".format(implicatureResponse[predict])}

    return ret