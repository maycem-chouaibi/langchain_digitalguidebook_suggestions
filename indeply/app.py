from flask import Flask, request, jsonify
from flask_cors import CORS
from langchainAgent.tools import google_search, create_model, create_agent
from pydantic import BaseModel, ValidationError, Field
import logging
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

class GuideBookRequest(BaseModel):
    age: int = Field(..., gt=0, description="Age must be positive")
    destination: str = Field(..., min_length=1)
    interests: List[str] = Field(..., min_items=1)
    gender: str = Field(..., pattern="^(male|female|other)$")
    language: str = Field(..., pattern="^(en|es|fr|de|it|pt|ru|zh|ja|ko|ar)$")

class ErrorResponse(BaseModel):
    error: str
    status: int = 500

@app.route('/guideBookData', methods=['POST'])
def guideBookData():
    try:
        request_data = request.get_json()
        if not request_data:
            raise ValidationError("Request body is required")
        
        validated_data = GuideBookRequest(**request_data)
        
        google_search_tool = google_search("Google Search", "Useful for searching stuff on the web.")
        model = create_model("llama3-70b-8192", 0, 2, 1024)
        tools = [google_search_tool]
        
        results = create_agent(
                    model, 
                    tools, 
                    validated_data.age,
                    validated_data.destination,
                    validated_data.interests,
                    validated_data.gender,
                    validated_data.language
                )      
          
        return jsonify(results)
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify(ErrorResponse(error=str(e)).model_dump()), 400
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        return jsonify(ErrorResponse(error=str(e)).model_dump()), 500

    
if __name__ == '__main__':
    app.run(debug=True)