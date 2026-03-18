FROM python:3.10.12
WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    git

COPY ./app/ ./
COPY requirements.txt ./requirements.txt 

RUN pip3 install -r requirements.txt
EXPOSE 8501 

ENTRYPOINT ["streamlit", "run", "src/home.py", "--server.port=8501", "--server.address=0.0.0.0"]

