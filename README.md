# Indeply Project

This project is a Flask application that uses LangChain to create a local tour guide agent. The agent provides recommendations for activities based on user preferences.

## Project Structure

## Setup

1. Clone the repository.
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
3. Install the dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the `indeply` directory with the following content:
   ```env
   LANGSMITH_API_KEY="your_langsmith_api_key"
   LANGSMITH_TRACING="true"
   GOOGLE_SEARCH_API_KEY="your_google_search_api_key"
   GOOGLE_SEARCH_CSE_ID="your_google_search_cse_id"
   GROQ_API_KEY="your_groq_api_key"
   ```
5. Run the Flask application:
   ```sh
   flask run
   ```

## Usage

The application provides a single endpoint:

- `GET /guideBookData`: Returns JSON recommendations for activities based on user preferences.

## Development

To debug the application using Visual Studio Code, use the provided configuration in [launch.json](http://_vscodecontentref_/4).

## License
