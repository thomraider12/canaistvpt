#!/bin/bash

# Mover para a pasta iptv-org-epg onde o npm está instalado
cd /home/runner/work/canaistvpt/canaistvpt/iptv-org-epg && npm install

# PT EPG
npm run grab -- --channels=../EPG/pt.channels.xml --output=../EPG/epg-pt.xml --days=7 --maxConnections=50
echo "EPG PT atualizada!"
sleep 3

# NOS EPG
npm run grab -- --channels=../EPG/nos.pt.channels.xml --output=../EPG/epg-nos-pt.xml --days=7 --maxConnections=50
echo "EPG da NOS atualizada!"
sleep 3

# Mudar para a pasta EPG para comprimir e apagar os ficheiros
cd ../EPG

# Comprimir ficheiros XML na pasta EPG
gzip -f -9 epg*.xml
echo "Ficheiros comprimidos."
sleep 3

# Apagar ficheiros XML na pasta EPG
rm epg*.xml
echo "Ficheiros XML apagados! A sair!"
sleep 3

exit 0
