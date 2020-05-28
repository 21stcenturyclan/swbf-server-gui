class SWBFConfig:
    def __init__(self, filename):
        self._filename = filename
        self._properties = {}

    def __getitem__(self, item):
        if item in self._properties:
            return self._properties
        return None

    def __setitem__(self, key, value):
        self._properties[key] = value
