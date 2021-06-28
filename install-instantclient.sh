#!/bin/bash -e

oracle_home_directory=/opt/oracle

echo "Installing instantclient for linux 64-bit distribution. See docs: https://www.oracle.com/database/technologies/instant-client/linux-x86-64-downloads.html"

mkdir -p ${oracle_home_directory}

cd ${oracle_home_directory}

curl -o instantclient_19_11.zip https://download.oracle.com/otn_software/linux/instantclient/1911000/instantclient-basic-linux.x64-19.11.0.0.0dbru.zip

unzip instantclient_19_11.zip && rm -fr instantclient_19_11.zip

apt-get update && apt-get install -y libaio1