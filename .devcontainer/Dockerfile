FROM nikolaik/python-nodejs:python3.7-nodejs14

# Provide an optional non-root user with sudo
ARG USERNAME=temat
ARG USER_UID=1000
ARG USER_GID=$USER_UID
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID --shell /bin/bash --create-home $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

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
