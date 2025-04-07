#!/bin/bash

# ---------------------------
# Downloader
# ---------------------------
cd /app
pip3 install -r requirements.txt
python3 downloader.py

# ---------------------------
# Server
# ---------------------------
cd /app/bedrock_server
chmod +x ./bedrock_server
./bedrock_server
