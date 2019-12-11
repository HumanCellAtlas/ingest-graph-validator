class DataStore(object):

    def __init__(self):
        self.name = "empty"
        self.entity_map = {}
        self.backend = None
