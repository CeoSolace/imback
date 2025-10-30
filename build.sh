#!/bin/bash
# build.sh

echo "📦 Installing FFmpeg..."
apt-get update && apt-get install -y ffmpeg

echo "⬇️ Downloading Blender 3.6 LTS (headless)..."
BLENDER_VERSION="3.6.12"
wget https://download.blender.org/release/Blender${BLENDER_VERSION%.*}/blender-${BLENDER_VERSION}-linux-x64.tar.xz
tar -xf blender-${BLENDER_VERSION}-linux-x64.tar.xz
mv blender-${BLENDER_VERSION}-linux-x64 blender

echo "✅ Build complete"
