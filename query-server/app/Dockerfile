FROM python:3.9-slim

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY app.py /app

EXPOSE 8123

CMD ["python", "app.py"]