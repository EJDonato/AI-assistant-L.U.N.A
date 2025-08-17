import logging
from livekit.agents import function_tool, RunContext
from langchain_community.tools import DuckDuckGoSearchRun

from services.google_calendar import get_incoming_events

@function_tool()
async def search_web(
    context: RunContext, 
    query: str) -> str:
    """
    Search the web using DuckDuckGo.
    """
    try:
        results = DuckDuckGoSearchRun().run(tool_input=query)
        logging.info(f"Search results for '{query}': {results}")
        return results
    except Exception as e:
        logging.error(f"Error searching the web for '{query}': {e}")
        return f"An error occurred while searching the web for '{query}'. Due to {e}."


@function_tool()
async def check_incoming_schedule(
    context: RunContext
    ) -> str:
    """
    Check the user's incoming schedule from Google Calendar.
    """
    return get_incoming_events()

