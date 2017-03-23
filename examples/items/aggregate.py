from esser.entities import Entity
from esser.reducer import BaseReducer
from examples.items import events


class ItemReducer(BaseReducer):

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


class Item(Entity):

    reducer = ItemReducer()
    price_updated = events.PriceUpdated()
    colors_added = events.ColorsAdded()
    created = events.ItemCreated()
    deleted = events.Deleted()
