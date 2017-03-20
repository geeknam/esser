esser - [E]vent [S]ourcing [Ser]verlessly
============================================

[![Codefresh build status]( https://g.codefresh.io/api/badges/build?repoOwner=geeknam&repoName=esser&branch=master&pipelineName=esser&accountName=namngology&type=cf-1)]( https://g.codefresh.io/repositories/geeknam/esser/builds?filter=trigger:build;branch:master;service:58ce8dac6fc4340100512873~esser)
[![Build Status](https://travis-ci.org/geeknam/esser.svg?branch=master)](https://travis-ci.org/geeknam/esser)
[![Coverage Status](https://coveralls.io/repos/github/geeknam/esser/badge.svg?branch=master)](https://coveralls.io/github/geeknam/esser?branch=master)
[![Code Issues](https://www.quantifiedcode.com/api/v1/project/2644f358dc5246da951352fb0550f84f/badge.svg)](https://www.quantifiedcode.com/app/project/2644f358dc5246da951352fb0550f84f)



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

