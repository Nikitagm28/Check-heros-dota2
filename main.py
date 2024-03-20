from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from scraper import get_hero_info, get_hero_counters

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/info", response_class=HTMLResponse)
def post_hero_info(request: Request, hero_name: str = Form(None)):
    if hero_name is None or not hero_name.strip():
        return templates.TemplateResponse("index.html", {"request": request, "error": "Пожалуйста, введите имя героя."})
    try:
        hero_info = get_hero_info(hero_name)

        if 'error' in hero_info:
            raise HTTPException(status_code=404, detail=hero_info['error'])
        return templates.TemplateResponse("index.html", {"request": request, "info": hero_info, "hero_name": hero_name})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/counter", response_class=HTMLResponse)
def post_hero_counters(request: Request, hero_name: str = Form(None)):
    if hero_name is None or not hero_name.strip():
        return templates.TemplateResponse("index.html", {"request": request, "error": "Пожалуйста, введите имя героя."})
    
    try:
        hero_counters = get_hero_counters(hero_name)
        if 'error' in hero_counters:
            raise HTTPException(status_code=404, detail=hero_counters['error'])
        return templates.TemplateResponse("index.html", {"request": request, "counters": hero_counters, "hero_name": hero_name})
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
