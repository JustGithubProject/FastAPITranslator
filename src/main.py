import requests
from fastapi import FastAPI
from fastapi import Request
from fastapi import Form
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")

languages_lst = ["Russian", "English", "Polish", "Ukrainian", "Italian", "French", "Czech", "German", "Greek", "Uzbek",
                 "Latvian", "Spanish", "Turkish", "Serbian", "Estonian", "Armenian", "Azerbaijani", "Belarusian",
                 "Persian", "Bulgarian"]
lang_symbols = ["ru", "en", "pl", "uk", "it", "fr", "cs", "de", "el", "uz", "lv", "es", "tr", "sr", "et", "hy", "az",
                "be", "fa", "bg"]
languages_dict = dict(zip(languages_lst, lang_symbols))


@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "languages": languages_lst})


@app.post("/translate")
def translate_text(request: Request, text: str = Form(...), target_language: str = Form(...)):
    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"
    payload = {
        "q": text,
        "format": "text",
        "target": languages_dict[target_language]
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "application/gzip",
        "X-RapidAPI-Key": "8c19b34a82msh864a87611671af9p18308ajsn88a0c7fd4a28",
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
    }
    response = requests.post(url, data=payload, headers=headers)
    res = response.json()
    translated_text = res["data"]["translations"][0]["translatedText"]
    return templates.TemplateResponse("index.html",
                                      {"request": request, "translation": translated_text, "languages": languages_lst})
