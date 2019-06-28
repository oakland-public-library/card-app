# OS interaction and debugging
import os
import json
import pprint
import logging

# flask and forms
from flask import Flask, request, render_template
from wtforms import Form, StringField, IntegerField, BooleanField, RadioField, FormField
from wtforms.validators import DataRequired, Length

# interact with sierra API
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
from datetime import datetime
from flask_mail import Mail, Message

# test routines and mock data
import test

app = Flask(__name__)
app.config['DEBUG'] = True

pp = pprint.PrettyPrinter(indent=4)

API_KEY = os.environ.get('SIERRA_API_KEY', 'NONE')
API_SECRET = os.environ.get('SIERRA_API_SECRET', 'NONE')
API_URL_BASE = os.environ.get('SIERRA_API_URL_BASE', 'NONE')

SMTP_HOST = os.environ.get('SMTP_HOST', 'localhost')
SMTP_USER = os.environ.get('SMTP_USER', 'root')

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
    app.logger.info('sending confirmation email')
    patron_name = record['names'][0]
    home_code = record['homeLibraryCode']
    subject = 'Your New Library Card'
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

def form_export_record(form):
    app.logger.info('exporting patron record')
    return test.mock_record()

@app.route('/card', methods=['GET', 'POST'])
def apply():
    app.logger.info('{} {}'.format(request.method, request.url))
    form = RegForm(request.form)
    if not request.form and 'preload' in request.args:
        app.logger.info('populating form with mock data')
        app.logger.info(form.data.keys())
        test.form_fill(form)
    if request.method == 'POST' and form.validate():
        app.logger.info('form validated successfully')
        record = form_export_record(form)
        create_patron(authenticate(API_KEY, API_SECRET), record)
        send_email(record)
        return render_template('success.html', form=form)
    return render_template('card-app.html', form=form)

@app.route('/email', methods=['GET', 'POST'])
def email():
    form = RegForm(request.form)
    form.name.first = "Patron's Name"
    return render_template('email.html', form=form)
