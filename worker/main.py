from pipeline_langchain import load_chain
from celery_config import create_worker_from, ChatQueryTask
from loguru import logger
class ChatQueryTaskImp(ChatQueryTask):
    def __init__(self):
        super().__init__()
        self.LANGCHAIN_PIPELINE = load_chain()
    
    def run(self, query) -> dict:
        logger.info("START PROCESSING")
        chat_history = []
        result = self.LANGCHAIN_PIPELINE({"question": query, "chat_history": chat_history})
        logger.info("END PROCESSING")
        return {
            "result": {
                "query": query,
                "answern": result["answer"],
                "source_documents": result["source_documents"],
                "confident": 0.89,
            },
            "status":"SUCCESS"
        }

app, _ = create_worker_from(ChatQueryTaskImp)
if __name__=="__main__":
    app.worker_main()
# @app.task
# def task_add_user(count: int, delay: int):
#     url = "https://randomuser.me/api"
#     response = requests.get(f"{url}?results={count}").json()["results"]
#     time.sleep(delay)
#     result = []
#     for item in response:
#         user = UserIn(
#             first_name=item["name"]["first"],
#             last_name=item["name"]["last"],
#             mail=item["email"],
#             age=item["dob"]["age"],
#         )
#         # if crud_add_user(user):
#         #     result.append(user.dict())
#     return {"success": result}

