"""Streaming Multimodal Chat and Context Caching Router."""
import os
import json
import asyncio
from datetime import timedelta
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import google.generativeai as genai

router = APIRouter(prefix="/api/chat", tags=["chat"])

# Configure Gemini API key if present
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


class ChatMessagePart(BaseModel):
    text: Optional[str] = None
    inline_data: Optional[Dict[str, Any]] = None  # e.g., {"mime_type": "image/jpeg", "data": "<base64>"}


class ChatMessage(BaseModel):
    role: str  # "user" or "model"
    parts: List[ChatMessagePart]


class StreamingChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = "gemini-1.5-flash"
    system_instruction: Optional[str] = None
    cache_id: Optional[str] = None


class ContextCacheRequest(BaseModel):
    model: str = "gemini-1.5-pro"
    contents: List[str]
    ttl_minutes: int = 5


@router.post("/cache")
async def create_context_cache(req: ContextCacheRequest):
    """Create or register context caching for reuse across streaming sessions."""
    if not GEMINI_API_KEY:
        # Mock payload when API key is not configured
        return {
            "cache_id": f"cached_context_mock_{hash(tuple(req.contents)) % 100000}",
            "model": req.model,
            "ttl_minutes": req.ttl_minutes,
            "status": "cached"
        }
    try:
        # Utilizing genai caching pattern with valid timedelta
        cache = genai.caching.CachedContent.create(
            model=req.model,
            contents=req.contents,
            ttl=timedelta(minutes=req.ttl_minutes)
        )
        return {
            "cache_id": getattr(cache, "name", "cached_context"),
            "model": req.model,
            "ttl_minutes": req.ttl_minutes,
            "status": "cached"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stream")
async def stream_multimodal_chat(req: StreamingChatRequest):
    """Stream response from Gemini API supporting multimodal input and context caching."""
    selected_model = req.model or "gemini-1.5-flash"

    async def generate_stream():
        if not GEMINI_API_KEY:
            # Mock streaming output when GEMINI_API_KEY is not configured
            response_text = f"Streaming response from model {selected_model}: Hello! I am responding with multimodal streaming capabilities."
            for chunk in response_text.split(" "):
                yield f"data: {json.dumps({'text': chunk + ' '})}\n\n"
                await asyncio.sleep(0.05)
            yield "data: [DONE]\n\n"
            return

        try:
            kwargs = {}
            if req.system_instruction:
                kwargs["system_instruction"] = req.system_instruction
            if req.cache_id:
                try:
                    cached_content = genai.caching.CachedContent.get(req.cache_id)
                    kwargs["cached_content"] = cached_content
                except Exception:
                    pass

            model_instance = genai.GenerativeModel(
                model_name=selected_model,
                **kwargs
            )
            # Format history/parts
            formatted_contents = []
            for msg in req.messages:
                parts_list = []
                for p in msg.parts:
                    if p.text:
                        parts_list.append(p.text)
                    elif p.inline_data:
                        parts_list.append(p.inline_data)
                formatted_contents.append({"role": msg.role, "parts": parts_list})

            response = model_instance.generate_content(
                formatted_contents,
                stream=True
            )
            for chunk in response:
                if chunk.text:
                    yield f"data: {json.dumps({'text': chunk.text})}\n\n"
            yield "data: [DONE]\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(generate_stream(), media_type="text/event-stream")
