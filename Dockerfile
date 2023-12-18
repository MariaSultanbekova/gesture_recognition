FROM python:3.10.12

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1-mesa-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000", "--reload"]
