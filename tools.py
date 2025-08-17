import logging
from livekit.agents import function_tool, RunContext
from langchain_community.tools import DuckDuckGoSearchRun
from typing import Optional

from services.google_calendar import get_incoming_events, create_event

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


# Google Calendar Tools
@function_tool()
async def check_incoming_schedule(
    context: RunContext
    ) -> str:
    """
    Check the user's incoming schedule from Google Calendar.
    """
    return get_incoming_events()

@function_tool()
async def create_event_on_calendar(
    context: RunContext, 
    title: str,
    location: str,
    description: str,
    start: str,
    end: str,
    recurrence: Optional[str] = None,
    ) -> str:
    """
    Create an event on Google Calendar.

    Args:
        title (str): The title of the event.
        location (str): The location of the event.
        description (str): A short description of the event.
        start (str): The start time and date of the event in this format: "2025-10-01T10:00:00+8:00"
        end (str): The end time and date of the event in this format: "2025-10-01T10:00:00+8:00".
        recurrence (Optional[str]): Recurrence rule for the event, example: "RRULE:FREQ=DAILY;COUNT=2"
    """
    try:
        event = {
            "summary": title,
            "location": location,
            "description": description,
            "colorId": 5,
            "start": {"dateTime": start, "timeZone": "Asia/Manila"},
            "end": {"dateTime": end, "timeZone": "Asia/Manila"},
        }
        if recurrence:
            event["recurrence"] = [recurrence]

        result = create_event(event)
        logging.info(f"Event created: {result}")
        return result
    except Exception as e:
        logging.error(f"Error creating event: {e}")
        return f"An error occurred while creating the event. Due to {e}."

