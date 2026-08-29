"""Main application module delegating to FastAPI backend app."""
import sys
from pathlib import Path

# Ensure backend module can be imported
backend_dir = Path(__file__).resolve().parent.parent / "backend"
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from backend.app import app


def hello_world():
    """Return a hello world message."""
    return "Hello, Maypo!"


if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
