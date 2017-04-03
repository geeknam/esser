from esser.signals.decorators import receiver
from esser.signals import event_pre_save, event_received
from esser.handlers import LambdaHandler
from items.events import PriceUpdated


@receiver(event_pre_save, sender=PriceUpdated)
def check_price_update(sender, **kwargs):
    print sender
    print kwargs


@receiver(event_received, sender=LambdaHandler)
def do_something(sender, **kwargs):
    print sender
    print kwargs
