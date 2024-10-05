#!/bin/bash

cd /home/runner/work/canaistvpt/canaistvpt/iptv-org-epg && npm install

# PT EPG

npm run grab -- --channels=../EPG/pt.channels.xml --output=../EPG/epg-pt.xml --days=7 --maxConnections=50

echo "EPG PT atualizada!"
sleep 3

# MEO EPG

npm run grab -- --channels=../EPG/meo.pt.channels.xml --output=../EPG/epg-meo-pt.xml --days=7 --maxConnections=50

echo "EPG da MEO atualizada!"
sleep 3

# NOS EPG

npm run grab -- --channels=../EPG/nos.pt.channels.xml --output=../EPG/epg-nos-pt.xml --days=7 --maxConnections=50

echo "EPG da NOS atualizada!"
sleep 3

# Rytec EPG

cd ../EPG
wget -O epg-rytec-pt.xml.xz "http://www.xmltvepg.nl/rytecPT.xz"

echo "EPG da Rytec atualizada!"
sleep 3

# Comprimir ficheiros XML da EPG

xz -k -f -9 epg*.xml

echo -e "Ficheiros comprimidos."
sleep 3

# Apagar ficheiros XML

rm epg*.xml

echo "Ficheiros apagados! A sair!"
sleep 3


exit 0
