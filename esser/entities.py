import uuid

from esser.events import BaseEvent
from esser.constants import AGGREGATE_KEY_DELIMITER
from esser.repositories.base import DynamoDBRepository
from esser.utils import cached_property


class Entity(object):
    """
    Class representing an Aggregate in Event Sourcing
    """

    INITIAL_VERSION = 1

    repository_class = DynamoDBRepository

    def __init__(self, aggregate_id=None):
        """
        If aggregate_id is None, only Created events can be fired
        """
        self.aggregate_id = aggregate_id
        for name, value in self.__class__.__dict__.items():
            if isinstance(value, BaseEvent):
                value.attach_entity(self)
        self.repository = DynamoDBRepository(aggregate=self)

    @property
    def aggregate_name(self):
        """
        Override this to decide how this Aggregate is named
        """
        return self.__class__.__name__

    def generate_new_guid(self):
        """
        Override this to decide how new GUID is generated
        """
        return str(uuid.uuid4())

    def get_last_snapshot(self):
        return {}

    def get_initial_state(self):
        return {}

    def get_state_at(self, version):
        sequence = self.repository.get_events(version)
        initial_state = self.get_last_snapshot() or self.get_initial_state()
        return reduce(self.reducer.reduce, sequence, initial_state)

    def get_current_state(self):
        sequence = self.repository.get_all_events()
        initial_state = self.get_last_snapshot() or self.get_initial_state()
        return reduce(self.reducer.reduce, sequence, initial_state)

    current_state = property(get_current_state)
    cached_current_state = cached_property(get_current_state)

    def get_last_aggregate_version(self):
        last_event = self.repository.get_last_event()
        return last_event.version
