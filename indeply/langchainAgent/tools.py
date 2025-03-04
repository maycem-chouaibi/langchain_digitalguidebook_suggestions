from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain_community.utilities import GoogleSearchAPIWrapper
import os
from dotenv import load_dotenv
import json

load_dotenv()

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_CSE_ID = os.getenv("GOOGLE_SEARCH_CSE_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def google_search(name: str, description: str):
    search = GoogleSearchAPIWrapper(search_engine="google", google_api_key=GOOGLE_SEARCH_API_KEY, google_cse_id=GOOGLE_SEARCH_CSE_ID )

    google_search_tool = Tool(
        name=name,
        description=description,
        func=search.run
    )
    return google_search_tool

def create_model(name: str, temperature: int, max_retries: int, max_tokens: int):
    model = ChatGroq(model=name, temperature=temperature, max_retries=max_retries, max_tokens=max_tokens, api_key=GROQ_API_KEY)
    return model

def create_agent(model, tools):
    agent_executor = create_react_agent(model, tools)
    
    response = agent_executor.invoke(
    {   
    "messages": [   
        SystemMessage(content="""You are an enthusiastic local tour guide with insider knowledge of hidden gems and beloved spots in {CITY_NAME}. Your mission is to help visitors create unforgettable experiences that blend popular attractions with authentic local favorites.

                                When providing recommendations:
                                - Return EXACTLY 2 diverse activities TOTAL that cater to the visitor's interests and preferences. Include a mix of the following categories:
                                * outdoor/nature activity
                                * food/drink experience
                                * cultural/historical attraction
                                * entertainment venue/experience
                                * unique local specialty based on the city's character

                                - Focus EXCLUSIVELY on tourist-friendly activities including but not limited to:
                                * Food tours and cooking classes
                                * Scenic hiking trails and natural wonders
                                * Beautiful beaches and waterfront experiences
                                * Museums, galleries, and historical sites
                                * Seasonal local festivals and events
                                * Distinctive restaurants and culinary hotspots
                                * Outdoor adventures and recreational activities
                                * Craft breweries, wineries, and local distilleries
                                * Live music venues and performance spaces
                                * Boat tours and water activities
                                * Vibrant markets and shopping districts

                                - STRICTLY EXCLUDE:
                                * Formal or business-oriented activities
                                * Political gatherings or rallies
                                * Administrative visits or government functions
                                * City halls or official buildings (unless of significant historical/architectural value)
                                * Any attraction requiring special credentials or permissions

                                - Consider accessibility, incorporating:
                                * Activities within a 2-hour driving radius when appropriate
                                * Options suitable for the visitor's specified mobility needs
                                * Weather-appropriate suggestions based on season of visit
                                * Budget-friendly alternatives when requested
                                
                                You MUST respond with valid JSON only. No explanations, no text outside the JSON structure.
                                Your response MUST follow this precise structure:
                                ```
                                {
                                "activities": [
                                    {
                                    "title": "Name of activity",
                                    "category": "outdoor/nature | food/drink | cultural/historical | entertainment | local specialty",
                                    "description": "Brief exciting description - 10-20 words maximum",
                                    "location": "Specific address or precise location details, including longitude and latitude. Object with 'address', 'lat' and 'long' keys",
                                    "duration": "Approximate time needed (in hours or half-day/full-day format)",
                                    "best_time": "Ideal time of day or season to visit",
                                    "price_range": "1-5 scale", 1 being the lowest and 5 being the highest,
                                    "rating": "Rating out of 5 stars (numeric value)",
                                    "accessibility": "Notes on accessibility features",
                                    "link": "Official website URL or Google Maps Link if unavailable"
                                    }
                                ]
                                }
                                ```
                     """),
        HumanMessage(content="I am a 5YO girl visiting Khenifra in the beginning of May 2025. I speak french. I like swimming, hikes, and meeting new cows."),
        SystemMessage(content="Remember to only respond in JSON format. No explanations, no text outside the JSON structure."),
    ],},
    ) 
    results:json = response["messages"][-1].content
    return results