from esser.repositories import mixins


class DynamoDBRepository(mixins.ReadMixin, mixins.WriteMixin):

    def __init__(self, aggregate):
        self.aggregate = aggregate
