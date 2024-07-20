#!/bin/bash

# TVI - update the stream URL of TVI
sed -i "/live_tvi\/live_tvi/ c https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" pt.m3u
if grep -q "live_tvi\/live_tvi" pt.m3u; then
  echo "TVI URL updated successfully"
else
  echo "Failed to update TVI URL"
fi

# CNN Portugal - update the stream URL of CNN Portugal
sed -i "/live_cnn/ c https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)/" pt.m3u
if grep -q "live_cnn" pt.m3u; then
  echo "CNN URL updated successfully"
else
  echo "Failed to update CNN URL"
fi

exit 0
