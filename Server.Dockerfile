# ######################## Base stage ##########################
FROM python:3.11-slim-bullseye as base
LABEL maintainer="elbrus56@mail.ru"
LABEL vendor="Eldar Idiyatullin"

WORKDIR /app
RUN pip install --upgrade pip setuptools wheel

# Обновляем пакетный менеджер
RUN apt-get update -y && apt-get upgrade -y

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "-m", "server", "server:app"]
