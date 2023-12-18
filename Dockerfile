FROM python:3.10.12
WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app/src
EXPOSE 8000
CMD ["python3", "main.py"]
