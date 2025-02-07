FROM python:3.12-slim-bullseye

USER root
WORKDIR /app
COPY . /app
EXPOSE 8000

RUN apt-get update && apt-get install -y \
    unixodbc \
    unixodbc-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn","-w", "4", "-b", "0.0.0.0:8000", "--timeout", "0", "app:create_app()"]

