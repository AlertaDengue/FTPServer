FROM debian:bullseye-slim

ARG UID
ARG GID

USER root

RUN apt-get update && apt-get install -y vsftpd \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN groupadd -g ${GID} ftpuser \
  && useradd -u ${UID} -g ${GID} -m -s /bin/bash ftpuser \
  && mkdir -p /opt/services/ftp /etc/sudoers.d/ \
  && chown -R ftpuser:ftpuser /opt/services \
  && echo "ftpuser ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/ftpuser \
  && chmod 0440 /etc/sudoers.d/ftpuser

USER ftpuser

WORKDIR /opt/services/ftp
