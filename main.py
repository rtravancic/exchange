from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import  StaticFiles
import requests
from bs4 import BeautifulSoup
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_price(symbol: str) -> float:
    url = f"https://finance.yahoo.com/quote/{symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    price = soup.find("fin-streamer", {"data-field": "regularMarketPrice"})
    return float(price.text.replace(",", ""))

@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/prices")
async def get_prices():
    try:
        gold = get_price("GC=F")
        silver = get_price("SI=F")
        sp500 = get_price("^GSPC")
        return {"gold": gold, "silver": silver, "sp500": sp500}
    except Exception as e:
        return JSONResponse (content={"error": str(e)}, status_code=500)
