from esser.entities import Entity
from esser.event_handler import BaseEventHandler
from esser.registry import register
from items import commands
from items import receivers


class ItemEventHandler(BaseEventHandler):

    def on_item_created(self, aggregate, next_event):
        return self.on_created(aggregate, next_event)

    def on_item_updated(self, aggregate, next_event):
        return self.on_updated(aggregate, next_event)

    def on_price_updated(self, aggregate, next_event):
        aggregate['price'] = next_event.event_data['price']
        return aggregate

    def on_colors_added(self, aggregate, next_event):
        aggregate['colors'] = next_event.event_data['colors']
        return aggregate


@register
class Item(Entity):

    event_handler = ItemEventHandler()
    price_updated = commands.UpdatePrice()
    colors_added = commands.AddColors()
    created = commands.CreateItem()
    deleted = commands.DeleteItem()

    @property
    def price(self):
        try:
            return self.current_state['price']
        except KeyError:
            raise AttributeError()

    @price.setter
    def price(self, value):
        self.price_updated.save(attrs={'price': value})
