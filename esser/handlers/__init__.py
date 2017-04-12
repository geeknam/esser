import importlib
import json
from esser.signals import event_received, event_post_save
from esser.registry import registry
from esser.repositories.base import Event


class LambdaHandler(object):

    @staticmethod
    def get_aggregate(aggregate_name, aggregate_id):
        """Given an aggregate name and id return Aggregate instance

        Args:
            aggregate_name (str): Aggregate Name
            aggregate_id (str): Aggregate ID

        Returns:
            esser.entities.Entity: aggregate / entity
        """
        path = registry.get_path(aggregate_name)
        module, class_name = path.rsplit('.', 1)
        app_module = importlib.import_module(module)
        aggregate_class = getattr(app_module, class_name)
        aggregate = aggregate_class(
            aggregate_id=aggregate_id
        )
        return aggregate

    @staticmethod
    def image_to_event(image):
        aggregate_id, version = image['aggregate_key']['S'].split(':')
        return Event(
            aggregate_name=image['aggregate_name']['S'],
            aggregate_id=aggregate_id,
            version=version,
            event_type=image['event_type']['S'],
            created_at=image['created_at']['S'],
            event_data=json.loads(image['event_data']['S']),
        )

    def handle_event(self, event, context):
        event_name = event['EventName']
        aggregate_id = event.get('AggregateId', None)
        aggregate = self.get_aggregate(event['AggregateName'], aggregate_id)
        event_received.send(
            sender=self.__class__,
            aggregate_name=event['AggregateName'],
            aggregate_id=aggregate_id,
            payload=event['Payload']
        )
        event_class_attr = None
        for event_key, cls in aggregate.__class__.__dict__.items():
            if hasattr(cls.__class__, 'event_name') and cls.__class__.event_name == event_name:
                event_class_attr = event_key
        aggregate_event = getattr(aggregate, event_class_attr, None)
        if aggregate_event:
            return aggregate_event.save(attrs=event['Payload'])
        return

    def handle_stream(self, event, context):
        for record in event['Records']:
            keys = record['dynamodb']['Keys']
            new_image = record['dynamodb']['NewImage']
            aggregate_name = keys['aggregate_name']['S']
            aggregate_key = keys['aggregate_key']['S']
            aggregate_id = aggregate_key.split(':')[0]
            aggregate = self.get_aggregate(aggregate_name, aggregate_id)
            event_obj = self.image_to_event(new_image)
            event_post_save.send(
                sender=aggregate.__class__,
                event=event_obj
            )


default_handler = LambdaHandler()

handle_event = default_handler.handle_event
handle_stream = default_handler.handle_stream
