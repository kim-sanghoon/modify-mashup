from .modifyTriggerOnlyHandler import modifyTriggerOnlyHandler

def modifyFollowupAddChangeHandler(data):
    originalIntentContext = [
        c for c in data['queryResult']['outputContexts'] \
            if c['name'].endswith('/add-change-followup')
    ][0]['parameters']

    data['queryResult']['action'] = originalIntentContext['intent']

    if originalIntentContext['isTriggerOnly']:
        return modifyTriggerOnlyHandler(data)
    else:
        raise NotImplementedError # TODO