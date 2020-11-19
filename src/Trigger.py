from random import choice, randint

from .Time import Time

class NominalTrigger():
    triggerDict = {}

    def __init__(self, name: str, json_info: dict):
        self.name = name
        self.params = json_info['params']
        self.paramsRange = json_info['paramsRange']
        self.language = json_info['language']

        self.triggerDict[name] = self

    def __repr__(self):
        return '<{}>'.format(self.name)


class InstantiatedTrigger():
    def __init__(self, _type: NominalTrigger, _params: dict):
        self.type = _type
        self.params = {}
        for k in _type.params:
            self.params[k] = _params[k]
    
    def __init__(self, _type: NominalTrigger, _random: bool):
        if not _random:
            raise RuntimeError("You cannot instantiate actions without random flag!")
        
        self.type = _type
        self.params = {}
        for k in _type.params:
            paramType = _type.params[k]['type']
            paramRange = _type.paramsRange[k]

            pTypeHandler = {
                "string": lambda pRange: choice(pRange),
                "number": lambda pRange: randint(pRange[0], pRange[1]),
                "time": lambda pRange: Time(randint(pRange[0], pRange[1]))
            }

            self.params[k] = pTypeHandler[paramType](paramRange)
    
    def __repr__(self):
        return '<{0} with {1}>'.format(self.type.name, self.params)

