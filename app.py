from flask import Flask, request, jsonify
from flask_cors import CORS
from langchainAgent.tools import google_search, create_model, create_agent, google_places
from pydantic import BaseModel, ValidationError, Field
import logging
from typing import List
from ocr.processIDs import process_ids
from db.crud import create_record
from db.models import User
from datetime import date
import json

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

class SuccessResponse(BaseModel):
    response: dict
    status: int = 200

@app.route('/guideBookData', methods=['POST'])
def guideBookData():
    try:
        request_data = request.get_json()
        if not request_data:
            raise ValidationError("Request body is required")
        
        validated_data = GuideBookRequest(**request_data)
        google_places_tool = google_places("Google Places", "Useful for searching places, restaurants, and activities online.")
        google_search_tool = google_search("Google Search", "Useful for searching stuff on the web.")
        model = create_model("llama3-70b-8192", 0, 2, 1024)
        tools = [google_places_tool, google_search_tool]
        
        results = create_agent(
                    model, 
                    tools, 
                    validated_data.age,
                    validated_data.destination,
                    validated_data.interests,
                    validated_data.gender,
                    validated_data.language
                )      
          
        return (SuccessResponse(response=results).model_dump()), 200
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify(ErrorResponse(error=str(e)).model_dump()), 400
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        return jsonify(ErrorResponse(error=str(e)).model_dump()), 500

@app.route('/processIDs', methods=['POST'])
def processIDs():
    try:
        file_path = request.get_json().get('file_path')
        results = process_ids(file_path)
        return (SuccessResponse(response=json.loads(results)).model_dump()), 200
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify(ErrorResponse(error=str(e)).model_dump()), 400
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        return jsonify(ErrorResponse(error=str(e)).model_dump()), 500

class UserRequest(BaseModel):
    dob: date = Field(..., gt=0, description="Age must be positive")
    first_name: str = Field(..., min_length=1)
    last_name: str = Field(..., min_length=1)
    email: str = Field(..., pattern=r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$", description="Must be a valid email address.")
    gender: str = Field(..., pattern="^(male|female|other)$")
    phone: str = Field(..., min_length=1)
    phone_ext: str = Field(..., min_length=1)

@app.route('/users/add', methods=['POST'])
def addUser():
    try:
        request_data = request.get_json()
        if not request_data:
            raise ValidationError("Request body is required")
        
        validated_data = UserRequest(**request_data)     
        
        results = create_record(User, 
                        dob=validated_data.dob,
                        first_name=validated_data.first_name,
                        last_name=validated_data.last_name,
                        email=validated_data.email,
                        gender=validated_data.gender,
                        phone=validated_data.phone,
                        phone_ext=validated_data.phone_ext)
      
        return jsonify(SuccessResponse(response={"results": results.id}).model_dump()), 200
    except ValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify(ErrorResponse(error=str(e)).model_dump()), 400
    except Exception as e:
        logger.error(f"Internal server error: {e}")
        return jsonify(ErrorResponse(error=str(e)).model_dump()), 500


if __name__ == '__main__':
    app.run(debug=True)