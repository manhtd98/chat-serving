import time

import requests
from celery import Celery
from schemas import UserIn
from pipeline_langchain import load_chain

app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)


LANGCHAIN_PIPELINE = load_chain()
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


@app.task(name="task_query_workflow")
def task_query_workflow(query: str, chat_history: dict) -> dict:
    chat_history = []
    result = LANGCHAIN_PIPELINE({"question": query, "chat_history": chat_history})
    return {
        "result": {
            "query": query,
            "answern": result["answer"],
            "source_documents": result["source_documents"],
            "confident": 0.89,
        }
    }
