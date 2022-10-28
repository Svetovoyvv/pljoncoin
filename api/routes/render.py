from fastapi import APIRouter, Depends, Request, Query, Path
from depends import get_crypt_course, get_usd_course, get_user, User, get_authorized, get_db, Session
from main import render_template
from utils import format_int
from fastapi.responses import RedirectResponse, HTMLResponse
from models.crud import UserCRUD, LogEntryCRUD
router = APIRouter(tags=['Render'])

@router.get("/", response_class=HTMLResponse, summary='Отображение главной страницы')
async def index(
        request: Request,
        user: User | None = Depends(get_user),
        course: tuple[float, float] = Depends(get_crypt_course),
        usd_course: float = Depends(get_usd_course)):
    return render_template('index.html', course=course, request=request, usd=usd_course, format_int=format_int, user=user)

@router.get("/register", response_class=HTMLResponse, summary='Отображение страницы регистрации')
async def register(request: Request):
    return render_template('register.html', request=request)

@router.get("/admin", response_class=HTMLResponse, summary='Отображение страницы администратора')
async def admin_index(request: Request, user: User = Depends(get_authorized),
                      db: Session = Depends(get_db)):
    if not user.is_admin:
        return RedirectResponse(url='/')
    return render_template('admin.html', users=UserCRUD.get_all(db), user=user, request=request)

@router.get('/admin/history/{user_id}', response_class=HTMLResponse, summary='Отображение истории запросов пользователя')
async def admin_history(request: Request, user: User = Depends(get_authorized),
                        db: Session = Depends(get_db),
                        user_id: int = Path(..., description='ID пользователя'),
                        page: int = Query(1, description='Номер страницы')):
    if page < 1:
        page = 1
    if not user.is_admin:
        return RedirectResponse(url='/')
    return render_template('admin_history.html',
                           user=user,
                           request=request,
                           logs=LogEntryCRUD.get_history(db, user_id, (page - 1) * 10, 10, False),
                           page=page)

@router.get('/admin/search/{block_id}', response_class=HTMLResponse, summary='Отображение страницы поиска блока')
async def admin_search(request: Request, user: User = Depends(get_authorized), block_id: int = Path(..., description='ID блока')):
    if not user.is_admin:
        return RedirectResponse(url='/')
    return render_template('admin_search.html', user=user, request=request, block_id=block_id)

@router.get("/logout", response_class=RedirectResponse, summary='Выход из аккаунта')
async def logout():
    resp = RedirectResponse(url='/')
    resp.delete_cookie(key='token')
    return resp

@router.get('/search/{block_id}', response_class=HTMLResponse, summary='Отображение результата поиска')
async def search(request: Request,
                 user: User | None = Depends(get_authorized),
                 block_id: int = Path(..., description='ID блока в сети BTC')):
    return render_template('search.html', request=request, user=user, block_id=block_id)

@router.get('/history', response_class=HTMLResponse, summary='Отображение истории поиска')
async def history(request: Request,
                  user: User | None = Depends(get_authorized),
                  db: Session = Depends(get_db),
                  page: int = Query(1, description='Номер страницы')):
    if page < 1:
        page = 1
    logs = LogEntryCRUD.get_history(db, user.id, (page - 1) * 10, 10)
    return render_template('history.html', request=request, user=user, logs=logs, page=page)
