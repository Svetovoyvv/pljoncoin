from fastapi import APIRouter, Depends
from depends import admin_required

router = APIRouter(prefix='/admin', tags=['Admin'], dependencies=[Depends(admin_required)])

from .user import router as user_router
from .btc import router as btc_router
router.include_router(user_router)
router.include_router(btc_router)

