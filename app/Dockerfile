FROM python:3.6
WORKDIR /service
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . ./
EXPOSE 8080
ENTRYPOINT ["python3", "api.py"]