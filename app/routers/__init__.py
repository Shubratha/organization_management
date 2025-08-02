from fastapi import APIRouter

from app.auth.router import router as auth_router
from app.organization.router import router as org_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(org_router)
