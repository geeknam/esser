from esser.signals.decorators import receiver
from esser.signals import event_pre_save, event_received
from esser.handlers import LambdaHandler
from items.commands import UpdatePrice


@receiver(event_pre_save, sender=UpdatePrice)
def check_price_update(sender, **kwargs):
    pass


@receiver(event_received, sender=LambdaHandler)
def do_something(sender, **kwargs):
    pass
