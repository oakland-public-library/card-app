# About

A library card application form for patrons, leveraging the Sierra REST API (v5 or higher).

# Environment Variables

Configuration variables from the file ```.env``` will be used to configure the application when its Docker image is built. Copy ```env-example.conf``` to a new file ```.env``` in the project root, setting values to suit your particular installation.

# Deploy with Docker

Use docker-compose to build and run the application, along with a debug SMTP server to handle the confirmation emails (message content will appear in the console log):

```
docker-compose up --build
```

# Local Testing with gunicorn and aiosmtpd

Create a Python virtual environment with requisite packages:

```
python3 -m venv env
pip3 install gunicorn aiosmtpd wtforms oauthlib requests requests_oauthlib flask flask_mail
```

Simulate a production SMTP server to view confirmation emails sent to patrons. From a separate terminal:

```
sudo aiosmtpd -n -d -l 0.0.0.0:25
```

Run the application from within the source directory:

```
cd src
gunicorn --reload -b 0.0.0.0:8888 main:app
```

# View the Application

Browse to `http://localhost:8888/card`.

# Preload Form Data

Append `preload` to the query string: `http://localhost:8888/card?preload`.
