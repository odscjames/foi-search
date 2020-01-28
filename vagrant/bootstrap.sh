#!/bin/bash

set -e

apt-get update

DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip apt-transport-https virtualenv

wget -O - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add -

echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-7.x.list

apt-get update

DEBIAN_FRONTEND=noninteractive apt-get install -y elasticsearch

systemctl daemon-reload
systemctl enable elasticsearch.service
systemctl start elasticsearch.service
