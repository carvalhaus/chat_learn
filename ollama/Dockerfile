FROM ollama/ollama

ENV APP_HOME=/home

WORKDIR $APP_HOME

COPY . .

USER root
RUN apt-get update && apt-get install -y curl bash && rm -rf /var/lib/apt/lists/*

RUN chmod +x pull-ollama.sh

ENTRYPOINT ["/usr/bin/bash", "pull-ollama.sh"]