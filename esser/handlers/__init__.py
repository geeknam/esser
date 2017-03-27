import importlib
from esser.registry import registry


def handle_event(event, context):
    event_name = event['EventName']
    aggregate_id = event.get('AggregateId', None)
    path = registry.get_path(event['AggregateName'])
    module, class_name = path.rsplit('.', 1)
    app_module = importlib.import_module(module)
    aggregate_class = getattr(app_module, class_name)
    aggregate = aggregate_class(
        aggregate_id=aggregate_id
    )
    event_class_attr = None
    for event_key, cls in aggregate.__class__.__dict__.items():
        if cls.__class__.__name__ == event_name:
            event_class_attr = event_key
    aggregate_event = getattr(aggregate, event_class_attr, None)
    if aggregate_event:
        return aggregate_event.save(attrs=event['Payload'])
    return
