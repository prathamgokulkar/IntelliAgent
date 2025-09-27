# PDF AI Chat Assistant

A full-stack application for uploading PDFs and chatting with AI to get answers about your documents using Gemini AI.

## Features

- 📄 **PDF Upload**: Drag-and-drop or click to upload PDF files
- 🔍 **Text Extraction**: Extract text content from PDFs using pdf-parse
- 🤖 **AI Chat**: Chat with Gemini AI about your PDF content
- 💬 **Smart Responses**: AI provides contextual answers based on PDF content
- 📊 **Text Chunking**: Intelligent text processing for better AI responses
- 💾 **Export Options**: Copy to clipboard or download as text file
- 🎨 **Modern UI**: Beautiful, responsive chat interface
- ⚡ **Fast Processing**: Server-side PDF parsing and AI processing

## Architecture

- **Frontend**: React + Vite (Port 5173)
- **Backend**: Node.js + Express (Port 3001)
- **PDF Parsing**: pdf-parse library
- **AI Integration**: Google Gemini AI
- **Text Processing**: Custom chunking and relevance algorithms

## Quick Start

### Option 1: Start Both Servers (Recommended)
```bash
./start-dev.sh
```

### Option 2: Start Servers Separately

1. **Start Backend**:
   ```bash
   cd backend
   npm start
   ```

2. **Start Frontend** (in a new terminal):
   ```bash
   cd server
   npm run dev
   ```

## API Endpoints

### POST /api/parse-pdf
Upload and parse a PDF file.

**Request**: Multipart form data with `pdf` field
**Response**:
```json
{
  "success": true,
  "text": "Extracted text content...",
  "metadata": {
    "fileName": "document.pdf",
    "fileSize": 1024000,
    "pages": 5,
    "textLength": 2500,
    "wordCount": 400
  }
}
```

### POST /api/chat
Chat with AI about PDF content.

**Request**:
```json
{
  "question": "What is the main topic of this document?",
  "pdfText": "Extracted PDF text content..."
}
```

**Response**:
```json
{
  "success": true,
  "answer": "AI response based on PDF content...",
  "chunksUsed": 3,
  "contextLength": 2500
}
```

### GET /health
Health check endpoint.

## Project Structure

```
PDF/
├── backend/           # Node.js backend
│   ├── server.js     # Express server
│   └── package.json  # Backend dependencies
├── server/           # React frontend
│   ├── src/
│   │   ├── App.jsx   # Main React component
│   │   └── App.css   # Styles
│   └── package.json  # Frontend dependencies
└── start-dev.sh      # Development script
```

## Dependencies

### Backend
- express: Web framework
- pdf-parse: PDF text extraction
- multer: File upload handling
- cors: Cross-origin resource sharing

### Frontend
- react: UI library
- vite: Build tool

## Usage

1. Open http://localhost:5173 in your browser
2. Drag and drop a PDF file or click to browse
3. Wait for text extraction to complete
4. Click "💬 Chat with PDF" to start chatting
5. Ask questions about your PDF content
6. Get AI-powered answers based on your document
7. Copy or download the extracted text if needed

## Environment Setup

1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set the API key in your environment:
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```
   Or add it to a `.env` file in the backend directory.

## Error Handling

- File type validation (PDF only)
- File size limits (10MB max)
- Server error handling
- Network error handling

## Development

The application uses:
- **Backend**: Node.js with Express for API
- **Frontend**: React with Vite for fast development
- **PDF Processing**: pdf-parse for reliable text extraction
- **File Upload**: multer for handling multipart form data

## License

MIT
