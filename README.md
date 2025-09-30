# IntelliAgent AI: A Multi-Agent RAG System
A full-stack, AI-powered application for conversing with your financial documents. This system uses a multi-agent architecture to provide intelligent, fact-checked answers from both digital and scanned PDFs.

### Features
1. Hybrid PDF Processing: Handles both digitally native and scanned (image-based) PDFs seamlessly.
2. Multi-Agent Architecture: A robust backend built with specialized agents for Orchestration, Indexing, OCR, and Q&A.
3. Conversational Q&A: Ask complex questions in natural language and get answers based on the document's content.
4. Fact-Checked Responses: Includes a Validation Agent to check the AI's answers against the source text, reducing hallucinations.
5. Persistent Memory: Utilizes a Qdrant vector database running in Docker for fast, reliable, and isolated document memory.
6. Modern UI: A sleek, responsive chat interface built with React and Tailwind CSS.
7. Fast Inference: Powered by the high-speed Groq API for near-instantaneous LLM responses.

### Architecture
- Frontend: React + Vite (Port 5173)

- Backend: Python + FastAPI (Port 8000)

- AI Orchestration: LangChain

- Vector Database: Qdrant (via Docker)

- Embedding Model: Hugging Face all-MiniLM-L6-v2

- Language Model (LLM): Groq API (Llama 3)

- OCR Engine: Tesseract OCR

- PDF Parsing: PyMuPDF

## Quick Start
#### Prerequisites
- Docker Desktop: Must be installed and running.

- Python 3.10+ and a virtual environment (e.g., conda).

- Node.js and npm.

- Tesseract OCR installed on your system.
  
---

1. Configure Environment Variables
In the backend/ directory, create a .env file and add your Groq API key:
```
GROQ_API_KEY="gsk_YourSecretKeyHere"
```
2. Start the Qdrant Database
In a terminal, navigate to the backend/ directory and run:
```
docker-compose up -d
```
You can view the Qdrant dashboard at http://localhost:6334/dashboard.

3. Start the Backend Server
In a new terminal, activate your Python environment, navigate to the backend/ directory, and run:

### Activate your conda environment (e.g., conda activate btech_final)
```
pip install -r requirements.txt
uvicorn main:app --reload
```
The backend will be running on http://localhost:8000.

4. Start the Frontend Server
In a third terminal, navigate to the frontend/ directory and run:
```
npm install
npm run dev
```
The application will be available at http://localhost:5173.

---

### API Endpoints
- POST /api/process-invoice: Clears the old session and indexes a new PDF.

- POST /api/query: Receives a question and returns an AI-generated answer.

- POST /api/clear-store: Manually clears the vector database.
```
Project Structure
IntelliAgent-AI/
├── frontend/           # React frontend
│   ├── src/
│   └── package.json
└── backend/            # Python backend
    ├── .env
    ├── docker-compose.yml
    ├── main.py         # Orchestrator Agent (FastAPI)
    ├── requirements.txt
    └── src/
        ├── agents/     # Specialized agent logic
        └── core/       # Core services (loader, splitter, etc.)
```
