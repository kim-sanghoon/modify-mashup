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
    

def addBreak(s1, s2, breakTime='1000ms'):
    """Add a pause between two responses.

    Args:
        s1 (str): The first string.
        s2 (str): The second string.
        breakTime (str, optional): Length of the pause between the strings. Defaults to '1000ms'.

    Returns:
        str: Merged string with break time.
    """
    if s1.endswith('.'):
        s1 = s1[:-1]

    return s1 + ' <break time="{}">. '.format(breakTime) + s2
