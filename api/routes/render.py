from fastapi import APIRouter, Depends, Request
from depends import get_crypt_course, get_usd_course, get_user, User, get_authorized, get_db, Session
from main import render_template
from utils import format_int
from fastapi.responses import RedirectResponse
from models.crud import UserCRUD
from models.user import UserPrivate
router = APIRouter(include_in_schema=False)

@router.get("/")
async def index(
        request: Request,
        user: User | None = Depends(get_user),
        course: tuple[float, float] = Depends(get_crypt_course),
        usd_course: float = Depends(get_usd_course)):
    return render_template('index.html', course=course, request=request, usd=usd_course, format_int=format_int, user=user)

@router.get("/register")
async def register(request: Request):
    return render_template('register.html', request=request)

@router.get("/admin")
async def admin_index(request: Request, user: User = Depends(get_authorized),
                      db: Session = Depends(get_db)):
    if not user.is_admin:
        return RedirectResponse(url='/')
    return render_template('admin.html', users=UserCRUD.get_all(db), user=user, request=request)

@router.get("/logout")
async def logout():
    resp = RedirectResponse(url='/')
    resp.delete_cookie(key='token')
    return resp
