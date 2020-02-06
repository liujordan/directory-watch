FROM python:3.7.2-slim

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT python
CMD ./app.py
