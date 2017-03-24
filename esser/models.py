import os
from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import (
    UnicodeAttribute, UTCDateTimeAttribute,
    MapAttribute
)
from esser.constants import AGGREGATE_KEY_DELIMITER


class Event(Model):
    """
    A DynamoDB Event model
    """
    class Meta:
        table_name = "events"
        host = os.getenv('DYNAMODB_HOST', None)
    aggregate_name = UnicodeAttribute(hash_key=True)
    aggregate_id = UnicodeAttribute(range_key=True)
    event_type = UnicodeAttribute()
    created_at = UTCDateTimeAttribute()
    event_data = MapAttribute()

    @classmethod
    def _conditional_operator_check(cls, conditional_operator):
        pass

    @property
    def guid(self):
        return self.aggregate_id.split(AGGREGATE_KEY_DELIMITER)[0]


class Snapshot(Model):

    class Meta:
        table_name = "snapshots"
        host = os.getenv('DYNAMODB_HOST', None)
    aggregate_name = UnicodeAttribute(hash_key=True)
    aggregate_key = UnicodeAttribute(range_key=True)
    created_at = UTCDateTimeAttribute()
    state = MapAttribute()

    @classmethod
    def from_aggregate(cls, aggregate):
        state = aggregate.current_state
        last_event = aggregate.repository.get_last_event()
        snapshot = cls(
            aggregate_name=aggregate.aggregate_name,
            aggregate_key=last_event.aggregate_id,
            created_at=datetime.utcnow(),
            state=state
        )
        snapshot.save()
        return snapshot

    @classmethod
    def get_last_for(cls, aggregate, aggregate_id):
        cls.query(
            aggregate.aggregate_name,
            aggregate_id__begins_with=aggregate_id
        )
