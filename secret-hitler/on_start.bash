#!/bin/bash
export REDIS_HOST="127.0.0.1"
redis-server&
yarn prod &
sleep 3
yarn create-accounts
yarn assign-local-mod
sleep infinity
