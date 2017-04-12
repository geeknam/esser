from esser.entities import Entity
from esser.reducer import BaseReducer
from basket import commands
from items.aggregate import Item


class BasketReducer(BaseReducer):

    def on_basket_created(self, aggregate, next_event):
        return self.on_created(aggregate, next_event)

    def on_item_added(self, aggregate, next_event):
        item = Item(aggregate_id=next_event.event_data['aggregate_id'])
        aggregate['items'].append(item.current_state)
        return aggregate

    def on_item_added_with_projection(self, aggregate, next_event):
        aggregate['items'].append(next_event.event_data['aggregate_id'])
        return aggregate


class Basket(Entity):
    """
    Basket is an Aggregate root
    """
    reducer = BasketReducer()
    created = commands.CreateBasket()
    item_added = commands.AddItem()
    item_added_with_validation = commands.AddItemWithExistanceValidation()
    item_added_with_projection = commands.AddItemWithProjection()

    def get_initial_state(self):
        return {
            'items': []
        }
