from random import randint, choice

class NominalAction():
    actionDict = {}

    def __init__(self, name: str, json_info: dict):
        self.name = name
        self.inverseOf = json_info['inverseOf']
        self.type = json_info['type']
        self.values = json_info['values']
        self.valuesRange = json_info['valuesRange'] if len(self.values) > 0 else {}
        self.language = json_info['language']
        self.device = json_info['device']
        self.mainEffect = []
        self.sideEffect = []

        self.actionDict[name] = self
    
    def __repr__(self):
        return '<{}>'.format(self.name)


class InstantiatedAction():
    def __init__(self, _type: NominalAction, _random: bool, _values=None, _device=None):
        self.type = _type
        self.values = {}

        if not _random:
            assert _values != None
            assert _device != None and _device in _type.device

            self.device = _device
            for k in _type.values:
                self.values[k] = _values[k]

        else:
            self.device = choice(_type.device)
            for k in _type.values:
                minval, maxval = _type.valuesRange[k]
                self.values[k] = randint(minval, maxval)
    
    def __repr__(self):
        return '<{0} with {1} on {2}>'.format(self.type.name, self.values, self.device)
    
    def __hash__(self):
        return hash(repr(self))
    
    def __eq__(self, other):
        return hash(self) == hash(other)
    
    def __ne__(self, other):
        return not(self == other)