from fastapi import FastAPI
from utils import *
from typing import Dict, Any
import urllib, uvicorn, re, chromedriver_binary


app = FastAPI()

@app.post("/google_question")
def google_question(req: Dict[Any, Any] = None):
    kw = req['kw']
    uule = req['uule']
    cant_clicks = req['clicks']
    lang = req['lang']
    country = req['country']
    query = urllib.parse.quote(str(kw))
    base_url = 'https://www.google.com/search?q='
    url = f'{base_url}{query}&hl={lang}&gl={country}&uule={uule}'
    response = getGoogleQuestions(url, cant_clicks)
    if response:
        return {kw: [q for q in response]}
    else:
        return {kw: ["Nothing Found"]}

if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
