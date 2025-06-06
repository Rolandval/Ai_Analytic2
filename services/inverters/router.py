from fastapi import APIRouter

from services.inverters.exports.views import router as exports_router

router = APIRouter(prefix="/inverters", tags=["Inverters"])
router.include_router(exports_router)
