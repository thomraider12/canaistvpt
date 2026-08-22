#!/bin/bash

TOKEN=$(wget -qO- --timeout=15 --tries=2 https://services.iol.pt/matrix?userId)

if [ -z "$TOKEN" ]; then
  echo "Tokens são os mesmos."
  exit 0
fi

sed -i "s#wmsAuthSign=[^&]*#wmsAuthSign=${TOKEN}#g" *.m3u8

exit 0
