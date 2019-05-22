# About

A dockerized library card application form. Uses Python, Flask, and the Sierra API (v5+).

# Environment Variables

Configuration variables from the file ```.env``` will be used to configure the application when its Docker image is built. Copy ```env-example.conf``` to a new file ```.env``` in the project root, setting values to suit your particular installation.

# Build and Run Docker Images

Use docker-compose to build and run the application, along with a debug SMTP server to handle the confirmation emails (message content will appear in the console log):

```
docker-compose up --build
```

# View the Application

Browse to `http://localhost:8080/card`.
