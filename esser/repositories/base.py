
class Event(object):
    """
    Event class to represent a consistent interface across
    all repository implementations
    """

    def __init__(self, aggregate_name, aggregate_id, version,
                 event_type, created_at, event_data):
        self.aggregate_name = aggregate_name
        self.aggregate_id = aggregate_id
        self.version = version
        self.event_type = event_type
        self.created_at = created_at
        self.event_data = event_data

    @property
    def aggregate_key(self):
        return '%s:%s' % (self.aggregate_id, self.version)


class BaseRepository(object):

    def __init__(self, aggregate):
        self.aggregate = aggregate

    def to_event(self, obj):
        raise NotImplementedError(
            'Repository interface needs to implement to_event() method'
        )

    def get_events(self, version):
        raise NotImplementedError()

    def get_all_events(self):
        raise NotImplementedError()

    def get_last_event(self):
        raise NotImplementedError()

    def persist(self, aggregate_id, version, event_type, attrs):
        raise NotImplementedError()
