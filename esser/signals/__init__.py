import dispatch

event_received = dispatch.Signal(
    providing_args=['aggregate_name', 'aggregate_id', 'payload']
)

event_pre_save = dispatch.Signal(
    providing_args=[
        'aggregate_name', 'aggregate_id', 'payload',
        'event_name', 'version',
    ]
)

event_post_save = dispatch.Signal(
    providing_args=[
        'aggregate_name', 'aggregate_id', 'payload',
        'event_name', 'version',
    ]
)
