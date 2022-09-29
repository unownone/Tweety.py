FROM python:3.9.7-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/app


COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

WORKDIR /app

USER app

COPY . .

EXPOSE 80

CMD uvicorn --reload app:app --host 0.0.0.0 --port 80