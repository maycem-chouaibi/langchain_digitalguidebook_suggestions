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
from .systemPrompts import SYSTEM_PROMPT_1, SYSTEM_PROMPT_2

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

def create_agent(model, tools, prompt):
    agent_executor = create_react_agent(model, tools)
    
    response = agent_executor.invoke(
    {   
    "messages": [   
        SystemMessage(content=SYSTEM_PROMPT_1),
        HumanMessage(content=prompt),
        SystemMessage(content=SYSTEM_PROMPT_2),
    ],},
    ) 
    results:json = response["messages"][-1].content
    return results