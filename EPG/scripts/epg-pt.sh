# VODAFONE EPG
python vodafonept.py
echo "EPG da Vodafone atualizada!"

# Mover para a pasta iptv-org-epg onde o npm está instalado
cd /home/runner/work/canaistvpt/canaistvpt/iptv-org-epg && npm install

# PT EPG
npm run grab --- --channels=../EPG/pt.channels.xml --output=../EPG/epg-pt.xml --days=8 --maxConnections=500
echo "EPG PT atualizada!"

# NOS EPG
npm run grab --- --channels=../EPG/meo.pt.channels.xml --output=../EPG/epg-meo-pt.xml --days=8 --maxConnections=500
echo "EPG da MEO atualizada!"

npm run grab --- --channels=../EPG/testepg.pt.channels.xml --output=../EPG/epg-test-pt.xml --days=8 --maxConnections=800
echo "EPG de Teste atualizada!"

npm run grab --- --channels=../EPG/opto.sic.pt.channels.xml --output=../EPG/epg-sic-pt.xml --days=8 --maxConnections=100
echo "EPG da Opto atualizada!"

# Mudar para a pasta EPG para comprimir e apagar os ficheiros
cd ../EPG

# Comprimir ficheiros XML na pasta EPG
gzip -f -9 epg*.xml
echo "Ficheiros comprimidos."

exit 0
