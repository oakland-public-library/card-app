FROM python:3.7-alpine as base

FROM base as builder

RUN mkdir /install
WORKDIR /install

COPY requirements.txt /requirements.txt

RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base

COPY --from=builder /install /usr/local
COPY src /app

WORKDIR /app

EXPOSE 80

CMD ["gunicorn", "-w 4", "-b 0.0.0.0:80", "main:app"]

