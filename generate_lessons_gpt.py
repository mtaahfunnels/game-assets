import os
import json
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

PHONEMES = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "p", "qu", "r", "s", "t", "u", "v", "w", "x", "y", "z",
    "sh", "ch", "th", "wh", "ee", "ai", "ou", "ow", "ar", "or", "er",
    "oy", "oi", "igh", "ue", "air", "ear"
]

SYSTEM_PROMPT = "You are a creative early reading lesson designer for kids aged 4–7."

# ========== Prompt Template ==========
def lesson_prompt(phoneme):
    return f"""
Create a JSON lesson for the phoneme '{phoneme}'. It should contain:
1. A short 2-3 sentence story that uses '{phoneme}' multiple times.
2. A list of 2 image descriptions, one for each sentence.
3. 2 multiple-choice comprehension questions with 3 choices each and the correct answer.
Return it as valid JSON in this format:
{{
  "id": "{phoneme}",
  "story_text": ["...", "..."],
  "story_images": ["...", "..."],
  "questions": [
    {{"question": "?", "choices": ["...", "...", "..."], "answer": "..."}},
    {{"question": "?", "choices": ["...", "...", "..."], "answer": "..."}}
  ]
}}
"""

# ========== Generation Function ==========
def generate_lesson(phoneme):
    print(f"🧠 Generating lesson for: {phoneme}")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": lesson_prompt(phoneme)}
        ]
    )

    text = response.choices[0].message.content.strip()

    # ✅ Remove ```json block if present
    if text.startswith("```"):
        text = text.split("```")[1].strip()
        if text.startswith("json"):
            text = text[len("json"):].strip()

    try:
        lesson = json.loads(text)
        out_path = f"lessons/lesson_{phoneme}.json"
        os.makedirs("lessons", exist_ok=True)
        with open(out_path, "w") as f:
            json.dump(lesson, f, indent=2)
        print(f"✅ Saved: {out_path}")
    except Exception as e:
        print(f"❌ Failed to parse lesson for {phoneme}:", e)
        print("Raw output:\n", text)


# ========== Batch Generator ==========
if __name__ == "__main__":
    os.makedirs("lessons", exist_ok=True)
    for p in PHONEMES:
        generate_lesson(p)
        time.sleep(3)  # Avoid hitting rate limits
