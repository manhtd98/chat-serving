import time

import requests
from celery import Celery
from schemas import UserIn

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="sqla+postgresql://user:password@database:5432/alpha",
)


@app.task
def task_add_user(count: int, delay: int):
    url = "https://randomuser.me/api"
    response = requests.get(f"{url}?results={count}").json()["results"]
    time.sleep(delay)
    result = []
    for item in response:
        user = UserIn(
            first_name=item["name"]["first"],
            last_name=item["name"]["last"],
            mail=item["email"],
            age=item["dob"]["age"],
        )
        # if crud_add_user(user):
        #     result.append(user.dict())
    return {"success": result}


@app.task
def task_query_workflow(query: str, chat_history: dict) -> dict:
    return {
        "result": {
            "query": query,
            "answern": "Happy time with our Chatbot",
            "confident": 0.89,
        }
    }
