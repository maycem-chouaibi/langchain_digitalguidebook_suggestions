from langchain_google_community import GoogleSearchAPIWrapper, GooglePlacesAPIWrapper
from langchain_core.tools import Tool
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage
from langgraph.prebuilt import create_react_agent
from langchain_community.utilities import GoogleSearchAPIWrapper
import os
from dotenv import load_dotenv
import json
from .prompts import SYSTEM_PROMPT_1, SYSTEM_PROMPT_2, generate_human_prompt
from .models import ErrorResponse, AgentResponse, Activity
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_CSE_ID = os.getenv("GOOGLE_SEARCH_CSE_ID")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GPLACES_API_KEY = os.getenv("GPLACES_API_KEY")

if not all([GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_CSE_ID, GROQ_API_KEY]):
    raise ValueError("Missing required environment variables")

def google_places(name: str, description: str) -> Tool:
    try:
        search = GooglePlacesAPIWrapper(gplaces_api_key=GPLACES_API_KEY)

        google_places_tool = Tool(
            name=name,
            description=description,
            func=search.run
        )
        return google_places_tool
    except Exception as e:
        logger.error(f"Error creating Google Places tool: {e}")
        raise

def google_search(name: str, description: str) -> Tool:
    try:
        search = GoogleSearchAPIWrapper(search_engine="google", google_api_key=GOOGLE_SEARCH_API_KEY, google_cse_id=GOOGLE_SEARCH_CSE_ID )

        google_search_tool = Tool(
            name=name,
            description=description,
            func=search.run
        )
        return google_search_tool
    except Exception as e:
        logger.error(f"Error creating Google Search tool: {e}")
        raise        

def create_model(name: str, temperature: int, max_retries: int, max_tokens: int) -> ChatGroq:
    try:
        model = ChatGroq(model=name, temperature=temperature, max_retries=max_retries, max_tokens=max_tokens, api_key=GROQ_API_KEY)
        return model
    except Exception as e:
        logger.error(f"Error creating model: {e}")
        raise

def create_agent(model: ChatGroq, tools: list, age: int, destination: str, interests: list, gender: str, language: str) -> AgentResponse:
    try: 
        agent_executor = create_react_agent(model, tools)
        
        response = agent_executor.invoke(
        {   
        "messages": [   
            SystemMessage(content=SYSTEM_PROMPT_1),
            HumanMessage(content=generate_human_prompt(age, destination, interests, gender, language)),
            SystemMessage(content=SYSTEM_PROMPT_2),
        ]}
        ) 
        if "messages" not in response:
            raise ValueError("Response does not contain 'messages' key")
        
        response_content = response["messages"][-1].content
        logger.info(f"Agent response: {response_content}")
            
        results = json.loads(response_content)
        agent_response = AgentResponse(
            activities=[Activity(**activity) for activity in results["activities"]]
        )
            
        return agent_response.model_dump(mode='json')
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        return ErrorResponse(error=f"Invalid response format: {str(e)}").model_dump(mode='json')
        
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        return ErrorResponse(error=str(e)).model_dump(mode='json')