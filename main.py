from lesson_builder import build_lesson

input_data = {
    "phoneme": "d",
    "words": ["dog", "dig", "dad"],
    "story": "Dad has a dog. The dog dug. Dad did not mind."
}

if __name__ == "__main__":
    build_lesson(input_data)
