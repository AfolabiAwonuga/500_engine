FROM python:3.9-slim-buster  AS Builder

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && python -m pip install --upgrade pip \
    && pip install --default-timeout=200 --no-cache-dir \
    --target=/app/dependencies -r requirements.txt \
    && rm -rf /var/lib/apt/lists/* 

COPY . .

FROM python:3.9-slim-buster 

WORKDIR /app

COPY --from=Builder	/app .

ENV PYTHONPATH="${PYTHONPATH}:/app/dependencies"

RUN python -m nltk.downloader punkt \
    && python -m nltk.downloader stopwords 

CMD ["python", "inverted_index.py"]