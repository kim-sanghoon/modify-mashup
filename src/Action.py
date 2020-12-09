from random import randint

class NominalAction():
    actionDict = {}

    def __init__(self, name: str, json_info: dict):
        self.name = name
        self.inverseOf = json_info['inverseOf']
        self.type = json_info['type']
        self.values = json_info['values']
        self.valuesRange = json_info['valuesRange'] if len(self.values) > 0 else {}
        self.language = json_info['language']
        self.mainEffect = []
        self.sideEffect = []

        self.actionDict[name] = self
    
    def __repr__(self):
        return '<{}>'.format(self.name)


class InstantiatedAction():
    def __init__(self, _type: NominalAction, _random: bool, _values=None):
        self.type = _type
        self.values = {}

        if not _random:
            assert _values != None

            for k in _type.values:
                self.values[k] = _values[k]

        else:
            for k in _type.values:
                minval, maxval = _type.valuesRange[k]
                self.values[k] = randint(minval, maxval)
    
    def __repr__(self):
        return '<{0} with {1}>'.format(self.type.name, self.values)