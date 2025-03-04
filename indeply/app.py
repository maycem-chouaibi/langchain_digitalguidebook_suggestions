from flask import Flask, request, jsonify
from langchainAgent.tools import google_search, create_model, create_agent
from pydantic import ValidationError
from langchainAgent.models import ErrorResponse

app = Flask(__name__)

@app.route('/guideBookData', methods=['POST'])
def guideBookData():
    try:
        age = request.json["age"]
        destination = request.json["destination"]
        interests = request.json["interests"]
        gender = request.json["gender"]
        
        google_search_tool = google_search("Google Search", "Useful for searching stuff on the web.")
        model = create_model("llama3-70b-8192", 0, 2, 1024)
        tools = [google_search_tool]
        results = create_agent(model, tools, age, destination, interests, gender)
        return results
    except ValidationError as e:
        return jsonify(ErrorResponse(error=str(e)).model_dump_json()), 400
    except Exception as e:
        return jsonify(ErrorResponse(error=str(e)).model_dump_json()), 500

    
if __name__ == '__main__':
    app.run(debug=True)