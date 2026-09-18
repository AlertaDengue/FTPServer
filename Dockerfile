FROM python:3.12-slim

ARG GID
ARG UID
ENV TERM=xterm-256color

RUN groupadd -g ${GID} ftpgroup \
  && useradd -u ${UID} -g ${GID} -m -s /bin/bash ftpuser

RUN pip install --no-cache-dir pyftpdlib

USER ftpuser

WORKDIR /home/ftpuser/

COPY --chown=ftpuser:ftpgroup entrypoint.py /entrypoint.py

ENTRYPOINT ["python", "/entrypoint.py"]
