from cerberus import Validator


class EsserValidator(Validator):

    def __init__(self, *args, **kwargs):
        if 'aggregate' in kwargs:
            self.aggregate = kwargs['aggregate']
        if 'event' in kwargs:
            self.event = kwargs['event']
        super(EsserValidator, self).__init__(*args, **kwargs)

    def _validate_diff(self, diff, field, value):
        if diff:
            agg_field_value = self.aggregate.current_state.get(field, None)
            if agg_field_value == value:
                self._error(
                    field,
                    "already has the value of: %s" % agg_field_value
                )

    def _validate_aggregate_exists(self, aggregate_exists, field, value):
        if aggregate_exists and field == 'aggregate_id':
            related_aggregate = self.event.related_aggregate(aggregate_id=value)
            state = related_aggregate.current_state
            if not state:
                self._error(
                    field,
                    "aggregate for id %s does not exist" % value
                )
