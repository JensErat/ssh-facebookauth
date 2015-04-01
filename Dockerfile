FROM debian:8
MAINTAINER Jens Erat <email@jenserat.de>

RUN \
  apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install --no-install-recommends -y openssh-server libpam-python python-requests-oauthlib python-pyfiglet toilet-fonts sl bsdgames && \
  mkdir -p /var/run/sshd && \
  sed -i "s:pam_unix.so nullok_secure:pam_python.so /opt/oauth.py:" /etc/pam.d/common-auth && \
  sed -i "s/ChallengeResponseAuthentication no/ChallengeResponseAuthentication yes/" /etc/ssh/sshd_config && \
  adduser --disabled-password --gecos "ALL_USERS_ALLOWED" --shell /opt/startgame.sh facebook && \
  echo "" > /etc/motd
COPY oauth.py startgame.sh /opt/

EXPOSE 22
CMD ["/usr/sbin/sshd", "-De"]
