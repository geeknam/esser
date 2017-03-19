esser - [E]vent [S]ourcing [Ser]verlessly
============================================

- Serverless + Pay-As-You-Go
- Aggregates
- Snapshots
- Projections

Runtime
-----------------

- AWS Lambda Python


Event Store
-----------------

The primary data store used for writes is `DynamoDB`
Snapshoting can be achieved via `DynamoDB` streams

Query Store
-----------------

Aggregates should be queried using a different store.
Available strategies for storing materialsed views:

- PostgreSQL
- Elasticsearch
- Redis

AWS Lambda can pull changes from DynamoDB stream and update the
query models.

