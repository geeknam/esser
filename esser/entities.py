from esser.events import BaseEvent
from esser.exceptions import AggregateDoesNotExist
from esser.constants import AGGREGATE_KEY_DELIMITER
from esser.models import Event, Snapshot


class Entity(object):

    INITIAL_VERSION = 1

    def __init__(self, aggregate_id=None):
        self.aggregate_id = aggregate_id
        for name, value in self.__class__.__dict__.items():
            if isinstance(value, BaseEvent):
                value.attach_entity(self)

    @property
    def aggregate_name(self):
        return self.__class__.__name__

    def get_last_snapshot(self):
        return {}

    def get_initial_state(self):
        return {}

    def get_events(self, version):
        """
        Get all events up to specific version
        """
        return Event.query(
            self.aggregate_name,
            aggregate_id__le='%s:%s' % (
                self.aggregate_id, version
            )
        )

    def get_all_events(self):
        """
        Get all events up to latest version
        """
        return Event.query(
            self.aggregate_name,
            aggregate_id__begins_with=self.aggregate_id
        )

    def get_last_event(self):
        events = list(Event.query(
            self.aggregate_name,
            aggregate_id__begins_with=self.aggregate_id,
            limit=1, scan_index_forward=False
        ))
        try:
            return events[0]
        except IndexError:
            raise AggregateDoesNotExist()

    def get_state_at(self, version):
        sequence = self.get_events(version)
        initial_state = self.get_last_snapshot() or self.get_initial_state()
        return reduce(self.reducer.reduce, sequence, initial_state)

    @property
    def current_state(self):
        sequence = self.get_all_events()
        initial_state = self.get_last_snapshot() or self.get_initial_state()
        return reduce(self.reducer.reduce, sequence, initial_state)

    def get_last_aggregate_version(self):
        last_event = self.get_last_event()
        return int(
            last_event.aggregate_id.split(AGGREGATE_KEY_DELIMITER)[1]
        )
