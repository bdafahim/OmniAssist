from fastapi import APIRouter, HTTPException, Body
from app.services.knowledge_service import KnowledgeService
from app.core.config import settings
from typing import Dict

router = APIRouter(prefix="/knowledge", tags=["knowledge"])
knowledge_service = KnowledgeService()

@router.get("/query")
async def query_knowledge(query: str):
    """Query the knowledge base"""
    try:
        result = await knowledge_service.query_knowledge_base(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/business-type")
async def get_business_type():
    """Get the current business type"""
    return {"business_type": settings.BUSINESS_TYPE}

@router.get("/menu")
async def get_menu():
    """Get the menu (for restaurant business type)"""
    if settings.BUSINESS_TYPE != "restaurant":
        raise HTTPException(status_code=400, detail="This endpoint is only available for restaurant business type")
    
    try:
        result = await knowledge_service.query_knowledge_base("menu")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/properties")
async def get_properties():
    """Get the properties (for real estate business type)"""
    if settings.BUSINESS_TYPE != "real_estate":
        raise HTTPException(status_code=400, detail="This endpoint is only available for real estate business type")
    
    try:
        result = await knowledge_service.query_knowledge_base("properties")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/update")
async def update_knowledge(data: Dict = Body(...)):
    """
    Update the knowledge base with new information
    
    Example request body for restaurant:
    {
        "menu": {
            "appetizers": [
                {"name": "New Appetizer", "price": 9.99, "description": "A new delicious appetizer"}
            ]
        },
        "hours": "Monday-Sunday: 10am-11pm"
    }
    
    Example request body for real estate:
    {
        "properties": [
            {
                "id": "4",
                "type": "House",
                "address": "321 Elm St, Anytown, USA",
                "price": 400000,
                "bedrooms": 4,
                "bathrooms": 3,
                "square_feet": 2500,
                "description": "Spacious family home with pool"
            }
        ]
    }
    """
    try:
        success = await knowledge_service.update_knowledge_base(data)
        if success:
            return {"status": "success", "message": "Knowledge base updated successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to update knowledge base")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 