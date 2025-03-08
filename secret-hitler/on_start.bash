#!/bin/bash

export REDIS_HOST="127.0.0.1"

# Start Redis in background
redis-server &

# Decide whether to run in dev or prod mode based on NODE_ENV
if [ "$NODE_ENV" = "development" ]; then
    echo "Starting app in DEVELOPMENT mode..."
    # Runs both React (via webpack-dev-server) and Express (via nodemon) if your "dev" script does that
    yarn dev &
else
    echo "Starting app in PRODUCTION mode..."
    yarn prod &
fi

# Give the server(s) a few seconds to start
sleep 10

# Optionally run your script(s) to create accounts, assign mods, etc.
yarn create-accounts
yarn assign-local-mod
yarn prepare

# Keep container alive
sleep infinity
