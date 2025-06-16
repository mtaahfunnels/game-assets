import os
import json
import requests
from dotenv import load_dotenv
import openai

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Step 1: Load lesson data
lesson_path = os.path.join("lessons", "lesson_d.json")
with open(lesson_path, "r", encoding="utf-8") as f:
    lesson = json.load(f)

words = lesson.get("words", lesson.get("data", []))
if not isinstance(words, list) or len(words) == 0:
    raise ValueError("No valid 'words' or 'data' found in lesson JSON.")

# Step 2: Prepare output directory
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

# Step 3: Generate up to 2 images
for index, item in enumerate(words[:2]):
    word_text = item.get("text", str(item)) if isinstance(item, dict) else str(item)
    prompt = f"An illustration of: {word_text}, kid-friendly, clear and simple, colorful"

    print(f"🎨 Generating image for: {word_text}")

    try:
        # Call OpenAI Image API (DALL·E 3)
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        image_url = response.data[0].url

        # Download the image
        image_data = requests.get(image_url).content
        image_path = os.path.join(output_dir, f"image_{index+1}.png")
        with open(image_path, "wb") as f:
            f.write(image_data)

        print(f"✅ Saved: {image_path}")

    except Exception as e:
        print(f"❌ Error generating image for '{word_text}': {e}")
