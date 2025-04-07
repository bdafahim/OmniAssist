from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from app.api import voice, knowledge, sms
from app.core.config import settings
import os

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="An AI-powered customer service and ordering agent that can interact with customers via phone calls",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(voice.router, prefix=settings.API_V1_STR)
app.include_router(knowledge.router, prefix=settings.API_V1_STR)
app.include_router(sms.router, prefix=settings.API_V1_STR)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/api/v1/")
async def api_root():
    return {
        "message": "AI Customer Service & Ordering Agent API",
        "business_type": settings.BUSINESS_TYPE,
        "api_version": settings.API_V1_STR
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 