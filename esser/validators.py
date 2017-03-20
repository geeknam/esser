from cerberus import Validator


class EsserValidator(Validator):

    def __init__(self, *args, **kwargs):
        if 'aggregate' in kwargs:
            self.aggregate = kwargs['aggregate']
        super(EsserValidator, self).__init__(*args, **kwargs)

    def _validate_diff(self, diff, field, value):
        if diff:
            agg_field_value = self.aggregate.current_state.get(field, None)
            if agg_field_value == value:
                self._error(
                    field,
                    "already has the value of: %s" % agg_field_value
                )
