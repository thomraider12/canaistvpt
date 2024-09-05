#!/bin/bash

sed -i "/live_tvi\/live_tvi/ c https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" pt.m3u
if grep -q "live_tvi\/live_tvi" pt.m3u; then
  echo "Link da TVI atualizado."
else
  echo "Link da TVI não atualizado."
fi

sed -i "/live_cnn/ c https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" pt.m3u
if grep -q "live_cnn" pt.m3u; then
  echo "Link da CNN Portugal atualizado com sucesso."
else
  echo "Link da CNN Portugal não atualizado."
fi

exit 0