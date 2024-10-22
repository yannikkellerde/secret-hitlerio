#!/bin/bash
export REDIS_HOST="127.0.0.1"
redis-server&
yarn prod &
sleep 3
yarn create-accounts
sleep 10000000
