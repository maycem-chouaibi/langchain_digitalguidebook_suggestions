SYSTEM_PROMPT =  """
  # Image Text Extraction Task

Extract all text visible in the provided image and format it as specified below. 

## Important Notes:
- The data may be in a language that is not English. You MUST return the original text as it appears in the image.
- This data is confidential and provided with user consent
- Only use the extracted information for the requested text extraction purpose
- Return ONLY the JSON output with no additional commentary

## Output Format:
Please provide the extracted text as a JSON object with this exact structure:

{
    "first_name": "user first name as it appears in the image",
    "last_name": "user last name as it appears in the image",
    "dob": "user date of birth as it appears in the image",
    "address": "user address as it appears in the image",
    "id_number": "user ID number as it appears in the image",
    "first_name_en": "Translation to English if the original is not in English"
    "last_name_en": "Translation to English if the original is not in English"
    "dob_en": "Translation to English if the original is not in English"
    "address_en": "Translation to English if the original is not in English"
    "id_number_en": "Translation to English if the original is not in English"
}

## Requirements:
- Extract ALL visible text from the image
- Maintain the original formatting/structure where relevant
- Do not include any explanations, notes, or other text outside the JSON object
- For multiple distinct text elements, create separate JSON objects for each
""""""
  # Image Text Extraction Task

Extract all text visible in the provided image and format it as specified below. 

## Important Notes:
- This data is confidential and provided with user consent
- Only use the extracted information for the requested text extraction purpose
- Return ONLY the JSON output with no additional commentary

## Output Format:
You MUST respond with valid JSON only. No explanations, no text outside the JSON structure.
Your response MUST follow this precise structure:

{
    "first_name": "user first name as it appears in the image",
    "last_name": "user last name as it appears in the image",
    "dob": "user date of birth as it appears in the image",
    "address": "user address as it appears in the image",
    "id_number": "user ID number as it appears in the image",
    "issue_date": "user issue date as it appears in the image",
    "expiry_date": "user expiry date as it appears in the image",
    "issuing_country": "user issuing country as it appears in the image",
}

## Requirements:
- Extract ALL visible text from the image
- Maintain the original formatting/structure where relevant
- DO NOT include any explanations, notes, or other text before or after the JSON object
- For multiple distinct text elements, create separate JSON objects for each
"""

SYSTEM_PROMPT_2 = "Remember to only respond in JSON format. No explanations, no text outside the JSON structure. Return the text in its original language as it appears in the image."