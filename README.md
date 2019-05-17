# About

A dockerized library card application form. Uses Python, Flask, and the Sierra API (v5+).

# Environment Variables

Copy ```env-example.conf``` to a new file ```.env``` in the project root, and set the variables to suit your installation.

# Testing (Linux)

__Start debug SMTP server:__

```
sudo python -m smtpd -n -c DebuggingServer localhost:25
```

__Build and run Docker image:__

```
docker build -t card-app .
docker run --rm --env-file .env --net="host" --name card-app card-app
```

__View the application:__

Browse to `http://localhost/card`.
