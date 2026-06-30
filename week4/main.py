from typing_extensions import Annotated
import urllib.request
import re
import json

from fastapi import FastAPI, Request , Form ,status
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
templates = Jinja2Templates(directory="templates")


hotels_cn_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
hotels_en_url = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"

data_cn = urllib.request.urlopen(hotels_cn_url, data=None, context=None).read().decode('utf-8')
data_en = urllib.request.urlopen(hotels_en_url, data=None, context=None).read().decode('utf-8')
j_h_cn : list = json.loads(data_cn)["list"]
j_h_en : list= json.loads(data_en)["list"]
total_hotels_list = {}
cn_map = {item["_id"]: item for item in j_h_cn}
for x in j_h_en:
    cn_x = cn_map[x["_id"]]
    if cn_x :
        total_hotels_list[x["_id"]] = (cn_x["旅宿名稱"].strip(),x["hotel name"].strip(),cn_x["電話或手機號碼"])

@app.middleware("http")
async def setlog(request: Request, call_next):
    is_login = request.session.get("LOGGED-IN", False)

    if is_login and request.url.path not in ("/member", "/logout"):
        return RedirectResponse(url="/member", status_code=status.HTTP_303_SEE_OTHER)
    
    response = await call_next(request)
    return response

app.add_middleware(
    SessionMiddleware,
    secret_key="唐祥豪",
    session_cookie="session",
    max_age=1800
)

@app.get("/",response_class=HTMLResponse)
def home(request: Request):
    data ={
        "sitetitle": "主頁",
        "title":"歡迎光臨，請輸入帳號密碼",
        "is_home":True,
        "is_login":False,
        "message":""
    }
    return templates.TemplateResponse(request=request,name="template.html",context={"data":data})


@app.post("/login",response_class=RedirectResponse)
def login(request: Request,email: Annotated[str, Form()], password: Annotated[str, Form()],allow: Annotated[bool, Form()] = False):
    target_email = "abc@abc.com"
    target_password = "abc"
    if (email == target_email) and (password == target_password):
        request.session["LOGGED-IN"] = True
        return RedirectResponse(url="/member", status_code=status.HTTP_303_SEE_OTHER)
    
    return RedirectResponse(url="/ohoh?msg=帳號或密碼輸入錯誤", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/logout")
def logout(request: Request):
    request.session["LOGGED-IN"] = False
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@app.get("/member")
def member(request: Request):
    print(request.session["LOGGED-IN"])
    if not request.session.get("LOGGED-IN",False):
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    data ={
        "sitetitle": "結果頁",
        "title":"歡迎光臨，這是會員頁",
        "is_home":False,
        "is_login":True,
        "message":"恭喜您，成功登入系統！"
    }
    return templates.TemplateResponse(request=request,name="template.html",context={"data":data})


@app.get("/ohoh")
def failed(request: Request,msg:str = "帳號、或者密碼輸入錯誤"):
    data ={
        "sitetitle": "結果頁",
        "title":"失敗頁",
        "is_home":False,
        "is_login":False,
        "message":msg
    }
    return templates.TemplateResponse(request=request,name="template.html",context={"data":data})

@app.get("/hotel/{id}")
def hotel(request:Request,id:int):

    ans  = total_hotels_list.get(id)

    data ={
        "sitetitle": "旅館資訊",
        "title":"旅館的資訊",
        "is_home":False,
        "is_login":False,
        "message":", ".join(ans) if ans else "查詢不到相關資料"
    }
    return templates.TemplateResponse(request=request,name="template.html",context={"data":data})
