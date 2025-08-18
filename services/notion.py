import requests

import os
import json
from dotenv import load_dotenv

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
TASK_DB_ID = os.getenv("TASK_DB_ID")

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_pages():
    url = f"https://api.notion.com/v1/databases/{TASK_DB_ID}/query"
    payload = {"page_size": 100}
    response = requests.post(url, headers=headers, json=payload)

    data = response.json()
    with open("notion_data.json", "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    results = data["results"]
    return results

pages = get_pages()
for page in pages:
    task = page["properties"]["Task"]["title"][0]["text"]["content"]
    deadline = page["properties"]["Deadline"]["date"]["start"]
    status = page["properties"]["Status"]["status"]["name"]

    print(f"Task: {task}, Deadline: {deadline}, Status: {status}")

