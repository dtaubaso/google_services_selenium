from fastapi import FastAPI
from utils import *
from typing import Dict, Any
import urllib, uvicorn, re, os
import firebase_admin
from firebase_admin import credentials, db


def get_webhook():
    if not firebase_admin._apps:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://nmd-firebase-default-rtdb.firebaseio.com',
            'name': 'fbapp'
        })

    ref = db.reference('/acceso')
    data = ref.get()
    return data.get('error_webhook', None)

webhook_url = get_webhook()


app = FastAPI()

@app.post("/google-question")
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
        text = f'*Google People Also Ask* Error: {e}'
        send_slack(text, webhook_url)

@app.post("/people-also-search")
def people_also_search(req: Dict[Any, Any] = None):
    kw = req['kw']
    uule = req['uule']
    lang = req['lang']
    country = req['country']
    query = urllib.parse.quote(str(kw))
    base_url = 'https://www.google.com/search?q='
    url = f'{base_url}{query}&hl={lang}&gl={country}&uule={uule}'
    print(f'kw: {kw}, url: {url}')
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

@app.post("/get-body")
def get_page_body(req: Dict[Any, Any] = None):
    url = req['url']
    try:
        response = return_body(url)
        return response
    except Exception as e:
        print(e)
        text = f'*Get Body* Error: {e}'
        send_slack(text, webhook_url)


if __name__ == '__main__':
    uvicorn.run(app=app, host="127.0.0.1", port=8000)
