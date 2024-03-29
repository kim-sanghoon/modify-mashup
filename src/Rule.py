from .Trigger import *
from .Action import *

import json

class Rule:
    def __init__(self, _trigger: InstantiatedTrigger, _actions: list):
        self.trigger = _trigger
        self.actions = _actions
    
    def __repr__(self):
        return '<{0} - {1}>'.format(self.trigger, self.actions)
    
    def __eq__(self, other):
        return repr(self) == repr(other)
    
    def __ne__(self, other):
        return not(self == repr)
    
    @staticmethod
    def from_json(filename: str):
        with open(filename) as f:
            rawData = json.load(f)
        
        trigger = InstantiatedTrigger(
            _type=NominalTrigger.triggerDict[rawData['trigger']['type']],
            _random=False,
            _params=rawData['trigger']['params'])
        
        actions = []
        
        for rawAction in rawData['actions']:
            actions.append(InstantiatedAction(
                _type=NominalAction.actionDict[rawAction['type']],
                _random=False,
                _values=rawAction['values'],
                _device=rawAction['device']
            ))
        
        return Rule(trigger, actions)
    
    def to_json(self, filename: str):
        retDict = {}

        retDict['trigger'] = {
            'type': self.trigger.type.name,
            'params': self.trigger.params
        }

        retDict['actions'] = [
            {
                'type': action.type.name,
                'values': action.values,
                'device': action.device
            } for action in self.actions
        ]

        with open(filename, 'w') as f:
            json.dump(retDict, f)
    
    def merge(self, other):
        assert self.trigger == other.trigger

        for otherAction in other.actions:
            if otherAction not in self.actions:
                self.actions.append(otherAction)
        