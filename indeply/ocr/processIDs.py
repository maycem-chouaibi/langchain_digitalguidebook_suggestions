import base64
import os
from dotenv import load_dotenv
from together import Together
from .prompts import SYSTEM_PROMPT, SYSTEM_PROMPT_2

load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def process_ids(file_path, model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo"):
    
    together = Together(api_key=TOGETHER_API_KEY)
    return get_info(together, model, file_path)

def get_info(together, vision_llm, file_path):
     
    final_image_url = file_path if is_remote_file(file_path) else f"data:image/jpeg;base64,{encode_image(file_path)}"
    
    output = together.chat.completions.create(
        model=vision_llm,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": SYSTEM_PROMPT},
                    {"type": "image_url", "image_url": {"url": final_image_url}},
                    {"type": "text", "text": SYSTEM_PROMPT_2},
                ],
            }
        ]
    ).choices[0].message.content
    return output[output.index("{"):]

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def is_remote_file(file_path):
    return file_path.startswith("http://") or file_path.startswith("https://")
