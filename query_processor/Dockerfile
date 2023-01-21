FROM python:3.9-slim-buster 

EXPOSE 8501

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && python -m pip install --upgrade pip \
    && pip install --default-timeout=200 --no-cache-dir -r requirements.txt \
    && python -m nltk.downloader punkt \
    && python -m nltk.downloader stopwords \
    && rm -rf /var/lib/apt/lists/* 

COPY . .

CMD ["streamlit", "run", "query_processor.py"]
