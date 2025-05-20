FROM python:3.10.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY templates /app/templates

COPY static /app/static

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]