from fastapi import APIRouter

from services.batteries.exports.views import router as exports_router

router = APIRouter(prefix="/batteries", tags=["Batteries"])
router.include_router(exports_router)
