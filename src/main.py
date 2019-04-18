# flask and forms
from flask import Flask, request, render_template
from wtforms import Form, StringField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length

# sierra api
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from datetime import datetime
import json

# access secrets passed to env by e.g. docker
import os
API_KEY = os.environ['SIERRA_API_KEY']
API_SECRET = os.environ['SIERRA_API_SECRET']
API_URL_BASE = os.environ['SIERRA_API_URL_BASE']

patron_data = {
    # "expirationDate": str(expiration_date) set to arbitrary past date,
        "expirationDate": '2013-03-28',
    "patronCodes": {
        # age level
            "pcode1": "1",
        # not used for online reg
            "pcode2": "-",
        # library jurisdiction
            "pcode3": 1
    },
    "varFields": [{
        # school
            "fieldTag": "c",
        "content": "SIERRA ELEMENTARY"
    },
                  {
                      # unique ID
                "fieldTag": "u",
                      "content": "CS{}".format(datetime.now().strftime('%y%m%d%H%M%S'))
                  },
                  {
                      # parent name
                "fieldTag": "e",
                      "content": "TEST PARENT"
                  },
                  {
                      # language
                "fieldTag": "k",
                      "content": "MALTESE"
                  },
                  {
                      # self reg info
                "fieldTag": "d",
                      "content": "|t ID_PASSPORT"
                  },
    ]
    ,
    "patronType": 18,
    # "birthDate": str(birth_date),
    # dates should be in the format YYYY-MM-DD
        "birthDate": '2006-12-01',
    # Home Library
        "homeLibraryCode": 'xxa',
    "names": [
        'PATLASTNAME' + ', ' + 'PATFIRSTNAME' + ' ' + 'M'
    ],
    # 3 lines if apt number exists, else 2 lines
        "addresses": [{
            "lines": [
                '125 14TH ST',
                'APT 2',
                'OAKLAND, CA 94612'
            ],
            "type": "a"
        }],
    # format xxx-xxx-xxxx
        "phones": [{
            "number": '510-999-9999',
            "type": "t"
        }],
    "emails": [
        "devnullexplorer@aol.com"
    ],
}

def authenticate(api_key, api_secret):
    auth = HTTPBasicAuth(api_key, api_secret)
    client = BackendApplicationClient(client_id=api_key)
    session = OAuth2Session(client=client)
    session.fetch_token(token_url=API_URL_BASE + '/token', auth=auth)
    return session

def create_patron(session, patron_data):
    url = '/patrons/'
    headers = {'content-type': 'application/json'}
    data = json.dumps(patron_data)
    r = session.post(API_URL_BASE + url, data=data, headers=headers)
    record_id = json.loads(r.text)['link'].split('/')[-1]
    return record_id   

app = Flask(__name__)

class RegForm(Form):
    name = StringField('Name', [DataRequired(), Length(min=2, max=20)])
    
@app.route('/apply', methods=['GET', 'POST'])
def login():
    form = RegForm(request.form)
    if not request.form:
        # set form defaults here
        form.process()
    if request.method == 'POST' and form.validate():
        session = authenticate(API_KEY, API_SECRET)
        rec = create_patron(session,patron_data)
        print(rec)
        #return render_template('success.html', form=form)
    return render_template('card-app.html', form=form)
