# FastAPI app entry point & Orchestrator logic
import os
import shutil
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from src.agents import indexing_agent, retrieval_agent
from src.schemas import QueryRequest, QueryResponse, UploadResponse


app = FastAPI()

# Allow your React frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from the IntelliAgent Backend!"}

@app.post("/api/process-invoice", response_model=UploadResponse)
async def process_invoice(file: UploadFile = File(...)):
    temp_dir = "temp_files"
    os.makedirs(temp_dir, exist_ok=True)
    temp_file_path = os.path.join(temp_dir, file.filename)

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Call the indexing agent to process the PDF
        indexing_agent.process_and_store_pdf(temp_file_path)

        return {"success": True, "message": "PDF processed and indexed successfully."}
    except Exception as e:
        print(f"Orchestrator: Error during PDF processing - {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Orchestrator: Temporary file '{file.filename}' cleaned up.")

@app.post("/api/query", response_model=QueryResponse)
async def query_agent(request: QueryRequest):
    try:
        print(f"Orchestrator: Received query - {request.question}")
        print("Orchestrator: invoking Q&A agent")

        answer = retrieval_agent.answer_query(request.question)
        return {"success": True, "answer": answer}
    
    except Exception as e:
        print(f"Orchestrator: Error during query processing - {e}")
        raise HTTPException(status_code=500, detail=str(e))

