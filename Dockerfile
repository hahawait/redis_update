FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install redis python-dotenv

WORKDIR /app

COPY . /app

CMD ["python", "main.py"]
