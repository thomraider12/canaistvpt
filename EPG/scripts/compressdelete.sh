cd ../EPG
xz -k -f -9 epg*.xml && gzip -k -f -9 epg*.xml
echo "Ficheiros comprimidos."
sleep 3
cd ../EPG
rm epg*.xml
echo "Ficheiros XML apagados!"
sleep 3

exit 0
