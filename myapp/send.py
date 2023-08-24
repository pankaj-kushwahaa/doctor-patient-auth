# import json
# import datetime
# import requests
# from pprint import pprint
# from helper import get_service

# get_service()

# API_KEY = "AIzaSyDnjvOsAEElOR0wwTaOrV3MXR6RJiqqDWs"
# url = f"https://www.googleapis.com/calendar/v3/calendars/primary/events?key={API_KEY}"

# access_token = ''
# now = datetime.datetime.now()
# with open("token.json") as f:
#   data = json.loads(f.read())
#   token = data.get('token')
#   access_token = token
#   print(access_token)


# headers = {
#   'Content-Type': 'application/json', 
#   'Accept': 'application/json', 
#   'Authorization': f'Bearer {access_token}'
# }

# event = json.dumps({
#   'summary': 'Test Event Summary',
#   'location': 'Dera Bassi, Mohali, Punjab',
#   'description': 'This is test event description',
#   'start': {'dateTime': "2023-08-28T17:00:00+05:30",'timeZone': 'Asia/Kolkata',},
#   'end': {'dateTime': "2023-08-28T18:00:00+05:30", 'timeZone': 'Asia/Kolkata',},
#   'recurrence': ['RRULE:FREQ=DAILY;COUNT=2'],
#   'attendees': [{'email': 'lpage@example.com'},{'email': 'sbrin@example.com'},],
#   # 'reminders': {
#   #   'useDefault': False,
#   #   'overrides': [
#   #     {'method': 'email', 'minutes': 24 * 60},
#   #     {'method': 'popup', 'minutes': 10},
#   #   ],
# })

# response = requests.post(url=url, headers=headers, data=event)

# pprint(response.text)
# if response.status_code == 200:
#   print(response.text)
# else:
#   print("something went wrong")
import datetime

start = datetime.datetime.strptime("2023-08-23 12:15:00", '%Y-%m-%d %H:%M:%S')

print(datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S+05:30'))