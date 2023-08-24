# Refer to the Python quickstart on how to setup the environment:
# https://developers.google.com/calendar/quickstart/python
# Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# stored credentials.
from __future__ import print_function
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

credential_path = 'myapp/credentials/credentials.json'
token_path = 'myapp/credentials/token.json'

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_service():
  """Shows basic usage of the Google Calendar API.
  Prints the start and name of the next 10 events on the user's calendar.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists(token_path):
    creds = Credentials.from_authorized_user_file(token_path, SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(credential_path, SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_path, 'w') as token:
      token.write(creds.to_json())

  try:
    service = build('calendar', 'v3', credentials=creds)
    return service
  except HttpError as error:
    print('An error occurred: %s' % error)

def create_event(start_time:datetime.datetime, end_time: datetime.datetime, summary: str, description: str, attendees: dict):
  """
  start_time : datetime,
  end_time : datetime,
  summary : str,
  description : str,
  attendees : dict(doctor_email=str, patient_email=str),
  """
  start_time = start_time.strftime("%Y-%m-%dT%H:%M:%S+05:30")
  end_time = end_time.strftime("%Y-%m-%dT%H:%M:%S+05:30")
  service = get_service()
  event = {
    'summary': summary,
    # 'location': 'Dera Bassi, Mohali, Punjab',
    'description': description,
    'start': {'dateTime': start_time,'timeZone': 'Asia/Kolkata',},
    'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata',},
    # 'recurrence': ['RRULE:FREQ=DAILY;COUNT=2'],
    'attendees': [{'email': attendees.get('doctor_email')}, {'email': attendees.get('patient_email')}, ],
    'extendedProperties': {
      'private': {
        attendees.get('doctor_email'): 'Doctor',
        attendees.get('patient_email'): 'Patient',
      },
    },
    'sendNotifications':True,
    'sendUpdates': 'all',
    'reminders': {
      'useDefault': False,
      'overrides': [
        {'method': 'email', 'minutes': 24 * 60},
        {'method': 'popup', 'minutes': 10},
      ],
    },
  }
  event = service.events().insert(calendarId='primary', body=event).execute()
  print('Event created: %s' % (event.get('htmlLink')))

def get_events():
  service = get_service()
  now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
  print('Getting the upcoming 10 events')
  events_result = service.events().list(calendarId='primary', timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
  
  events = events_result.get('items', [])

  if not events:
    print('No upcoming events found.')
    return 
  # Prints the start and name of the next 10 events
  for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(start, event['summary'])
  
if __name__ == "__main__":
  create_event()
