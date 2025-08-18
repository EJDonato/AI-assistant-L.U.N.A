import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_credentials():
    """
    Get the credentials for Google Calendar API.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the athorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
      creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
        creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open("token.json", "w") as token:
        token.write(creds.to_json())
    return creds

def get_incoming_events():
  """
  Get the next 10 events on google calendar.
  """
  creds = get_credentials()

  try:
    service = build("calendar", "v3", credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.now(tz=datetime.timezone.utc).isoformat()
    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
      print("No upcoming events found.")
      return "No upcoming events found."

    # Prints the start and name of the next 10 events
    events_list = []
    for event in events:
      start = event["start"].get("dateTime", event["start"].get("date"))
      summary = event['summary']

      events_list.append(f"{start} - {summary}")
      print(start, summary)
      
    return "\n".join(events_list) + "\nIf there are repeated events, do not repeat yourself."

  except HttpError as error:
    print(f"An error occurred: {error}")
    return f"An error occurred, unable to make request: {error}"
  

def create_event(event):
    """
    Create an event on google calendar.
    """
    creds = get_credentials()

    try:
      service = build("calendar", "v3", credentials=creds)
      add_event = service.events().insert(calendarId="primary", body=event).execute()
      link = add_event.get('htmlLink')

      print(f"Event successfully created: {link}")
      return f"Event successfully created: {link}"

    except HttpError as error:
      print(f"An error occurred: {error}")
      return f"An error occurred, unable to make request: {error}"

