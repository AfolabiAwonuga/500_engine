FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt 

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt 

COPY . .

RUN playwright install \
    && playwright install-deps 

CMD ["python", "run_spiders.py"]
