FROM node:23-bookworm as base
ENV DEBIAN_FRONTEND=noninteractive 

RUN apt-get -y update && apt-get -qyy install git curl

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.1/install.sh | bash
ADD secret-hitler / app/
WORKDIR /app

ENV NVM_DIR="$HOME/.nvm"

RUN export NVM_DIR="$HOME/.nvm" && \
    [ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh" && \
    [ -s "$NVM_DIR/bash_completion" ] && . "$NVM_DIR/bash_completion" && \
    nvm install "16.13.0" && \
    nvm use "16.13.0" && \
    yarn
    
ENTRYPOINT ["/usr/bin/env"]
#CMD [ "bash", "-c", "sleep 10000" ]
CMD [ "bash", "-c", "export NVM_DIR=$HOME/.nvm && \
    [ -s $NVM_DIR/nvm.sh ] && . $NVM_DIR/nvm.sh && \
    [ -s $NVM_DIR/bash_completion ] && . $NVM_DIR/bash_completion && \
    nvm use 16.13.0 && yarn prod" ]