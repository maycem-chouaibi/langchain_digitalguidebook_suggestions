# Indeply Project

A Flask-based AI tour guide application that provides personalized travel recommendations using LangChain and Groq.

## Features

- Personalized activity recommendations based on user preferences
- Multi-language support
- Integration with Google Search for up-to-date information
- Location-aware suggestions
- Accessibility considerations

## Project Structure

indeply/ ├── app.py # Main Flask application ├── langchainAgent/ │ ├── init.py │ ├── models.py # Pydantic models │ ├── prompts.py # System prompts │ └── tools.py # LangChain tools and agent └── requirements.txt

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

4. Creat .env file:
   GOOGLE_SEARCH_API_KEY="your_google_api_key"
   GOOGLE_SEARCH_CSE_ID="your_google_cse_id"
   GROQ_API_KEY="your_groq_api_key"

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
