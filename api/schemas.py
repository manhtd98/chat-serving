from pydantic import BaseModel


class TaskResult(BaseModel):
    trace_id: str
    status: str
    result: dict
    
class QueryRequest(BaseModel):
    query: str
    token: str
    bucket: str

class UserIn(BaseModel):
    first_name: str
    last_name: str
    mail: str
    age: int

class UserOut(BaseModel):
    first_name: str
    last_name: str

