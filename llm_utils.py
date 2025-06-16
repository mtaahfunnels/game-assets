# llm_utils.py

from openai import OpenAI
from config import OPENAI_API_KEY, IMAGE_SIZE, GPT_MODEL

# Initialize OpenAI client with your API key
client = OpenAI(api_key=OPENAI_API_KEY)

# PART 1 – Chat with GPT
def chat_with_gpt(messages):
    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=messages
    )
    return response.choices[0].message.content

# PART 2 – Generate Image using DALL·E
def generate_image(prompt):
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size=IMAGE_SIZE,
        response_format="url"
    )
    return response.data[0].url
