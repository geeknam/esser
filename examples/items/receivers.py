from esser.signals.decorators import receiver
from esser.signals import event_pre_save, event_received, event_post_save
from esser.handlers import LambdaHandler
from items.commands import UpdatePrice


@receiver(event_pre_save, sender=UpdatePrice)
def check_price_update(sender, **kwargs):
    print('Event pre save handled: %s' % kwargs)


@receiver(event_received, sender=LambdaHandler)
def do_something(sender, **kwargs):
    print('Command received handled: %s' % kwargs)


@receiver(event_post_save)
def handle_event_saved(sender, **kwargs):
    print('Post saved handled: %s' % kwargs['event'].as_dict())
