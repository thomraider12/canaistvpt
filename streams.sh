#!/bin/bash

# Atualizar o link da TVI
sed -i "/live_tvi\/live_tvi/ c https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" pt.m3u
if grep -q "live_tvi\/live_tvi" pt.m3u; then
  echo "Link da TVI atualizado."
else
  echo "Link da TVI não atualizado."
fi

# Atualizar o link da CNN Portugal
sed -i "/live_cnn/ c https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" pt.m3u
if grep -q "live_cnn" pt.m3u; then
  echo "Link da CNN Portugal atualizado com sucesso."
else
  echo "Link da CNN Portugal não atualizado."
fi

# Extração do link m3u8 da live do YouTube
YOUTUBE_URL="https://www.youtube.com/watch?v=BJ3Yv572V1A"

# Baixar o código-fonte da página da live
curl -s "$YOUTUBE_URL" -o pagina.html

# Procurar o link m3u8
M3U8_URL=$(grep -oP 'https://manifest\.googlevideo\.com/api/manifest/hls_variant/[^"]+' pagina.html)

# Verificar se o link foi encontrado
if [ -z "$M3U8_URL" ]; then
    echo "Nenhum link m3u8 do YouTube encontrado!"
    exit 1
else
    echo "Link m3u8 do YouTube encontrado: $M3U8_URL"
fi

# Atualizar o link do YouTube no arquivo pt.m3u
sed -i "/https:\/\/manifest\.googlevideo\.com\/api\/manifest\/hls_variant\// c $M3U8_URL" pt.m3u

if grep -q "/https:\/\/manifest\.googlevideo\.com\/api\/manifest\/hls_variant\//" pt.m3u; then
  echo "Link da live do NATGEOWILD atualizado com sucesso."
else
  echo "Link da live do NATGEOWILD não atualizado."
fi

exit 0
