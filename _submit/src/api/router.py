from fastapi import APIRouter

from api.v1 import auth, roles

router = APIRouter()
router.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
router.include_router(roles.router, prefix="/api/v1/roles", tags=["roles"])
