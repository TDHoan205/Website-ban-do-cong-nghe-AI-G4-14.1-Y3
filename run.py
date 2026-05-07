"""
Webstore FastAPI - Entry Point
Run with: python run.py
"""
# pyrefly: ignore [missing-import]
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "flask_app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
