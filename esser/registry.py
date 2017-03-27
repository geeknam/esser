

class AggregateRegistry(object):

    def __init__(self):
        self.aggregate_paths = {}

    def register(self, aggregate_name, path):
        self.aggregate_paths.update({
            aggregate_name: path
        })

    def get_path(self, aggregate_name):
        return self.aggregate_paths[aggregate_name]

    def clear(self):
        self.aggregate_paths = {}


registry = AggregateRegistry()


def register(aggregate_class):
    path = '%s.%s' % (
        aggregate_class.__module__,
        aggregate_class.__name__
    )
    registry.register(
        aggregate_class.__name__, path
    )
    return aggregate_class
