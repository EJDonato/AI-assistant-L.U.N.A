import logging
from livekit.agents import function_tool, RunContext
from langchain_community.tools import DuckDuckGoSearchRun
from typing import Optional

from services.google_calendar import get_incoming_events, create_event
from services.notion import get_pages

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


# Notion Tools
@function_tool()
async def check_tasks():
    """
    Check tasks from Notion.
    """
    try:
        tasks = get_pages()

        if isinstance(tasks, str):
            logging.info(f"No tasks found: {tasks}")
            return tasks
        
        logging.info(f"Tasks retrieved")
        logging.info("\n".join(tasks))
        return "\n".join(tasks)
    except Exception as e:
        logging.error(f"Error checking tasks: {e}")
        return f"An error occurred while checking tasks. Due to {e}."
    
@function_tool()
async def create_task(
    context: RunContext, 
    task: str, 
    deadline: str
    ) -> str:
    """
    Create a task in Notion.

    Args:
        task (str): The task short title.
        deadline (str): The deadline for the task in this format: "2025-12-30"
    """
    try:
        result = create_task(task, deadline)
        if result.status_code != 200:
            logging.error(f"Failed to create task: {result.text}")
            return f"Failed to create task: {result.text}"
        logging.info(f"Task created: {result.json()}")
        return f"Task '{task}' created successfully with deadline {deadline}."
    except Exception as e:
        logging.error(f"Error creating task: {e}")
        return f"An error occurred while creating the task. Due to {e}."