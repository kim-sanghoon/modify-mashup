def wrapSpeak(s):
    """Wrap the sentence with a `<speak>{s}</speak>` format.

    Args:
        s (`str`): A sentence to be wrapped.

    Returns:
        `str`: Wrapped sentence.
    """
    if not s.startswith('<speak>'):
        s = '<speak>' + s

    if not s.endswith('</speak>'):
        s += '</speak>'
    
    return s


def unwrapSpeak(s):
    """Unwrap the sentence with a `<speak>{s}</speak>` format.

    Args:
        s (`str`): A sentence to be unwrapped.

    Returns:
        `str`: Unwrapped sentence.
    """
    if s.startswith('<speak>'):
        s = s[7:]
    
    if s.endswith('</speak>'):
        s = s[:-8]
    
    return s
    

def addBreak(s1, s2, breakTime='700ms', strength=None, comma=False):
    """Add a pause between two responses.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.
        breakTime (str, optional): Length of the pause between the strings. Defaults to '1000ms'.
        strength (str, optional): The strength of a break: 'weak', 'medium', 'strong'. Defaults to None.
        comma (bool, optional): Using comma between two sentences if true. Defaults to False.

    Returns:
        str: Merged string with break time.
    """
    if s1.endswith('.'):
        s1 = s1[:-1]
    
    breakToken = '<break time="{}" />'.format(breakTime)
    if strength is not None:
        breakToken = '<break strength="{}" />'.format(strength)

    return s1 + '{}{} '.format(breakToken, ',' if comma else '.') + s2


def googleResponse(ssml, text):
    """Generate (dirty) google payload of a webhook response.

    Args:
        ssml (str): A SSML string.
        text (str): Plain text string.

    Returns:
        dict: Generated google payload.
    """
    return {
        'google': {
            'expectUserResponse': True,
            'richResponse': {
                'items': [
                    {
                        'simpleResponse': {
                            'ssml': ssml,
                            'text': text
                        }
                    }
                ]
            }
        }
    }


def genericErrorResponse(data, whileWhat=None):
    fulfillmentText = [
        'Sorry, I found a serious technical trouble {}'.format(
            'while processing your command' if not whileWhat else whileWhat
        ),
        'Could you command again?'
    ]
    outputContexts = []
    for c in data['queryResult']['outputContexts']:
        c['lifespanCount'] += 1
        outputContexts.append(c)
    
    return {
        'fulfillmentText': '. '.join(fulfillmentText),
        'outputContexts': outputContexts,
        'payload': googleResponse(
            ssml=wrapSpeak(addBreak(fulfillmentText[0], fulfillmentText[1])),
            text='. '.join(fulfillmentText)
        )
    }