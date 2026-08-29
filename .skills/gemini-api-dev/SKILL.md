# Gemini API Dev Skill Guidelines

## Overview
This skill provides pattern definitions, standard conventions, and rules for developing with the Gemini API (using Google GenAI SDKs), including streaming multimodal chat interfaces, context caching, and model routing guidelines.

## 1. SDK Patterns & Usage
- Use `@google/genai` (Node.js/TypeScript) or `google-genai` / `google-generativeai` (Python) standard initialization.
- Initialize clients using environment variable `GEMINI_API_KEY`.

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
```

## 2. Model Routing Guidelines
- **`gemini-1.5-pro`**: Complex reasoning, large context windows, deep multimodal analysis, and context caching.
- **`gemini-1.5-flash`**: High-frequency, low-latency tasks, simple multimodal chat streaming, and cost-effective workloads.

## 3. Context Caching Pattern
- For repetitive or large prompt contexts (e.g. system instructions + extensive documentation/codebases), use Context Caching to optimize latency and token cost.
- TTL (Time To Live) should be set according to session lifecycle.

## 4. Streaming Multimodal Chat Interface
- Endpoint routes must support chunked streaming responses (e.g., Server-Sent Events or FastAPI `StreamingResponse`).
- Handle multimodal inputs (text, images, audio, video) cleanly by formatting parts in the message structure.
- Always handle errors gracefully with standard status codes and fallback models if rate limits are reached.
