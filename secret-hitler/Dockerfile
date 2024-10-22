FROM node:16.13.0-buster

RUN apt-get -y update
RUN apt-get -qyy install lsb-release curl gpg && \
    curl -fsSL https://packages.redis.io/gpg | gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg && \
    chmod 644 /usr/share/keyrings/redis-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/redis.list && \
    apt-get -y update && \
    apt-get -y install redis

ADD . / app/
WORKDIR /app

RUN yarn

ENTRYPOINT ["/usr/bin/env"]
CMD [ "bash", "/app/on_start.bash" ]