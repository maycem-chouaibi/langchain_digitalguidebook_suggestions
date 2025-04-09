import json
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import SYSTEM_PROMPT, SYSTEM_PROMPT_2
from consts import API_ENDPOINTS
from google.genai.types import GenerateContentConfig


load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

def clean_data(data):
    client = genai.Client(api_key = GEMINI_API_KEY)
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        config=GenerateContentConfig(system_instruction=[SYSTEM_PROMPT, SYSTEM_PROMPT_2]),
        contents=data
    )
    
    print(response.text)
    return json.loads(response.text.replace("```json", "").replace("```", ""))

def parse_data(summary_file):
    with open(summary_file, "r") as s:
        summary = json.loads(s.read())

    single_listing_results = []

    files = [f"{listing["id"]}.json" for listing in summary.get("listings", [])]
    for file in files:
        with open(file, "r+") as f:
            contents = f.read()
            json_contents = json.loads(contents)
            for section_name, section in API_ENDPOINTS.items():
                section_data = json_contents["data"][section_name]
                single_listing_results.append(clean_data(str(section_data)))
            f.seek(0)
            f.write(single_listing_results)
            f.truncate()

    return


