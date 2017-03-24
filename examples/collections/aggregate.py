from esser.entities import Entity
from esser.reducer import BaseReducer
from examples.collections import events
from examples.items.aggregate import Item


class CollectionReducer(BaseReducer):

    def on_collection_created(self, aggregate, next_event):
        return self.on_created(aggregate, next_event)

    def on_item_added(self, aggregate, next_event):
        item = Item(aggregate_id=next_event.event_data['aggregate_id'])
        aggregate['items'].append(item.current_state)
        return aggregate


class Collection(Entity):
    """
    Collection is an Aggregate root
    """
    reducer = CollectionReducer()
    created = events.CollectionCreated()
    item_added = events.ItemAdded()
    item_added_with_validation = events.ItemAddedWithExistanceValidation()

    def get_initial_state(self):
        return {
            'items': []
        }
