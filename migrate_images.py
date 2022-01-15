import os
from pathlib import Path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "images")

for filename in os.listdir(IMAGES_DIR):
  folder = os.path.splitext(filename)[0].split('-')[0]
  if not os.path.exists(f"{BASE_DIR}/dataset/{folder}"):
    os.makedirs(f"{BASE_DIR}/dataset/{folder}")
  print(f"movendo {IMAGES_DIR}/{filename} -> {BASE_DIR}/dataset/{folder}/{filename}")
  Path(f"{IMAGES_DIR}/{filename}").rename(f"{BASE_DIR}/dataset/{folder}/{filename}")