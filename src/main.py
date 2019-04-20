# flask and forms
from flask import Flask, request, render_template
from wtforms import Form, StringField, IntegerField, BooleanField, RadioField, FormField
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

# debug
import pprint
pp = pprint.PrettyPrinter(indent=4)

API_KEY = os.environ['SIERRA_API_KEY']
API_SECRET = os.environ['SIERRA_API_SECRET']
API_URL_BASE = os.environ['SIERRA_API_URL_BASE']

SMTP_HOST = os.environ['SMTP_HOST']
SMTP_USER = os.environ['SMTP_USER']

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

class BirthDate(Form):
    month = IntegerField('Month', [DataRequired(), Length(max=2)])
    day = IntegerField('Day', [DataRequired(), Length(max=2)])
    year = IntegerField('Year', [DataRequired(), Length(min=4, max=4)])

class Name(Form):
    last = StringField('Last', [DataRequired(), Length(max=20)])
    first = StringField('First', [DataRequired(), Length(max=20)])
    initial = StringField('Middle Initial', [DataRequired(), Length(max=1)])

class Address(Form):
    addr_num = IntegerField('Number', [DataRequired(), Length(max=10)])
    street = StringField('Street', [DataRequired(), Length(max=20)])
    apt_num = StringField('Apartment Number', [DataRequired(), Length(max=20)])
    city = StringField('City', [DataRequired(), Length(max=20)])
    state = StringField('State', [DataRequired(), Length(max=20)])
    zip_code = StringField('Zip Code', [DataRequired(), Length(max=10)])
    
class RegForm(Form):
    birth_date = FormField(BirthDate)
    age_range = RadioField('Age', choices = [('child1', 'Child 0-7'),
                                             ('child2', 'Child 8-12'),
                                             ('teen', 'Teen 13-17'),
                                             ('adult', 'Adult 18+')])
    name = FormField(Name)
    address = FormField(Address)
    phone = StringField('Telephone', [DataRequired(), Length(max=20)])
    email = StringField('Email', [DataRequired(), Length(max=20)])
    school = StringField('School (optional)', [DataRequired(), Length(max=20)])
    id_num = StringField('ID (see below for details)', [DataRequired(), Length(max=20)])
    want_ext_svc = BooleanField('Want Extended Services', [DataRequired()])
    want_teacher_card = BooleanField('Want Teacher Card', [DataRequired()])
    want_dsg_borrower = BooleanField('Want Designated Borrower', [DataRequired()])
    dsg_borrower = StringField('Designated Borrowers', [DataRequired(), Length(max=20)])
    parent_sig = StringField('Parent/Legal Guardian’s Signature', [DataRequired(), Length(max=20)])
    parent_name = StringField('Parent/Legal Guardian’s Name', [DataRequired(), Length(max=20)])
    
app = Flask(__name__)

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    form = RegForm(request.form)
    pp.pprint(request.form)
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

@app.route('/email', methods=['GET', 'POST'])
def email():
    form = RegForm(request.form)
    form.patron_name.first = 'foo'
    return render_template('email.html', form=form)
