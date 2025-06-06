from fastapi import APIRouter

from services.solar_panels.exports.views import router as exports_router

router = APIRouter(prefix="/solar_panels", tags=["SolarPanels"])
router.include_router(exports_router)
