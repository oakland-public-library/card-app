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

Simulate a production SMTP server to view confirmation emails sent to patrons (run from a separate terminal):

```
sudo pip install aiosmtpd
sudo aiosmtpd -n -d -l 0.0.0.0:25
```

Run the application from within the source directory:

```
cd src
gunicorn --reload -b 0.0.0.0:8888 main:app
```

# View the Application

Browse to `http://localhost:8888/card`.

# Preload form data

Append `preload` to the query string: `http://localhost:8888/card?preload`.
