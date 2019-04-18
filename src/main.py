# flask and forms
from flask import Flask, request, render_template
from wtforms import Form, StringField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length

# interact with sierra API
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from datetime import datetime
import json

# get configuration passed through environment variables (e.g. by docker)
import os

# confirmation email
from flask_mail import Mail, Message

API_KEY = os.environ['SIERRA_API_KEY']
API_SECRET = os.environ['SIERRA_API_SECRET']
API_URL_BASE = os.environ['SIERRA_API_URL_BASE']

SMTP_HOST = os.environ['SMTP_HOST']
SMTP_USER = os.environ['SMTP_USER']

# birth date: month, day, year
# age range: child (0-7), child (8-12), teen (13-17), adult (18+)
# name: last, first, middle initial
# address: number, street, apt number, city, state, zip code
# telephone: area code, number
# email address
# school (optional)
# ID number (use drop-down for type)
# languages (use note?)
# want extended services? (checkbox)
# want teacher card? (checkbox)
# want designated borrower? (checkbox)
# designated borrower: name
# parent signature (0-12 only)
# parent name (0-12 only)

patron_data = {
    # "expirationDate": str(expiration_date) set to arbitrary past date,
        "expirationDate": '2001-01-01',
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
                      "content": "CS{}".format(
                          datetime.now().strftime('%y%m%d%H%M%S'))
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

def patron_record_by_id(session, record_id):
    patron_api_fields = {'fields': 'emails,names,homeLibraryCode'}
    r = session.get(API_URL_BASE + '/patrons/{}'.format(str(record_id)),
                    params=patron_api_fields)
    return json.loads(r.text)

def send_email(record):
    patron_name = record['names'][0]
    home_code = record['homeLibraryCode']
    subject = 'Yout New Library Card'
    sender = SMTP_USER
    msg = Message(subject, sender=sender, recipients=record['emails'])
    msg.body = render_template('email.txt', name=patron_name)
    msg.html = render_template('email.html', name=patron_name)
    mail = Mail(app)
    mail.send(msg)

class RegForm(Form):
    name = StringField('Name', [DataRequired(), Length(min=2, max=20)])

app = Flask(__name__)

@app.route('/apply', methods=['GET', 'POST'])
def login():
    form = RegForm(request.form)
    if not request.form:
        # set form defaults here
        form.process()
    if request.method == 'POST' and form.validate():
        # session = authenticate(API_KEY, API_SECRET)
        # record_id = create_patron(session, patron_data)
        # record = patron_record_by_id(session, record_id)

        # for testing: load patron record from file
        with open('test_record.json', 'r') as infile:
            record = json.load(infile)

        send_email(record)
        #return render_template('success.html', form=form)
    return render_template('card-app.html', form=form)
