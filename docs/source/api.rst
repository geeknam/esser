.. _api:

Developer Interface
===================

.. module:: esser

This part of the documentation covers all the interfaces of `esser`.


Entities / Aggregates
-----------------------

.. autoclass:: esser.entities.Entity
    :members:
    :undoc-members:

Repositories
-----------------------

.. automodule:: esser.repositories.mixins
    :members:
    :undoc-members:

.. automodule:: esser.repositories.base
    :members:
    :undoc-members:

Data Persistence
-----------------------

.. automodule:: esser.models
    :members:
    :undoc-members:


Events
-----------------------

.. autoclass:: esser.events.BaseEvent
    :members:
    :undoc-members:

.. autoclass:: esser.events.CreateEvent
    :members:
    :undoc-members:

.. autoclass:: esser.events.DeleteEvent
    :members:
    :undoc-members:


Reducers
---------------------

.. autoclass:: esser.reducer.BaseReducer
    :members:
    :undoc-members:



Exceptions
-----------------------

.. automodule:: esser.exceptions
    :members:
    :undoc-members: