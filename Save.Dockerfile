# ######################## Base stage ##########################
FROM python:3.11-slim-bullseye as base
LABEL maintainer="elbrus56@mail.ru"
LABEL vendor="Eldar Idiyatullin"

WORKDIR /app
RUN pip install --upgrade pip setuptools wheel

# Обновляем пакетный менеджер
RUN apt-get update -y && apt-get upgrade -y

# Ставим зависимости GDAL, PROJ
# RUN apt-get install -y gdal-bin libgdal-dev
# RUN apt-get install -y python3-gdal
# RUN apt-get install -y binutils libproj-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod 755 /app

CMD ["python", "-m", "save", "save:app"]
