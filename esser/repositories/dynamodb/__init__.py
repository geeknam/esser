from datetime import datetime
from pynamodb.exceptions import PutError

from esser.repositories.base import BaseRepository, Event
from esser.repositories.dynamodb.models import DynamoDBEventModel
from esser.constants import AGGREGATE_KEY_DELIMITER
from esser.exceptions import AggregateDoesNotExist, IntegrityError


class DynamoDBRepository(BaseRepository):

    model = DynamoDBEventModel

    def to_event(self, obj):
        return Event(
            aggregate_name=obj.aggregate_name,
            aggregate_id=obj.aggregate_id,
            version=obj.version,
            event_type=obj.event_type,
            created_at=obj.created_at,
            event_data=obj.event_data.as_dict()
        )

    def get_events(self, version):
        """
        Get all events up to specific version
        """
        for item in self.model.query(
            self.aggregate.aggregate_name,
            aggregate_key__le='%s:%s' % (
                self.aggregate.aggregate_id, version
            )
        ):
            yield self.to_event(item)

    def get_all_events(self):
        """
        Get all events up to latest version
        """
        for item in self.model.query(
            self.aggregate.aggregate_name,
            aggregate_key__begins_with=self.aggregate.aggregate_id
        ):
            yield self.to_event(item)

    def get_last_event(self):
        events = list(self.model.query(
            self.aggregate.aggregate_name,
            aggregate_key__begins_with=self.aggregate.aggregate_id,
            limit=1, scan_index_forward=False
        ))
        try:
            return self.to_event(events[0])
        except IndexError:
            raise AggregateDoesNotExist()

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
        event = self.model(
            aggregate_name=self.aggregate.aggregate_name,
            aggregate_key=aggregate_key,
            event_type=event_type,
            created_at=datetime.utcnow(),
            event_data=attrs
        )
        try:
            event.save(
                aggregate_name__ne=event.aggregate_name,
                aggregate_key__ne=event.aggregate_key,
                conditional_operator='and'
            )
        except PutError:
            raise IntegrityError(errors={
                'aggregate_name': event.aggregate_name,
                'aggregate_key': event.aggregate_key,
            })
        return self.to_event(event)
