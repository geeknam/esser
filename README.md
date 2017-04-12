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
