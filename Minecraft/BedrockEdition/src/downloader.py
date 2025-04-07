"""
Copyright (c) 2021 Donverse.net All rights reserved.
DO NOT CHANGE THIS FILE

* If you use this file, you must include the copyright notice
* Put this file in /app folder
"""
# Modules
from html.parser import HTMLParser
import os
import shutil
import requests
import zipfile

# Variables
LINUX_BINS = []

SERVER_DIR = "bedrock_server"
DOWNLOAD_DIR = "downloads"
UNZIP_DIR = "unzip"
TEMP_DIR = "temp"

FOLDER_TARGETS = [
    "/bedrock_server/worlds",
    "/bedrock_server/resource_packs",
    "/bedrock_server/behavior_packs",
    "/bedrock_server/config",
]
FILE_TARGETS = [
    "/bedrock_server/server.properties",
    "/bedrock_server/permissions.json",
    "/bedrock_server/allowlist.json",
]

# Create directory
if not os.path.exists(SERVER_DIR):
    os.makedirs(SERVER_DIR)

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

if not os.path.exists(UNZIP_DIR):
    os.makedirs(UNZIP_DIR)

if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Class
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href" and value.endswith(".zip") and "bin-linux" in value:
                    LINUX_BINS.append(value)

# Visit website
url = 'https://www.minecraft.net/en-us/download/server/bedrock'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

try:
    print("[INFO] Seeing https://www.minecraft.net/en-us/download/server/bedrock")

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    html_content = response.text

    print("[INFO] Finding download links...")

    parser = MyHTMLParser()
    parser.feed(response.text)

    for bin in LINUX_BINS:
        print(bin)

    print("[INFO] Downloading...")

    # download zip not preview
    url = LINUX_BINS[0]
    response = requests.get(url, headers=headers, stream=True)
    response.raise_for_status()

    with open(f"{DOWNLOAD_DIR}/bedrock_server.zip", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"[INFO] Download complete! In {DOWNLOAD_DIR}")

except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")

# Unzip -> UNZIP_DIR
print("[INFO] Unzipping...")

with zipfile.ZipFile(f"{DOWNLOAD_DIR}/bedrock_server.zip", "r") as zip_ref:
    zip_ref.extractall(f"{UNZIP_DIR}")

print("[INFO] Unzip complete!")

# If already exist server binary, move data to temp
if os.path.exists(f"{SERVER_DIR}/bedrock_server"):
    print("[INFO] Move data to temp...")

    for target in FOLDER_TARGETS:
        if os.path.exists(target):
            os.makedirs(f"{TEMP_DIR}{target}", exist_ok=True)
            os.replace(target, f"{TEMP_DIR}{target}")

    for target in FILE_TARGETS:
        if os.path.exists(target):
            os.makedirs(f"{TEMP_DIR}{target}", exist_ok=True)
            os.replace(target, f"{TEMP_DIR}{target}")

    print("[INFO] Move data to temp complete!")
else:
    print("[INFO] Server binary not exist!")

# Replace server binary
print("[INFO] Replace server binary...")

for item in os.listdir(f"{SERVER_DIR}"):
    if os.path.isdir(f"{SERVER_DIR}/{item}"):

        print(f"[INFO] Item {item} removing...")
        shutil.rmtree(f"{SERVER_DIR}/{item}")
        print(f"[INFO] Item {item} removed!")

    elif os.path.isfile(f"{SERVER_DIR}/{item}"):

        print(f"[INFO] Item {item} removing...")
        os.remove(f"{SERVER_DIR}/{item}")
        print(f"[INFO] Item {item} removed!")

    else:
        print(f"[INFO] Item {item} can not be remove!")
        continue

for file in os.listdir(f"{UNZIP_DIR}"):
    print("[INFO] Copying " + file)
    os.replace(f"{UNZIP_DIR}/{file}", f"{SERVER_DIR}/{file}")

print("[INFO] Replace server binary complete!")

# Move data from temp to server
print("[INFO] Move data from temp to server...")

for target in FOLDER_TARGETS:
    if os.path.exists(f"{TEMP_DIR}{target}"):
        os.makedirs(target, exist_ok=True)
        os.replace(f"{TEMP_DIR}{target}", target)

for target in FILE_TARGETS:
    if os.path.exists(f"{TEMP_DIR}{target}"):
        os.makedirs(target, exist_ok=True)
        os.replace(f"{TEMP_DIR}{target}", target)

print("[INFO] Move data from temp to server complete!")

# Remove temp
print("[INFO] Remove temp...")

os.rmdir(f"{TEMP_DIR}")

print("[INFO] Remove temp complete!")

# Remove zip
print("[INFO] Remove zip...")

os.remove(f"{DOWNLOAD_DIR}/bedrock_server.zip")

print("[INFO] Remove zip complete!")

print("[INFO] Done!")
