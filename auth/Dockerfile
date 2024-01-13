FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY auth_service.py .
COPY static .
COPY templates .

EXPOSE 30091

CMD ["python", "auth_service.py"]
