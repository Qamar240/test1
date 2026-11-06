#!/bin/bash
# renders BridgeLite (675 frames @10fps) in 9 chunks so progress survives interruptions
cd ~/shorts; export TEMP=$HOME/rtmp TMP=$HOME/rtmp
for i in $(seq 0 8); do a=$((i*75)); b=$((a+74)); o=out/bridge/lite_$i.mp4
  [ -s $o ] && continue
  npx remotion render src/index.ts BridgeLite $o --frames=$a-$b --scale 0.5 --props='{"post":{"dpr":0.5}}' --gl=swangle --browser-executable=/opt/pw-browsers/chromium --concurrency=2 --timeout=900000 --muted > out/bridge/lite_$i.log 2>&1 || echo "chunk $i FAILED"
  echo "chunk $i done $(date +%T)"
done
