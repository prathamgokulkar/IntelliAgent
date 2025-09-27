from pydantic import BaseModel

class QueryRequest(BaseModel):

    # Defines the structure for a request to the /api/query endpoint
    question: str


class QueryResponse(BaseModel):
    # Defines the structure for a successful response from the /api/query endpoint.
    success: bool
    answer: str


class UploadResponse(BaseModel):
   
    success: bool
    message: str