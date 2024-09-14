#!/bin/bash

file1="m3u8s/cnnpt.m3u8"
file2="m3u8s/tvi.m3u8"

for file in "$file1" "$file2"; do
  sed -i "s#wmsAuthSign=[^&]*#wmsAuthSign=$(wget -qO- https://services.iol.pt/matrix?userId -o /dev/null)#g" "$file"
done
exit 0