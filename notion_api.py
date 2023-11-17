from datetime import datetime
import json
from typing import List, Optional
import requests
from requests import Response
from commands.projects.entities import ProjectsItem

from settings import API_URL, ACCEPTED_KEYS
from commands.tasks.entities import TaskItem, TaskToCreate
from commands.birthdays.entities import BirthdayItem

class NotionAPI:

    def __init__(self, api_token: str, notion_version: str) -> None:
        self.api_token: str = api_token
        self.notion_version: str = notion_version

    def __sanitize_data(self, data: List[dict]) -> List[dict]:
        items = []
        for i in data:
            temp = {k: v for k, v in i.items() if k in ACCEPTED_KEYS}
            items.append(temp)
        return items

    def query_tasks(self,
                    database_id: str,
                    daily: bool = False,
                    weekly: bool = False) -> List[TaskItem]:
        """List tasks based on the given filter."""
        filter: Optional[dict] = {"filter": { "property": "Data", "date": {} }}
        if daily:
            filter["filter"]["date"] = {"equals": datetime.today().date().isoformat()}
        elif weekly:
            filter["filter"]["date"] = {"this_week": {}}
        else:
            filter = None
        response = requests.post(
            f"{API_URL}/databases/{database_id}/query",
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Notion-Version": self.notion_version,
            },
            json=json.loads(json.dumps(filter))
        )
        items = self.__sanitize_data(response.json()["results"])
        datas = []
        for item in items:
            datas.append(TaskItem(**item))
        return datas

    def query_bithdays(self, database_id: str) -> List[BirthdayItem]:
        response = requests.post(
            f"{API_URL}/databases/{database_id}/query",
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Notion-Version": self.notion_version,
            }
        )
        items = self.__sanitize_data(data=response.json()["results"])
        data = []
        for item in items:
            data.append(BirthdayItem(**item))
        return data

    def query_projects(self, database_id: str) -> List[ProjectsItem]:
        response = requests.post(
            f"{API_URL}/databases/{database_id}/query",
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Notion-Version": self.notion_version,
            }
        )
        items = self.__sanitize_data(data=response.json()["results"])
        data = []
        for item in items:
            data.append(ProjectsItem(**item))
        return data

    def create_tasks(self, task: TaskToCreate) -> Response:
        """Creates a inbox tasks into the Tasks Database"""
        response = requests.post(
            f"{API_URL}/pages",
            headers={
                "Authorization": f"Bearer {self.api_token}",
                "Notion-Version": self.notion_version,
            },
            json=task.as_dict(),
        )

        return response
