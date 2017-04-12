esser - [E]vent [S]ourcing [Ser]verlessly
============================================

[![pypi version]( https://img.shields.io/pypi/v/esser.svg)]( https://pypi.python.org/pypi/esser)
[![pypi package]( https://img.shields.io/pypi/dm/esser.svg)]( https://pypi.python.org/pypi/esser)
[![Build Status](https://travis-ci.org/geeknam/esser.svg?branch=master)](https://travis-ci.org/geeknam/esser)
[![Coverage Status](https://coveralls.io/repos/github/geeknam/esser/badge.svg?branch=master)](https://coveralls.io/github/geeknam/esser?branch=master)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/2644f358dc5246da951352fb0550f84f/badge.svg)](https://www.quantifiedcode.com/app/project/2644f358dc5246da951352fb0550f84f)
[![Slack](https://img.shields.io/badge/chat-slack-ff69b4.svg)](https://esser-py.slack.com/)


- Serverless + Pay-As-You-Go
- Aggregates
- Snapshots
- Projections

Architectural Design
-----------------------

[![Esser Diagram]( https://cloud.githubusercontent.com/assets/199628/24705037/6cbf50b0-1a4d-11e7-99d5-7ad32295912c.png)]

Features
--------------

- Command validation
- Datastore agnostic read layer
- Push based messaging via DynamoDB Stream
- Built-in Snapshotting
- Publish / subscribe style signalling
- Generated Cloudformation templates (Infrastructure as Code)


Components
-----------------

- Runtime: AWS Lambda (Python)
- Append Only Event Store: DynamoDB
- Event Source Triggers: DynamoDB Stream
- Read / Query Store: PostgreSQL / Elasticsearch (via contrib)

Example Usage
------------------

#### Add first entity

`items/aggregate.py`

```python
from esser.entities import Entity
from esser.registry import register
from items import commands
from items import receivers
from items.reducer import ItemReducer


@register
class Item(Entity):

    reducer = ItemReducer()
    created = commands.CreateItem()
    price_updated = commands.UpdatePrice()

```

#### Add commands that can be issued

`items/commands.py`

```python
from esser.commands import BaseCommand, CreateCommand


class CreateItem(CreateCommand):

    event_name = 'ItemCreated'
    schema = {
        'name': {'type': 'string'},
        'price': {'type': 'float'}
    }


class UpdatePrice(BaseCommand):

    event_name = 'PriceUpdated'
    schema = {
        'price': {'type': 'float', 'diff': True}
    }
```

#### Add reducer to fold event stream

`items/reducer.py`

```python
from esser.reducer import BaseReducer

class ItemReducer(BaseReducer):

    def on_item_created(self, aggregate, next_event):
        return self.on_created(aggregate, next_event)

    def on_price_updated(self, aggregate, next_event):
        aggregate['price'] = next_event.event_data['price']
        return aggregate

```

#### Subscribe to events

`items/receivers.py`


```python
from esser.signals.decorators import receiver
from esser.signals import event_pre_save, event_received, event_post_save
from esser.handlers import LambdaHandler
from items.commands import UpdatePrice


@receiver(event_pre_save, sender=UpdatePrice)
def presave_price_updated(sender, **kwargs):
    # Do something before saving the event
    pass


@receiver(event_received, sender=LambdaHandler)
def received_command(sender, **kwargs):
    # when the command is received
    pass

@receiver(event_post_save)
def handle_event_saved(sender, **kwargs):
    # when the event has already been saved
    pass

```
