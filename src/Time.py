class Time(dict):
    def __init__(self, _t):
        # Unmarshalling JSON-ified Time object
        if isinstance(_t, dict):
            _t = _t['t']

        dict.__init__(self, t=_t)
        self.t = _t
    
    def __repr__(self):
        pm = True if self.t >= 12 else False
        timeval = self.t % 12
        
        if timeval == 0:
            timeval += 12
        
        return "{0} {1}".format(timeval, "p.m." if pm else "a.m.")

    def __str__(self):
        return self.__repr__()
