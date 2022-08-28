FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

CMD ["python3.10", "-m", "uvicorn", "main:app", "--port", "8080", "--host", "0.0.0.0"]
