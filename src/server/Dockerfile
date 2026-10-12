FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
COPY dist ./dist
COPY ./src/server ./src/server

RUN pip install -r requirements.txt

CMD ["python","src/server/server.py"]

EXPOSE 8000

