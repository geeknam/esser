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

