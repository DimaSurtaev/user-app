FROM python:3.10.11

RUN apt-get update && apt-get install -y netcat

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY templates /app/templates

COPY static /app/static

COPY app.py .

ENV FLASK_APP=app.py
ENV FLASK_ENV=development

EXPOSE 5000

CMD ["python", "app.py"]