from datetime import datetime
from pynamodb.exceptions import PutError

from esser.models import Event
from esser.exceptions import AggregateDoesNotExist, IntegrityError


class ReadMixin(object):

    def get_events(self, version):
        """
        Get all events up to specific version
        """
        return Event.query(
            self.aggregate.aggregate_name,
            aggregate_id__le='%s:%s' % (
                self.aggregate.aggregate_id, version
            )
        )

    def get_all_events(self):
        """
        Get all events up to latest version
        """
        return Event.query(
            self.aggregate.aggregate_name,
            aggregate_id__begins_with=self.aggregate.aggregate_id
        )

    def get_last_event(self):
        events = list(Event.query(
            self.aggregate.aggregate_name,
            aggregate_id__begins_with=self.aggregate.aggregate_id,
            limit=1, scan_index_forward=False
        ))
        try:
            return events[0]
        except IndexError:
            raise AggregateDoesNotExist()


class WriteMixin(object):

    def persist(self, aggregate_id, event_type, attrs):
        """Persist event in dynamodb."""
        event = Event(
            aggregate_name=self.aggregate.aggregate_name,
            aggregate_id=aggregate_id,
            event_type=event_type,
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
