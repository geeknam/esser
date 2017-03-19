from datetime import datetime
import uuid
from pynamodb.exceptions import PutError
from cerberus import Validator
from esser.constants import AGGREGATE_KEY_DELIMITER
from esser.exceptions import EventValidationException, IntegrityError
from esser.models import Event


class BaseEvent(object):
    """Base Event class."""

    def __init__(self):
        """
        Initialise the validator for the event based on schema.

        A valid Event class should have Event.schema
        """
        self.validator = Validator(self.schema)

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

    def persist(self, attrs):
        """Persist event in dynamodb."""
        event = Event(
            aggregate_name=self.entity.aggregate_name,
            aggregate_id=self.get_aggregate_key(),
            event_type=self.event_name,
            created_at=datetime.utcnow(),
            event_data=attrs
        )
        try:
            event.save(
                aggregate_name__ne=event.aggregate_name,
                aggregate_id__ne=event.aggregate_id,
                conditional_operator='and'
            )
        except PutError:
            raise IntegrityError(errors={
                'aggregate_name': event.aggregate_name,
                'aggregate_id': event.aggregate_id,
            })
        return event

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
        aggregate_id = str(uuid.uuid4())
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
