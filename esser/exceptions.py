
class IntegrityError(Exception):
    def __init__(self, errors, message='Duplicate hash and range keys'):
        message = '%s: %s' % (message, errors)
        super(IntegrityError, self).__init__(message)
        self.errors = errors


class EventValidationException(Exception):
    def __init__(self, errors, message='Event validation error'):
        message = '%s: %s' % (message, errors)
        super(EventValidationException, self).__init__(message)
        self.errors = errors


class AggregateDoesNotExist(Exception):
    pass


class AggregateDeleted(Exception):
    """
    Raised when aggregate contains a DeleteEvent
    """
    pass
