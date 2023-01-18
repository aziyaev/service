FROM python:latest

WORKDIR /app

COPY requirements.txt ./
ADD src ./

RUN pip3 install -r requirements.txt && rm requirements.txt

ENTRYPOINT ["python3", "main.py"]
