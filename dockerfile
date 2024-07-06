FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    python3-venv \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

COPY . .

CMD ["python3", "src/main.py"]
