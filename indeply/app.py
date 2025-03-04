from flask import Flask, request, jsonify
from langchainAgent.tools import google_search, create_model, create_agent

app = Flask(__name__)

@app.route('/guideBookData', methods=['POST'])
def guideBookData():
    try:
        prompt = request.json['prompt']
        google_search_tool = google_search("Google Search", "Useful for searching stuff on the web.")
        model = create_model("llama3-70b-8192", 0, 2, 1024)
        tools = [google_search_tool]
        return create_agent(model, tools, prompt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)