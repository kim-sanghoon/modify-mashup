action_dict = {}

class NominalAction():
    def __init__(self, name: str, json_info: dict):
        self.name = name
        self.inverseOf = json_info['inverseOf']
        self.type = json_info['type']
        self.values = json_info['values']
        self.language = json_info['language']
        self.mainEffect = []
        self.sideEffect = []

        action_dict[name] = self
    
    def __repr__(self):
        return '<{}>'.format(self.name)


class InstantiatedAction():
    def __init__(self, _type: NominalAction, _values: dict):
        self.type = _type
        self.values = {}
        for k in _type.values:
            self.values[k] = _values[k]
    