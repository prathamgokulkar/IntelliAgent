import { useState, useCallback, useEffect, useRef } from 'react'

function App() {
  const [pdfFile, setPdfFile] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [isIndexed, setIsIndexed] = useState(false)
  const [error, setError] = useState('')
  const [isDragOver, setIsDragOver] = useState(false)
  
  // Chat state
  const [messages, setMessages] = useState([])
  const [currentQuestion, setCurrentQuestion] = useState('')
  const [isChatLoading, setIsChatLoading] = useState(false)
  const [showChat, setShowChat] = useState(false)
  const [showScrollButton, setShowScrollButton] = useState(false)
  
  const chatMessagesRef = useRef(null)

  useEffect(() => {
    if (chatMessagesRef.current) {
      chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight
    }
  }, [messages, isChatLoading])

  // Handle scroll events to show/hide scroll-to-bottom button
  const handleScroll = useCallback(() => {
    if (chatMessagesRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = chatMessagesRef.current
      const isNearBottom = scrollHeight - scrollTop - clientHeight < 100
      setShowScrollButton(!isNearBottom)
    }
  }, [])

  // Scroll to bottom function
  const scrollToBottom = useCallback(() => {
    if (chatMessagesRef.current) {
      chatMessagesRef.current.scrollTo({
        top: chatMessagesRef.current.scrollHeight,
        behavior: 'smooth'
      })
    }
  }, [])

  const handleFileUpload = useCallback(async (file) => {
    if (!file || file.type !== 'application/pdf') {
      setError('Please select a valid PDF file')
      return
    }

    setError('')
    setIsLoading(true)
    setPdfFile(file)

    try {
      // FormData to send file to backend
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('http://localhost:8000/api/process-invoice', {
        method: 'POST',
        body: formData
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to parse PDF')
      }

      const data = await response.json()

      if (data.success) {
        setIsIndexed(true); 
        console.log("Backend has indexed the document successfully.");
      }    
    } catch (err) {
      setError('Error parsing PDF: ' + err.message)
    } finally {
      setIsLoading(false)
    }
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setIsDragOver(false)
    
    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFileUpload(files[0])
    }
  }, [handleFileUpload])

  const handleDragOver = useCallback((e) => {
    e.preventDefault()
    setIsDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e) => {
    e.preventDefault()
    setIsDragOver(false)
  }, [])

  const handleFileInput = useCallback((e) => {
    const file = e.target.files[0]
    if (file) {
      handleFileUpload(file)
    }
  }, [handleFileUpload])

  const clearData = useCallback(() => {
    setPdfFile(null)
    setError('')
    setMessages([])
    setShowChat(false)
  }, [])

  const handleChatSubmit = useCallback(async (e) => {
    e.preventDefault()
    if (!currentQuestion.trim() || !isIndexed || isChatLoading) return;

    const question = currentQuestion.trim()
    setCurrentQuestion('')
    setIsChatLoading(true)

    // Add user message to chat
    const userMessage = { type: 'user', content: question, timestamp: new Date() }
    setMessages(prev => [...prev, userMessage])

    try {
      const response = await fetch('http://localhost:8000/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question,
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.error || 'Failed to get answer')
      }

      const data = await response.json()
      
      // Add AI response to chat
      const aiMessage = { 
        type: 'ai', 
        content: data.answer, 
        timestamp: new Date(),
        metadata: {
          chunksUsed: data.chunksUsed,
          contextLength: data.contextLength
        }
      }
      setMessages(prev => [...prev, aiMessage])

    } catch (err) {
      const errorMessage = { 
        type: 'error', 
        content: 'Error: ' + err.message, 
        timestamp: new Date() 
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsChatLoading(false)
    }
  }, [currentQuestion, isIndexed, isChatLoading])

  const startChat = useCallback(() => {
    if (isIndexed) {
      setShowChat(true)
      setMessages([{
        type: 'ai',
        content: 'Hello! I\'m your AI assistant. I can help you understand this PDF document. What would you like to know?',
        timestamp: new Date()
      }])
    }
  }, [isIndexed])

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-800 via-blue-900 to-blue-900">
      <header className="bg-white/10 backdrop-blur-md border-b border-white/20">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl md:text-4xl font-bold text-white text-center mb-2">
          IntelliAgent
          </h1>
          <p className="text-white/90 text-center text-lg">
            Upload a PDF and chat with AI to get answers about your document
          </p>
        </div>
      </header>

      {/* Main Content - Two Column Layout */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 h-[calc(100vh-200px)]">
          
          {/* Left Column - PDF Upload */}
          <div className="flex flex-col space-y-4">
            {/* Upload Area */}
            <div className="flex-1">
              <div
                className={`h-full border-2 border-dashed rounded-xl p-8 text-center transition-all duration-300 cursor-pointer ${
                  isDragOver 
                    ? 'border-green-400 bg-green-50/20 scale-105' 
                    : 'border-white/30 bg-white/10 hover:border-white/50 hover:bg-white/15 hover:-translate-y-1'
                }`}
                onDrop={handleDrop}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
              >
                <div className="flex flex-col items-center justify-center h-full">
                  <div className="text-6xl mb-4 opacity-80">📄</div>
                  <h3 className="text-xl font-semibold text-white mb-2">
                    Drop your PDF here
                  </h3>
                  <p className="text-white/80 mb-6">or click to browse files</p>
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={handleFileInput}
                    className="hidden"
                    id="pdf-upload"
                  />
                  <label
                    htmlFor="pdf-upload"
                    className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-green-500 to-green-600 text-white font-semibold rounded-full hover:from-green-600 hover:to-green-700 transform hover:-translate-y-1 transition-all duration-300 shadow-lg hover:shadow-xl cursor-pointer"
                  >
                    Choose PDF File
                  </label>
                </div>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <div className="bg-red-50/20 border border-red-300/30 rounded-lg p-4 flex items-center gap-3 backdrop-blur-sm">
                <span className="text-red-400 text-xl">⚠️</span>
                <span className="text-red-200">{error}</span>
              </div>
            )}

            {/* Loading State */}
            {isLoading && (
              <div className="bg-white/10 rounded-lg p-8 text-center backdrop-blur-sm">
                <div className="w-10 h-10 border-4 border-white/30 border-t-white rounded-full animate-spin mx-auto mb-4"></div>
                <p className="text-white text-lg font-medium">Extracting text from PDF...</p>
              </div>
            )}

            {/* File Info */}
            {pdfFile && !isLoading && (
              <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20">
                <h3 className="text-white text-lg font-semibold mb-4">File Information</h3>
                <div className="space-y-2 text-white/90">
                  <p><strong>Name:</strong> {pdfFile.name}</p>
                  <p><strong>Size:</strong> {(pdfFile.size / 1024 / 1024).toFixed(2)} MB</p>
                  <p><strong>Type:</strong> {pdfFile.type}</p>
                </div>
                <button
                  onClick={clearData}
                  className="mt-4 w-full bg-gradient-to-r from-red-500 to-red-600 text-white font-semibold py-2 px-4 rounded-lg hover:from-red-600 hover:to-red-700 transform hover:-translate-y-1 transition-all duration-300 shadow-lg"
                >
                  Clear & Upload New
                </button>
              </div>
            )}

            {/* Success State */}
            {isIndexed && !showChat && (
              <div className="bg-green-900/50 backdrop-blur-sm rounded-lg p-6 shadow-xl border border-green-500/30">
                <div className="flex items-center gap-3 mb-4">
                  <span className="text-2xl">✅</span>
                  <h3 className="text-green-300 text-lg font-semibold">PDF Indexed Successfully!</h3>
                </div>
                <p className="text-gray-300 mb-4">
                  The document has been processed and is ready for you to ask questions.
                </p>
                <button
                  onClick={startChat}
                  className="w-full bg-indigo-600 text-white font-semibold py-3 px-4 rounded-lg hover:bg-indigo-700 transform hover:-translate-y-1 transition-all duration-300 shadow-lg"
                >
                  💬 Chat with PDF
                </button>
              </div>
            )}
          </div>

          {/* Right Column - Chat Interface */}
          <div className="flex flex-col">
            {showChat ? (
              <div className="bg-white/95 backdrop-blur-sm rounded-lg shadow-xl h-full flex flex-col max-h-[600px]">
                {/* Chat Header */}
                <div className="flex justify-between items-center p-4 border-b border-gray-200">
                  <h3 className="text-gray-800 text-lg font-semibold">💬 Chat with your PDF</h3>
                  <button
                    onClick={() => setShowChat(false)}
                    className="w-8 h-8 bg-red-500 text-white rounded-full hover:bg-red-600 transform hover:scale-110 transition-all duration-300 flex items-center justify-center"
                  >
                    ✕
                  </button>
                </div>
                
                {/* Messages */}
                <div 
                  ref={chatMessagesRef}
                  onScroll={handleScroll}
                  className="flex-1 overflow-y-auto p-4 space-y-4 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100 hover:scrollbar-thumb-gray-400 relative"
                  style={{ scrollBehavior: 'smooth' }}
                >
                  {messages.map((message, index) => (
                    <div key={index} className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                      <div className={`flex items-start gap-3 max-w-[80%] ${message.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center text-lg flex-shrink-0 ${
                          message.type === 'user' 
                            ? 'bg-gradient-to-r from-blue-500 to-blue-600' 
                            : message.type === 'ai'
                            ? 'bg-gradient-to-r from-green-500 to-green-600'
                            : 'bg-gradient-to-r from-red-500 to-red-600'
                        }`}>
                          {message.type === 'user' && '👤'}
                          {message.type === 'ai' && '🤖'}
                          {message.type === 'error' && '⚠️'}
                        </div>
                        <div className="flex-1 min-w-0">
                          <div className={`px-4 py-3 rounded-2xl ${
                            message.type === 'user'
                              ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white'
                              : message.type === 'error'
                              ? 'bg-red-50 text-red-800 border border-red-200'
                              : 'bg-gray-100 text-gray-800'
                          }`}>
                            <div className="break-words">{message.content}</div>
                            {message.metadata && (
                              <div className="text-xs opacity-70 mt-1">
                                Chunks: {message.metadata.chunksUsed} | Context: {message.metadata.contextLength} chars
                              </div>
                            )}
                          </div>
                          <div className="text-xs text-gray-500 mt-1">
                            {message.timestamp.toLocaleTimeString()}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                  
                  {isChatLoading && (
                    <div className="flex justify-start">
                      <div className="flex items-start gap-3 max-w-[80%]">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-r from-green-500 to-green-600 flex items-center justify-center text-lg flex-shrink-0">
                          🤖
                        </div>
                        <div className="bg-gray-100 px-4 py-3 rounded-2xl">
                          <div className="flex gap-1">
                            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                            <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  {/* Scroll to bottom button */}
                  {showScrollButton && (
                    <button
                      onClick={scrollToBottom}
                      className="fixed bottom-20 right-8 w-12 h-12 bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-full shadow-lg hover:from-blue-600 hover:to-blue-700 transform hover:scale-110 transition-all duration-300 flex items-center justify-center z-10"
                      title="Scroll to bottom"
                    >
                      ↓
                    </button>
                  )}
                </div>

                {/* Chat Input */}
                <form onSubmit={handleChatSubmit} className="p-4 border-t border-gray-200">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={currentQuestion}
                      onChange={(e) => setCurrentQuestion(e.target.value)}
                      placeholder="Ask a question about your PDF..."
                      className="flex-1 px-4 py-3 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed"
                      disabled={isChatLoading}
                    />
                    <button
                      type="submit"
                      disabled={!currentQuestion.trim() || isChatLoading}
                      className="w-12 h-12 bg-gradient-to-r from-green-500 to-green-600 text-white rounded-full hover:from-green-600 hover:to-green-700 disabled:from-gray-400 disabled:to-gray-500 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-300 flex items-center justify-center shadow-lg"
                    >
                      {isChatLoading ? '⏳' : '➤'}
                    </button>
                  </div>
                </form>
              </div>
            ) : (
              <div className="bg-white/10 backdrop-blur-sm rounded-lg h-full flex items-center justify-center border border-white/20">
                <div className="text-center text-white/80">
                  <div className="text-6xl mb-4">💬</div>
                  <h3 className="text-xl font-semibold mb-2">Start a Conversation</h3>
                  <p className="text-sm">Upload a PDF and click "Chat with PDF" to begin</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
