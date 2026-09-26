#!/bin/bash

URL="https://sic.live.impresa.pt/sic.m3u8"
OUTPUT="sic.m3u8"

curl -fsSL \
  --retry 2 \
  --max-time 15 \
  -A "Firefox" \
  -e "https://sic.pt/" \
  -H "Origin: https://sic.pt/" \
  "$URL" -o "$OUTPUT"

if [ $? -ne 0 ]; then
  echo "Erro ao descarregar $URL"
  exit 1
fi

echo "SIC.m3u8 atualizado."
