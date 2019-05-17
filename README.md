# About

A dockerized library card application form. Uses Python, Flask, Sierra API.

# Environment Variables

These environment variables must be set to configure the application:

- `SIERRA_API_URL_BASE`- Sierra API URL, e.g. https://catalog.yourlibrary.org/iii/sierra-api/v5
- `SIERRA_API_KEY`- Sierra API Key
- `SIERRA_API_SECRET`- Sierra API secret
- `SMTP_HOST` - SMTP server host name
- `SMTP_USER` - Confirmation email "from" address

# Testing

Install required packages:

```
pip install -r requirements.txt
```

Start debug SMTP server:

```
sudo python -m smtpd -n -c DebuggingServer localhost:25
```

Serve application form locally using gunicorn:

```
cd src
gunicorn --reload -b 0.0.0.0:8000 main:app
```
