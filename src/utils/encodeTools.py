import pickle, base64

def encodeObj(obj):
    """
    function encodeObj(obj)

    @param obj: any object to be encoded
    @return a string in base64 format, which contains the pickled object
    """
    pickledObject = pickle.dumps(obj)
    return base64.urlsafe_b64encode(pickledObject).decode('utf-8')


def decodeObj(b64str):
    """
    function decodeObj(b64str)

    @param b64str: a string in base64 format, which contains the pickled object
    @return the unpickled object
    """
    decodedPickle = base64.urlsafe_b64decode(b64str)
    return pickle.loads(decodedPickle)