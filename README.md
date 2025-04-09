# Indeply Project

A Flask-based AI tour guide application that provides personalized travel recommendations using LangChain and Groq.
This project uses PostgreSQL for the DB.
This project is UV friendly.

## Features

- Personalized activity recommendations based on user preferences
- Multi-language support
- Integration with Google Search for up-to-date information
- Location-aware suggestions
- Accessibility considerations

## Setup

1. Clone the repository
2. Create and activate virtual environment:

```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create .env file:

   ```bash
   LANGSMITH_API_KEY="your_values"
   LANGSMITH_TRACING="your_values"
   LANGSMITH_ENDPOINT="your_values"
   LANGSMITH_PROJECT="your_values"
   GOOGLE_SEARCH_API_KEY="your_values"
   GOOGLE_SEARCH_CSE_ID="your_values"
   GROQ_API_KEY="your_values"
   TOGETHER_API_KEY="your_values"
   TOGETHER_CLIENT_ID="your_values"
   ```

   # HUGGING_FACE_TOKEN="your_values"

   ```bash
   GPLACES_API_KEY="your_values"
   GOOGLE_ROUTES_API_KEY="your_values"
   OPENAI_API_KEY="your_values"
   POSTGRES_PWD="your_values"
   POSTGRES_DB_NAME="your_values"
   POSTGRES_USERNAME="your_values"
   POSTGRES_PORT = your_values
   POSTGRES_HOST="your_values"
   POSTGRES_DRIVER="your_values"
   ```

5. Run the app:

```bash
flask run
```

## API Usage:

### POST /guideBookData

Create personalized travel recommendations.

Request body example:

```bash
{
    "age": 25,
    "destination": "Paris",
    "interests": ["art", "food"],
    "gender": "female",
    "language": "en"
}
```

Expected response format:

```bash
{
    "status": "success",
    "data": {
        "activities": [
            {
                "title": "Activity name",
                "category": "Category type",
                "description": "Brief description",
                "location": {
                    "address": "Full address",
                    "lat": 0.0,
                    "long": 0.0
                },
                "duration": "Duration",
                "best_time": "Best time to visit",
                "price_range": 1-5,
                "rating": 1-5,
                "accessibility": "Accessibility info",
                "link": "URL"
            }
        ]
    }
}
```
