# app.py
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
import json
import base64
from typing import Optional
import tempfile
import os
import io

# Import your existing modules
from llm import build_llm
from stt import speech_to_text
from tts import speak
from utils import is_exit

app = FastAPI(title="Voice Assistant API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class TextInput(BaseModel):
    text: str
    session_id: Optional[str] = "default"

class TextResponse(BaseModel):
    response: str
    session_id: str
    is_exit: bool = False

class TTSRequest(BaseModel):
    text: str

class AudioResponse(BaseModel):
    audio_base64: str

# Global conversation sessions
conversations = {}

def get_conversation(session_id: str):
    """Get or create a conversation for a session."""
    if session_id not in conversations:
        conversations[session_id] = build_llm()
    return conversations[session_id]

@app.get("/")
async def root():
    return {"message": "CodeMate Voice Assistant API is running!", "version": "1.0.0"}

@app.post("/chat/text", response_model=TextResponse)
async def chat_text(request: TextInput):
    """Process text input and return AI response."""
    try:
        # Check if it's an exit command
        if is_exit(request.text):
            return TextResponse(
                response="Goodbye! Thanks for using CodeMate!",
                session_id=request.session_id,
                is_exit=True
            )
        
        conversation = build_llm()
        
        # Debug: Let's see what invoke returns
        try:
            result = conversation.invoke({"input": request.text})
            print(f"DEBUG - invoke result: {result}")
            print(f"DEBUG - result type: {type(result)}")
            print(f"DEBUG - result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
        except Exception as invoke_error:
            print(f"DEBUG - invoke failed: {invoke_error}")
            # Fallback to predict for now
            response = conversation.predict(text=request.text)
            return TextResponse(
                response=response,
                session_id=request.session_id,
                is_exit=False
            )
        
        # Try different ways to extract the response
        if isinstance(result, dict):
            response = result.get("response") or result.get("text") or result.get("output") or str(result)
        else:
            response = str(result)
        
        return TextResponse(
            response=response,
            session_id=request.session_id,
            is_exit=False
        )
    except Exception as e:
        print(f"ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.post("/speech/recognize")
async def recognize_speech():
    """Convert speech to text using your existing STT function."""
    try:
        text = speech_to_text()
        if text:
            return {"text": text, "success": True}
        else:
            return {"text": "", "success": False, "message": "Could not understand audio"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech recognition error: {str(e)}")

@app.post("/speech/synthesize")
async def synthesize_speech(request: TTSRequest):
    """Convert text to speech using your existing TTS function."""
    try:
        # Use your existing speak function
        speak(request.text)
        return {"success": True, "message": "Speech synthesis completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")

@app.post("/chat/voice")
async def voice_chat(session_id: Optional[str] = "default"):
    """Complete voice interaction - STT -> LLM -> TTS"""
    try:
        # Step 1: Speech to text
        text = speech_to_text()
        if not text:
            raise HTTPException(status_code=400, detail="Could not understand audio")
        
        # Step 2: Check for exit
        if is_exit(text):
            response_text = "Goodbye! Thanks for using CodeMate!"
            speak(response_text)
            return {
                "user_input": text,
                "response": response_text,
                "is_exit": True,
                "session_id": session_id
            }
        
        # Step 3: Get LLM response
        conversation = get_conversation(session_id)
        result = conversation.invoke(text=text)
        
        if isinstance(result, dict):
            response = result.get("response", str(result))
        else:
            response = str(result)
        
        # Step 4: Speak the response
        speak(response)
        
        return {
            "user_input": text,
            "response": response,
            "is_exit": False,
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Voice chat error: {str(e)}")

@app.delete("/session/{session_id}")
async def clear_session(session_id: str):
    """Clear conversation history for a session."""
    if session_id in conversations:
        del conversations[session_id]
        return {"message": f"Session {session_id} cleared successfully"}
    return {"message": f"Session {session_id} not found"}

@app.get("/sessions")
async def list_sessions():
    """List all active sessions."""
    return {"active_sessions": list(conversations.keys())}

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "CodeMate Voice Assistant API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)