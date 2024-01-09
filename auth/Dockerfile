FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY auth_service.py .

EXPOSE 5001

CMD ["python", "auth_service.py"]
