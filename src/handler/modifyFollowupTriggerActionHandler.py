from .modifyTriggerActionHandler import *
from .modifyParameterChangeHandler import modifyParameterChangeHandler

def modifyFollowupTriggerActionHandler(data):
    originalIntentContext = [
        c for c in data['queryResult']['outputContexts'] \
            if c['name'].endswith('/trigger-action-followup')
    ][0]['parameters']

    data['queryResult']['action'] = originalIntentContext['intent']

    if 'isParamChange' in originalIntentContext and originalIntentContext['isParamChange']:
        return modifyParameterChangeHandler(data)
    return modifyTriggerActionHandler(data)
