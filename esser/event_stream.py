

class EventStream(object):

    def __init__(self):
        self.changes = []
        self.event_appliers = {}
        self.register_appliers()

    def register_appliers(self):
        raise NotImplementedError(
            'register_appliers() not implemeted'
        )

    def register_applier(self, applier):
        self.event_appliers[]