FROM python:3.9-slim

WORKDIR /app
COPY ./app /app
RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1

EXPOSE 5123

CMD ["python", "db-api.py"]