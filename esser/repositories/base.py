from esser.repositories import mixins
from esser.repositories.models import Event


class BaseRepository(object):

    def __init__(self, aggregate):
        self.aggregate = aggregate


class DynamoDBRepository(BaseRepository, mixins.ReadMixin, mixins.WriteMixin):

    model = Event
