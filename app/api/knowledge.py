from fastapi import APIRouter, HTTPException
from app.services.knowledge_service import KnowledgeService
from app.core.config import settings

router = APIRouter()
knowledge_service = KnowledgeService()

@router.get("/knowledge/query")
async def query_knowledge(query: str):
    """Query the knowledge base"""
    try:
        result = await knowledge_service.query_knowledge_base(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/knowledge/business-type")
async def get_business_type():
    """Get the current business type"""
    return {"business_type": settings.BUSINESS_TYPE}

@router.get("/knowledge/menu")
async def get_menu():
    """Get the menu (for restaurant business type)"""
    if settings.BUSINESS_TYPE != "restaurant":
        raise HTTPException(status_code=400, detail="This endpoint is only available for restaurant business type")
    
    try:
        result = await knowledge_service.query_knowledge_base("menu")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/knowledge/properties")
async def get_properties():
    """Get the properties (for real estate business type)"""
    if settings.BUSINESS_TYPE != "real_estate":
        raise HTTPException(status_code=400, detail="This endpoint is only available for real estate business type")
    
    try:
        result = await knowledge_service.query_knowledge_base("properties")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 