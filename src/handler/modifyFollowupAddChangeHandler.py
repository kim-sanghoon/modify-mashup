from .modifyTriggerOnlyHandler import modifyTriggerOnlyHandler
from .modifyTriggerActionHandler import modifyTriggerActionHandler

def modifyFollowupAddChangeHandler(data):
    originalIntentContext = [
        c for c in data['queryResult']['outputContexts'] \
            if c['name'].endswith('/add-change-followup')
    ][0]['parameters']

    data['queryResult']['action'] = originalIntentContext['intent']

    if originalIntentContext['isTriggerOnly']:
        return modifyTriggerOnlyHandler(data)
    else:
        return modifyTriggerActionHandler(data)