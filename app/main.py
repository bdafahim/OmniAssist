from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import voice, knowledge
from app.core.config import settings

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

# Include routers
app.include_router(voice.router, prefix=settings.API_V1_STR)
app.include_router(knowledge.router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {
        "message": "AI Customer Service & Ordering Agent API",
        "business_type": settings.BUSINESS_TYPE,
        "api_version": settings.API_V1_STR
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 