import dispatch

event_received = dispatch.Signal(
    providing_args=['aggregate_name', 'aggregate_id', 'payload']
)

command_received = dispatch.Signal(
    providing_args=['aggregate', 'command_name', 'command_data']
)

event_pre_save = dispatch.Signal(
    providing_args=[
        'aggregate_name', 'aggregate_id', 'payload',
        'event_name', 'version',
    ]
)

event_post_save = dispatch.Signal(
    providing_args=['event']
)
