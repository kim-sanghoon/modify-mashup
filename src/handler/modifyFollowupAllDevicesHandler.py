from .modifyDevicesParameterHandler import *

def modifyFollowupAllDevicesHandler(data):
    originalIntentContext = [
        c for c in data['queryResult']['outputContexts'] \
            if c['name'].endswith('/all-devices-followup')
    ][0]['parameters']

    data['queryResult']['action'] = originalIntentContext['intent']

    return modifyDevicesParameterHandler(data, fromFollowup=True)
