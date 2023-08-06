FROM registry.gitlab.com/spirostack/salt-container:master

COPY dist/spirofs-*.tar.gz /tmp/spirofs.tar.gz
COPY vagrant/saltstack/etc/master /etc/salt/master.d/spiro.conf
COPY vagrant/saltstack/salt /srv/salt

RUN salt-call --local state.apply spiro && pip install /tmp/spirofs.tar.gz && rm /tmp/spirofs.tar.gz
