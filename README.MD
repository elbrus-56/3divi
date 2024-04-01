# Приложение
Версия Python 3.11.4
Приложение использует асинхронный веб-сервер `aiohttp`

## Запуск
Активировать виртуальное окружение: `python-m venv venv`
Нужно выполнить команду: `pip install -r requirements.txt`

Последовательный запуск сервисов

### Клиент
`python -m client client:app;`

### Сервер
`python -m server server:app;`

### Обработчик
`python -m process process:app;`

### Сохранение
`python -m save save:app;`


## Параметры URL для передачи клиенту
`http://127.0.0.1:5000/?connection_count=100&connection_value=100&delay_range=5`

По-умолчанию ззначения параметров:
connection_count = 10
connection_value =  10
delay_range = 5



## Запуск в докере
### Запуск в docker compose

`docker-compose up --build`

Внимание! Нужно учесть, что внутри контейнеров будут происходить API вызовы и URL соттвествует имн вызываемго контейнера.

Если нужно запустить без докера, нужно править URL.


Выполнить 4 команды для сборки образов:

1. `docker build -t client_app -f Client.Dockerfile .`
2. `docker build -t server_app -f Server.Dockerfile .`
3. `docker build -t process_app -f Process.Dockerfile .`
4. `docker build -t save_app -f Save.Dockerfile .`

Выполнить для запуска контейнеров:

1. `docker run --rm -p 5000:5000 --net=host client_app:latest`
2. `docker run --rm -p 5001:5001 --net=host server_app:latest`
3. `docker run --rm -p 5001:5001 --net=host process_app:latest`
4. `docker run --rm -p 5003:5003 --net=host --volume=${PWD}:/app  save_app:latest`




## TODO
При разработке отталкивался от принципа, все что не запрещено, то разрешено.
Суммарно ушел день на реализацию подобного сервиса и то с оговоркой, что я его сделал не совсем в соответствии с ТЗ.
Что нужно было делать понятно. Самое сложное писать задачи в файл в правильном порядке. В идеале, нужно использовать было бы очередь типа Celery.
Попробовал обойтись без этого, но не вышло. Потратил на это все время.

Как вараинт, можно было бы делать 2 запроса клиентом: 1 Запрос для обработчика, 2 запрос Сервису записи. Но по условию ТЗ, обработчик возвращает `{'asyncAnswer': 'Ok'}` и искусственная сортировка по времени уже невозможна была бы.

TODO Написать Docker образы (Объединить в докер compose). Проверить `url` в коде.
TODO Написать тесты
TODO Подумать еще, как можно было асинхронный хаос преватить в упорядоченную запись без селери и можно ли вообще
