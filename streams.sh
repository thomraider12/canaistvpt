#!/bin/bash
# Thanks to LITUATUI user on github

sed -i "/live_cnn/ c  https://video-auth7.iol.pt/live_cnn/live_cnn/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)" pt.m3u

sed -i "/live_tvi\/live_tvi/ c  https://video-auth6.iol.pt/live_tvi/live_tvi/playlist.m3u8?wmsAuthSign=$(wget https://services.iol.pt/matrix?userId= -o /dev/null -O -)" pt.m3u

exit 0
