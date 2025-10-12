import os
import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
from typing import Literal

load_dotenv()

JIRA_URL = os.getenv("JIRA_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")

issue_url = f"{JIRA_URL}/issue"

def get_user_id(email_or_name: str):
    url = f"{JIRA_URL}/user/search"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {"Accept": "application/json"}
    
    params = {"query": email_or_name}
    response = requests.get(url, headers=headers, auth=auth, params=params)
    
    if response.status_code == 200:
        users = response.json()
        if users:
            return users[0].get('accountId')
    return None

def create_issue(title: str, description: str, due_date: str, team: Literal["Product", "Engineering", "Marketing", "Design"]):
    """
    Create a Jira issue with the given title, description, due date, and team.

    Args:
        title: The title of the issue.
        description: A detailed description of the issue.
        due_date: The due date of the issue in YYYY-MM-DD format.
        team: The team of the issue (Product, Engineering, Marketing, Design).
    """
    teams = {
        "Product": "sohanyt.main@gmail.com",
        "Engineering": "amomahesh@ucdavis.edu",
        "Marketing": "savir.1614@gmail.com",
        "Design": "aritrasray@gmail.com"
    }
    issue_url = f"{JIRA_URL}/issue"
    auth = HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    fields = {
        "project": {
            "key": JIRA_PROJECT_KEY
        },
        "issuetype": {
            "name": "Task"
        },
        "summary": title,
        "description": {
            "content": [{
                "type": "paragraph",
                "content": [{
                    "type": "text",
                    "text": description
                }]
            }],
            "type": "doc",
            "version": 1
        },
        "labels": [team],
        "duedate": due_date
    }
    assignee_id = get_user_id(teams[team])
    if assignee_id:
        fields["assignee"] = {"id": assignee_id}
    payload = json.dumps({"fields": fields})
    response = requests.post(issue_url, data=payload, headers=headers, auth=auth)
    return response.json()