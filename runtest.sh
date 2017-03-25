#!/bin/bash

# sleep to wait for dynamodb container to bootstrap
sleep 1
set -e
nosetests --with-coverage --cover-package=esser
coveralls

travis-sphinx -n build
travis-sphinx -n deploy