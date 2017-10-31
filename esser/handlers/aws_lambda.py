import importlib
from esser.registry import registry
from esser.signals import command_received


class CommandHandler(object):

    @property
    def command_name(self):
        raise NotImplementedError()

    @property
    def command_data(self):
        raise NotImplementedError()

    @property
    def aggregate_name(self):
        raise NotImplementedError()

    @property
    def aggregate_id(self):
        raise NotImplementedError()

    @property
    def aggregate_class(self):
        """Given an aggregate name and id return Aggregate class

        Returns:
            esser.entities.Entity: aggregate / entity
        """
        path = registry.get_path(self.aggregate_name)
        module, class_name = path.rsplit('.', 1)
        app_module = importlib.import_module(module)
        return getattr(app_module, class_name)

    @property
    def aggregate(self):
        return self.aggregate_class(
            aggregate_id=self.aggregate_id
        )

    def dispatch(self):
        command_received.send(
            sender=self.aggregate_class,
            aggregate=self.aggregate,
            command_name=self.command_name,
            command_data=self.command_data
        )


class AwsLambdaCommandHandler(CommandHandler):

    def __init__(self, event, context):
        self.event = event
        self.context = context

    @property
    def command_name(self):
        return self.event['CommandName']

    @property
    def command_data(self):
        return self.event['Payload']

    @property
    def aggregate_name(self):
        return self.event['AggregateName']

    @property
    def aggregate_id(self):
        return self.event['AggregateId']

    @property
    def command(self):
        for command_key, cls in self.aggregate_class.__dict__.items():
            if hasattr(cls.__class__, 'command_name') and cls.__class__.command_name == self.command_name:
                return getattr(self.aggregate, command_key, None)
        return
