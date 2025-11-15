"""
API v1 Router
Consolidates all API endpoints
"""

from fastapi import APIRouter
from app.api.v1.endpoints import (
    auth,
    datasets,
    statistics,
    users
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(datasets.router, prefix="/datasets", tags=["Datasets"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["Statistics"])
