FROM python:3.10

ADD main.py .
ADD requirements.txt .
ADD service_client_secret.json .

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]