import json
from queue import Queue
import random
from threading import Thread, current_thread
import uuid
from aiohttp import web

import requests
import logging


logging.basicConfig(
    format="[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("client")

queue = Queue()


def sync_make_request(payload: dict):
    url = "http://server:5001/handler"
    thread = current_thread()
    logger.info(f"TREAD: {thread.name}, DATA: {payload}")
    response = requests.post(url, data=json.dumps(payload))
    return response.json()


def put_queue(payloads: list):
    for payload in payloads:
        queue.put(payload)
    print(queue.qsize())


def get_queue():
    while True:
        item = queue.get()
        if item is None:
            break
        sync_make_request(item)
        queue.task_done()


async def handle(request):
    connection_count = request.rel_url.query.get("connection_count") or 5
    connection_value = request.rel_url.query.get("connection_value") or 10
    delay_range = request.rel_url.query.get("delay_range") or 5

    payloads = [
        {
            "request": {
                "id": str(uuid.uuid4()),
                "delay": random.randrange(int(delay_range)),
            }
        }
        for _ in range(int(connection_value))
    ]

    put_queue(payloads)

    for i in range(connection_count):
        print(connection_count)
        thread = Thread(target=get_queue)
        thread.start()

    return web.Response(body=json.dumps({"asyncAnswer": "Ok"}))


app = web.Application()
app.add_routes([web.get("/", handle)])


if __name__ == "__main__":
    web.run_app(app, port=5000)
