from fastapi import FastAPI
from utils import *
from typing import Dict, Any
import urllib, uvicorn, re

webhook_url = "https://hooks.slack.com/services/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"

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
    try:
        response = getGoogleQuestions(url, cant_clicks)
        if response:
            return {kw: [q for q in response]}
        else:
            return {kw: ["Nothing Found"]}
    except Exception as e:
        print(e)
        text = f'*Google Questions* Error: {e}'
        send_slack(text, webhook_url)

@app.post("/people_also_search")
def people_also_search(req: Dict[Any, Any] = None):
    kw = req['kw']
    uule = req['uule']
    lang = req['lang']
    country = req['country']
    query = urllib.parse.quote(str(kw))
    base_url = 'https://www.google.com/search?q='
    url = f'{base_url}{query}&hl={lang}&gl={country}&uule={uule}'
    try:
        response = getRelated(url)
        if response:
            return {kw: [q for q in response]}
        else:
            return {kw: ["Nothing Found"]}
    except Exception as e:
        print(e)
        text = f'*Google People Also Search* Error: {e}'
        send_slack(text, webhook_url)

if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
