import importlib
from collections import defaultdict
from esser.registry import registry


def get_aggregate(aggregate_name, aggregate_id):
    path = registry.get_path(aggregate_name)
    module, class_name = path.rsplit('.', 1)
    app_module = importlib.import_module(module)
    aggregate_class = getattr(app_module, class_name)
    aggregate = aggregate_class(
        aggregate_id=aggregate_id
    )
    return aggregate


def handle_event(event, context):
    event_name = event['EventName']
    aggregate_id = event.get('AggregateId', None)
    aggregate = get_aggregate(event['AggregateName'], aggregate_id)
    event_class_attr = None
    for event_key, cls in aggregate.__class__.__dict__.items():
        if cls.__class__.__name__ == event_name:
            event_class_attr = event_key
    aggregate_event = getattr(aggregate, event_class_attr, None)
    if aggregate_event:
        return aggregate_event.save(attrs=event['Payload'])
    return


def handle_stream(event, context):
    aggregates = defaultdict(dict)
    for record in event['Records']:
        keys = record['dynamodb']['Keys']
        aggregate_name = keys['aggregate_name']['S']
        aggregate_key = keys['aggregate_key']['S']
        aggregate_id = aggregate_key.split(':')[0]
        aggregate = get_aggregate(aggregate_name, aggregate_id)
        aggregates[aggregate_name][aggregate_id] = aggregate.current_state
    return aggregates
