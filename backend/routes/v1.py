"""V1 API routes for Maypo platform with RESTful design."""
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field
from datetime import datetime

v1_router = APIRouter(prefix="/api/v1", tags=["v1"])


class ConsultationRequest(BaseModel):
    """Request model for creating a consultation."""
    query: str = Field(..., min_length=1, description="Consultation query")
    topic: str = Field("general", description="Topic of consultation")
    context: str = Field("", description="Additional context")


class SubmitRequest(BaseModel):
    """Request model for submitting data."""
    data: Dict[str, Any] = Field(..., description="Data to submit")
    type: Optional[str] = Field("general", description="Type of submission")


class ConsultationResponse(BaseModel):
    """Response model for consultations."""
    id: str
    topic: str
    query: str
    recommendation: str
    model: str
    confidence: float
    created_at: str


@v1_router.post(
    "/consultations",
    status_code=status.HTTP_201_CREATED,
    response_model=Dict[str, Any],
    summary="Create a new consultation",
    description="Submit a new consultation request with a query and optional topic"
)
async def create_consultation(request: ConsultationRequest):
    """Create a new consultation request.
    
    Returns:
        - Consultation object with generated ID and recommendation
        - HTTP 201 Created status
        
    Raises:
        - HTTP 400: If query is empty or invalid
    """
    if not request.query.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query cannot be empty or whitespace only"
        )
    
    return {
        "id": "c_102",
        "topic": request.topic,
        "query": request.query,
        "recommendation": f"Consultation result for '{request.query}': Standard prompt optimization applied.",
        "model": "gpt-4o",
        "confidence": 0.95,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }


@v1_router.get(
    "/consultations/{consultation_id}",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    summary="Retrieve a specific consultation",
    description="Get details of a previously created consultation by ID"
)
async def get_consultation(consultation_id: str):
    """Retrieve a specific consultation.
    
    Args:
        consultation_id: The ID of the consultation (must start with 'c_')
    
    Returns:
        - Consultation object with status and details
        
    Raises:
        - HTTP 400: If consultation_id format is invalid
        - HTTP 404: If consultation not found
    """
    if not consultation_id.startswith("c_"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid consultation ID format. ID must start with 'c_'"
        )
    
    # Mock: In production, query database
    return {
        "id": consultation_id,
        "topic": "Prompt Engineering",
        "query": "How to optimize LLM prompts?",
        "recommendation": "Leverage modular prompt architecture and cache repeated completions.",
        "model": "gpt-4o",
        "confidence": 0.95,
        "status": "completed",
        "created_at": "2026-08-29T12:00:00Z"
    }


@v1_router.get(
    "/consultations",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    summary="List all consultations",
    description="Retrieve consultation history with pagination"
)
async def list_consultations(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum records to return")
):
    """View consultation history with pagination.
    
    Args:
        skip: Pagination offset (default 0)
        limit: Pagination limit, max 100 (default 10)
    
    Returns:
        - List of consultations matching criteria
        - Total count of consultations
    """
    return {
        "data": [
            {
                "id": "c_101",
                "topic": "Prompt Engineering",
                "query": "How to optimize LLM prompts?",
                "status": "completed",
                "created_at": "2026-08-28T12:00:00Z"
            },
            {
                "id": "c_102",
                "topic": "System Architecture",
                "query": "Design patterns for scalable APIs",
                "status": "in_progress",
                "created_at": "2026-08-29T10:30:00Z"
            }
        ],
        "pagination": {
            "skip": skip,
            "limit": limit,
            "total": 2
        }
    }


@v1_router.post(
    "/submissions",
    status_code=status.HTTP_201_CREATED,
    response_model=Dict[str, Any],
    summary="Create a new submission",
    description="Submit data for processing"
)
async def create_submission(request: SubmitRequest):
    """Submit data for processing.
    
    Returns:
        - Submission object with ID and status
        - HTTP 201 Created status
        
    Raises:
        - HTTP 400: If data is empty or invalid
    """
    if not request.data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Submission data cannot be empty"
        )
    
    return {
        "id": "sub_123",
        "status": "received",
        "type": request.type,
        "data_keys": list(request.data.keys()),
        "message": "Data successfully queued for processing",
        "created_at": datetime.utcnow().isoformat() + "Z"
    }


@v1_router.get(
    "/submissions/{submission_id}",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    summary="Retrieve submission status",
    description="Get the status and details of a submission by ID"
)
async def get_submission(submission_id: str):
    """Retrieve submission details and status.
    
    Args:
        submission_id: The ID of the submission
        
    Returns:
        - Submission object with current status and results
        
    Raises:
        - HTTP 404: If submission not found
    """
    if not submission_id.startswith("sub_"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid submission ID format"
        )
    
    return {
        "id": submission_id,
        "status": "completed",
        "type": "general",
        "result": "Processing completed successfully",
        "created_at": "2026-08-29T11:00:00Z",
        "completed_at": "2026-08-29T11:05:00Z"
    }


@v1_router.get(
    "/prompts",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    summary="List available prompts",
    description="Retrieve all available prompt templates"
)
async def list_prompts():
    """List all available prompts for consultation.
    
    Returns:
        - List of prompt objects with id, name, and version
        - Total count of available prompts
        
    Example:
        GET /api/v1/prompts
        
        Response: 200 OK
        {
            "prompts": [
                {"id": "p_1", "name": "System Architecture Expert", "version": "1.0.0"},
                {"id": "p_2", "name": "Cost Optimization Advisor", "version": "1.1.0"}
            ],
            "total": 2
        }
    """
    return {
        "prompts": [
            {
                "id": "p_1",
                "name": "System Architecture Expert",
                "version": "1.0.0",
                "description": "Expert advice on system design and architecture"
            },
            {
                "id": "p_2",
                "name": "Cost Optimization Advisor",
                "version": "1.1.0",
                "description": "Recommendations for reducing infrastructure costs"
            }
        ],
        "total": 2
    }


@v1_router.get(
    "/prompts/{prompt_id}",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    summary="Retrieve specific prompt",
    description="Get details of a specific prompt template by ID"
)
async def get_prompt(prompt_id: str):
    """Retrieve details of a specific prompt.
    
    Args:
        prompt_id: The ID of the prompt
        
    Returns:
        - Prompt object with full details and content
        
    Raises:
        - HTTP 404: If prompt not found
    """
    if not prompt_id.startswith("p_"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid prompt ID format"
        )
    
    return {
        "id": prompt_id,
        "name": "System Architecture Expert",
        "version": "1.0.0",
        "description": "Expert advice on system design",
        "content": "You are an expert in system architecture...",
        "created_at": "2026-01-15T10:00:00Z"
    }


@v1_router.get(
    "/usage-analytics",
    status_code=status.HTTP_200_OK,
    response_model=Dict[str, Any],
    summary="Get usage statistics",
    description="Retrieve platform usage analytics and metrics"
)
async def get_usage_analytics(
    period: str = Query("7d", description="Analytics period: 7d, 30d, or 90d")
):
    """Get usage statistics and analytics.
    
    Args:
        period: Time period for analytics (7d, 30d, 90d)
    
    Returns:
        - Total requests count
        - Total tokens used
        - Peak usage hour
        - Top models used
        
    Example:
        GET /api/v1/usage-analytics?period=7d
        
        Response: 200 OK
        {
            "period": "7d",
            "total_requests": 1420,
            "total_tokens_used": 284000,
            "peak_hour": "14:00 UTC",
            "top_models": ["gpt-4o", "claude-3-5-sonnet"]
        }
    """
    valid_periods = ["7d", "30d", "90d"]
    if period not in valid_periods:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid period. Must be one of: {', '.join(valid_periods)}"
        )
    
    return {
        "period": period,
        "total_requests": 1420,
        "total_tokens_used": 284000,
        "peak_hour": "14:00 UTC",
        "top_models": ["gpt-4o", "claude-3-5-sonnet"],
        "average_response_time_ms": 245
    }
