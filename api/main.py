from fastapi import FastAPI
from models import Base, engine
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from cache import cache
from utils import get_crypt_course_online, get_usd_course_online

from models.user import User
Base.metadata.create_all(bind=engine)
cache.set('course', get_crypt_course_online)
cache.set('usd', get_usd_course_online)

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')
class RenderTemplate:
    def __init__(self, tmpl: Jinja2Templates):
        self.templates = tmpl
    def render_template(self, template_name: str, **context):
        return self.templates.TemplateResponse(template_name, context)
render_template = RenderTemplate(templates).render_template

from routes import render
from routes import api
app.include_router(render.router)
app.include_router(api.router)


