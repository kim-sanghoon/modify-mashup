from .modifyTriggerActionHandler import *

def modifyFollowupTriggerActionHandler(data):
    originalIntentContext = [
        c for c in data['queryResult']['outputContexts'] \
            if c['name'].endswith('/trigger-action-followup')
    ][0]['parameters']

    data['queryResult']['action'] = originalIntentContext['intent']

    return modifyTriggerActionHandler(data)
