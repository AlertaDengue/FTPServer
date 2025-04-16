FROM debian:buster AS builder

ENV DEBIAN_FRONTEND noninteractive
RUN echo "deb http://http.debian.net/debian buster main\n\
  deb-src http://http.debian.net/debian buster main\n\
  deb http://http.debian.net/debian buster-updates main\n\
  deb-src http://http.debian.net/debian buster-updates main\n\
  deb http://security.debian.org buster/updates main\n\
  deb-src http://security.debian.org buster/updates main\n\
  " > /etc/apt/sources.list

RUN apt-get -y update && \
  apt-get -y --force-yes --fix-missing install dpkg-dev debhelper &&\
  apt-get -y build-dep pure-ftpd

RUN mkdir /tmp/pure-ftpd/ && \
  cd /tmp/pure-ftpd/ && \
  apt-get source pure-ftpd && \
  cd pure-ftpd-* && \
  ./configure --with-tls | grep -v '^checking' | grep -v ': Entering directory' | grep -v ': Leaving directory' && \
  sed -i '/CAP_SYS_NICE,/d; /CAP_DAC_READ_SEARCH/d; s/CAP_SYS_CHROOT,/CAP_SYS_CHROOT/;' src/caps_p.h && \
  dpkg-buildpackage -b -uc | grep -v '^checking' | grep -v ': Entering directory' | grep -v ': Leaving directory'


FROM debian:buster-slim

LABEL maintainer "Luã Bida Vacaro <github.com/luabida>"

ARG UID
ARG GID
ARG FTP_USER_PASS
ENV FTP_USER_UID=${UID}
ENV FTP_USER_GID=${GID}
ENV FTP_USER_PASS=${FTP_USER_PASS}
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get -y update && \
  apt-get  --no-install-recommends --yes install \
  libc6 \
  libcap2 \
  libmariadb3 \
  libpam0g \
  libssl1.1 \
  lsb-base \
  openbsd-inetd \
  openssl \
  perl \
  rsyslog

COPY --from=builder /tmp/pure-ftpd/*.deb /tmp/pure-ftpd/

RUN dpkg -i /tmp/pure-ftpd/pure-ftpd-common*.deb &&\
  dpkg -i /tmp/pure-ftpd/pure-ftpd_*.deb && \
  # dpkg -i /tmp/pure-ftpd/pure-ftpd-ldap_*.deb && \
  # dpkg -i /tmp/pure-ftpd/pure-ftpd-mysql_*.deb && \
  # dpkg -i /tmp/pure-ftpd/pure-ftpd-postgresql_*.deb && \
  rm -Rf /tmp/pure-ftpd

RUN apt-mark hold pure-ftpd pure-ftpd-common

RUN groupadd -g ${GID} ftpgroup &&\
  useradd -u ${UID} -g ${GID} -d /home/ftpusers -s /dev/null ftpuser

RUN echo "" >> /etc/rsyslog.conf && \
  echo "#PureFTP Custom Logging" >> /etc/rsyslog.conf && \
  echo "ftp.* /var/log/pure-ftpd/pureftpd.log" >> /etc/rsyslog.conf && \
  echo "Updated /etc/rsyslog.conf with /var/log/pure-ftpd/pureftpd.log"

COPY ftpserver/entrypoint.sh /entrypoint.sh
RUN chmod u+x /entrypoint.sh

RUN chown -R ftpuser:ftpgroup /etc/pure-ftpd && chmod 755 /etc/pure-ftpd

RUN apt-get -y clean \
  && apt-get -y autoclean \
  && apt-get -y autoremove \
  && rm -rf /var/lib/apt/lists/*

ENV PUBLICHOST localhost

VOLUME ["/home/ftpusers", "/home/ftpuser", "/etc/pure-ftpd/passwd"]

CMD /entrypoint.sh -l puredb:/etc/pure-ftpd/pureftpd.pdb -j -R -P $PUBLICHOST -Y 0

EXPOSE 21 30000-30009
