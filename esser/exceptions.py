
class EsserException(Exception):

    def __init__(self, errors, message=None):
        message = '%s: %s' % (message or self.message, errors)
        super(EsserException, self).__init__(message)
        self.errors = errors


class IntegrityError(EsserException):

    message = 'Duplicate hash and range keys'


class EventValidationException(EsserException):

    message = 'Event validation error'


class AggregateDoesNotExist(Exception):
    pass


class AggregateDeleted(Exception):
    """
    Raised when aggregate contains a DeleteEvent
    """
    pass
