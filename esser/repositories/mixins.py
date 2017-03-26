from datetime import datetime
from pynamodb.exceptions import PutError

from esser.constants import AGGREGATE_KEY_DELIMITER
from esser.models import Event
from esser.exceptions import AggregateDoesNotExist, IntegrityError


class ReadMixin(object):

    def get_events(self, version):
        """
        Get all events up to specific version
        """
        return Event.query(
            self.aggregate.aggregate_name,
            aggregate_key__le='%s:%s' % (
                self.aggregate.aggregate_id, version
            )
        )

    def get_all_events(self):
        """
        Get all events up to latest version
        """
        return Event.query(
            self.aggregate.aggregate_name,
            aggregate_key__begins_with=self.aggregate.aggregate_id
        )

    def get_last_event(self):
        events = list(Event.query(
            self.aggregate.aggregate_name,
            aggregate_key__begins_with=self.aggregate.aggregate_id,
            limit=1, scan_index_forward=False
        ))
        try:
            return events[0]
        except IndexError:
            raise AggregateDoesNotExist()


class WriteMixin(object):

    @classmethod
    def get_aggregate_key(cls, aggregate_id, version):
        """Increment version of the event for the aggregate."""
        return '{aggregate_id}{delimiter}{version}'.format(
            aggregate_id=aggregate_id,
            delimiter=AGGREGATE_KEY_DELIMITER,
            version=version
        )

    def persist(self, aggregate_id, version, event_type, attrs):
        """Persist event in dynamodb."""
        aggregate_key = self.__class__.get_aggregate_key(
            aggregate_id, version
        )
        event = Event(
            aggregate_name=self.aggregate.aggregate_name,
            aggregate_key=aggregate_key,
            event_type=event_type,
            created_at=datetime.utcnow(),
            event_data=attrs
        )
        try:
            event.save(
                aggregate_name__ne=event.aggregate_name,
                aggregate_key__ne=event.aggregate_id,
                conditional_operator='and'
            )
        except PutError:
            raise IntegrityError(errors={
                'aggregate_name': event.aggregate_name,
                'aggregate_id': event.aggregate_id,
            })
        return event
