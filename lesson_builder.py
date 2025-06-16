import json
from llm_utils import chat_with_gpt, generate_image
with open("prompts/system_prompt.txt", "r") as f:
    SYSTEM_PROMPT = f.read().strip()

    
def build_lesson(input_data):
    phoneme = input_data["phoneme"]
    vocab_words = input_data["words"]
    story = input_data["story"]

    # Step 1: Get phoneme intro
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Introduce the sound '{phoneme}' to a 6-year-old and explain how to say it."}
    ]
    phoneme_intro = chat_with_gpt(messages)

    # Step 2: Follow-up question
    messages.append({"role": "assistant", "content": phoneme_intro})
    messages.append({"role": "user", "content": "Ask the child a fun question to test their understanding of that sound."})
    follow_up = chat_with_gpt(messages)

    # Step 3: Generate images
    images = {}
    for word in vocab_words:
        image_prompt = f"Cartoon drawing of the word '{word}' for kids"
        images[word] = generate_image(image_prompt)

    # Step 4: Build lesson structure
    lesson = {
        "phoneme": phoneme,
        "intro_text": phoneme_intro,
        "follow_up_question": follow_up,
        "story": story,
        "vocab_words": [
            {"word": word, "image_url": images[word]} for word in vocab_words
        ]
    }

    with open("output/output_lesson.json", "w") as f:
        json.dump(lesson, f, indent=2)

    print("✅ Lesson generated at: output/output_lesson.json")
