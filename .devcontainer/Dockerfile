FROM nikolaik/python-nodejs:python3.7-nodejs14

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIPENV_VENV_IN_PROJECT 1
ENV CHOKIDAR_USEPOLLING true

# Install packages & configure zsh as terminal
RUN apt update && apt install -y nano htop fonts-powerline
RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.1/zsh-in-docker.sh)" -- \
    -t agnoster \
    -p debian \
    -p git \
    -p git-flow \
    -p colorize \
    -p command-not-found \
    -p python \
    -p pip \
    -p node \
    -p npm

WORKDIR /usr/src/app/

EXPOSE 8000
EXPOSE 8080
