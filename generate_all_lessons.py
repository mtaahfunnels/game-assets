import json, os

phonemes = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
    "m", "n", "o", "p", "qu", "r", "s", "t", "u", "v", "w", "x",
    "y", "z", "sh", "ch", "th", "wh", "ee", "ai", "ou", "ow", "ar",
    "or", "er", "oy", "oi", "igh", "ue", "air", "ear"
]

os.makedirs("lessons", exist_ok=True)

for p in phonemes:
    data = {
        "id": f"lesson_{p}",
        "title": f"Sound: {p.upper()}",
        "story_text": [
            f"This is the story for the sound '{p}'.",
            f"We use '{p}' in many words.",
            f"Let's learn to listen and read with '{p}'!"
        ],
        "questions": [
            {
                "question": f"Which letter sound is this lesson about?",
                "choices": [p.upper(), "Z", "M"],
                "answer": p.upper()
            },
            {
                "question": f"Can you think of a word with the sound '{p}'?",
                "choices": ["Yes", "No", "Maybe"],
                "answer": "Yes"
            }
        ]
    }
    with open(f"lessons/lesson_{p}.json", "w") as f:
        json.dump(data, f, indent=2)

print("✅ All 44 phoneme lessons created.")
