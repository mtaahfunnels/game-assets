# generate_2_images.py (Refactored for GitHub upload and JSON auto-update)

import openai
import os
import json
import subprocess
from pathlib import Path

# === CONFIG ===
LESSON_FILE = "lessons/lesson_d.json"
IMAGES_DIR = "assets/images"
GITHUB_REPO_URL = "https://github.com/mtaahfunnels/game-assets"
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure this is set in your environment

# === PREP ===
os.makedirs(IMAGES_DIR, exist_ok=True)
lesson_path = Path(LESSON_FILE)

with open(lesson_path, "r", encoding="utf-8") as f:
    lesson_data = json.load(f)

# === IMAGE GENERATION ===
for i, item in enumerate(lesson_data):
    prompt = f"An illustration of: {item['text']}"
    print(f"\U0001f3a8 Generating image for line {i}: {prompt}")
    response = openai.images.generate(prompt=prompt, n=1, size="1024x1024")
    image_url = response.data[0].url
    
    image_name = f"lesson_d_{i}.png"
    image_path = Path(IMAGES_DIR) / image_name

    # Download image locally
    os.system(f"curl -o {image_path} {image_url}")
    print(f"✅ Saved: {image_path}")

    # Update JSON with GitHub raw URL reference
    lesson_data[i]["image"] = f"https://raw.githubusercontent.com/mtaahfunnels/game-assets/main/{IMAGES_DIR}/{image_name}"

# === SAVE UPDATED JSON ===
with open(lesson_path, "w", encoding="utf-8") as f:
    json.dump(lesson_data, f, indent=2)
print("✅ lesson_d.json updated with GitHub raw URLs")

# === GIT UPLOAD ===
print("\U0001f4e4 Uploading to GitHub...")
os.system("git add .")
os.system("git commit -m 'Add generated images and update lesson_d.json'")
os.system("git push origin main")
print("✅ GitHub upload complete.")
