from fastapi import APIRouter

from app.api.v1.endpoints import auth, properties, assessments, score_profiles
from app.api.v1.endpoints import catalog_properties

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(properties.router, prefix="/properties", tags=["properties"])
api_router.include_router(assessments.router, prefix="/assessments", tags=["assessments"])
api_router.include_router(score_profiles.router, prefix="/score-profiles", tags=["score_profiles"])
api_router.include_router(
    catalog_properties.router,
    prefix="/catalog-properties",
    tags=["catalog-properties"],
)
from app.api.v1.endpoints import (
    admin_imports,
    assessments,
    auth,
    catalog_properties,
    properties,
    score_profiles,
)
api_router.include_router(admin_imports.router)