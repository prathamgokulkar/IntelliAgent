from pydantic import BaseModel

class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    success: bool
    answer: str


class UploadResponse(BaseModel):
   
    success: bool
    message: str