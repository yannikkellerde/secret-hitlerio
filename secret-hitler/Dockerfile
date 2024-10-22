FROM node:16.13.0-stretch

ADD . / app/
WORKDIR /app

RUN yarn

ADD on_start.bash /app

ENTRYPOINT ["/usr/bin/env"]
CMD [ "bash", "/app/on_start.bash" ]