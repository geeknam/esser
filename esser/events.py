from esser.validators import EsserValidator
from esser.constants import AGGREGATE_KEY_DELIMITER
from esser.exceptions import EventValidationException


class BaseEvent(object):
    """Base Event class."""

    def __init__(self):
        """
        Initialise the validator for the event based on schema.

        A valid Event class should have Event.schema
        """
        self.validator = EsserValidator(
            self.schema, event=self
        )

    @property
    def event_name(self):
        """Event name by default is the class name."""
        return self.__class__.__name__

    def get_aggregate_key(self):
        """Increment version of the event for the aggregate."""
        version = self.entity.get_last_aggregate_version() + 1
        return '{aggregate_id}{delimiter}{version}'.format(
            aggregate_id=self.entity.aggregate_id,
            delimiter=AGGREGATE_KEY_DELIMITER,
            version=version
        )

    def attach_entity(self, entity):
        """Allow entity to be attached to the event."""
        setattr(self, 'entity', entity)
        setattr(self.validator, 'aggregate', entity)

    def persist(self, attrs):
        return self.entity.repository.persist(
            aggregate_id=self.get_aggregate_key(),
            event_type=self.event_name,
            attrs=attrs
        )

    def save(self, attrs):
        """Validate event input before saving."""
        if not self.validator.validate(attrs):
            raise EventValidationException(
                errors=self.validator.errors
            )
        return self.persist(attrs)


class CreateEvent(BaseEvent):
    """Event for creating an entity."""

    def save(self, attrs):
        """Generate aggregate id using uuid."""
        aggregate_id = self.entity.generate_new_guid()
        self.entity.aggregate_id = aggregate_id
        return super(CreateEvent, self).save(attrs)

    def get_aggregate_key(self):
        return '%s:%s' % (
            self.entity.aggregate_id, self.entity.INITIAL_VERSION
        )


class DeleteEvent(BaseEvent):

    @property
    def event_name(self):
        return 'Deleted'
