FROM nikolaik/python-nodejs:python3.7-nodejs12

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
ENV WORKON_HOME /usr/src/.venvs
ENV CHOKIDAR_USEPOLLING true

# Install packages
RUN apt-get install -y nano htop && npm install -g @vue/cli

# Create project folder structure
WORKDIR /usr/src/
RUN mkdir app && mkdir .venvs

WORKDIR /usr/src/app/

EXPOSE 8000
EXPOSE 8080
