import requests
import json
import os

TODOIST_TOKEN=os.environ.get('TODOIST_TOKEN')
PROJECT_ID=os.environ.get('PROJECT_ID')
NTFY_SERVER_ENDPOINT=os.environ.get('NTFY_SERVER_ENDPOINT')

res = requests.post(
  "https://api.todoist.com/sync/v9/projects/get_data",
  headers={"Authorization":f'Bearer {TODOIST_TOKEN}'}, 
  data={"project_id":PROJECT_ID}
)
data = res.json()
if(len(data["items"])!=0):
  url = NTFY_SERVER_ENDPOINT
  message="Please check Todoist, items in inbox detected"
  response = requests.post(url, data=message, headers={"Tags":"inbox_tray,pushpin"})
  if response.status_code == 200:
    print("Text data posted successfully!")
  else:
    print(f"Error: {response.status_code}")
    print(response.text)
  