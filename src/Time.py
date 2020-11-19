class Time():
    def __init__(self, _t: int):
        self.t = _t
    
    def __repr__(self):
        pm = True if self.t >= 12 else False
        timeval = self.t % 12
        
        if timeval == 0:
            timeval += 12
        
        return "{0} {1}".format(timeval, "p.m." if pm else "a.m.")

    def __str__(self):
        return self.__repr__()
