#!/bin/bash
export NVM_DIR=$HOME/.nvm
[ -s $NVM_DIR/nvm.sh ] && . $NVM_DIR/nvm.sh
[ -s $NVM_DIR/bash_completion ] && . $NVM_DIR/bash_completion
nvm use 16.13.0
yarn prod&
sleep 3
yarn create-accounts