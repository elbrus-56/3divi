import asyncio
import functools
import json
import random
from threading import current_thread
import uuid
from aiohttp import web
import concurrent.futures

import requests
import logging


logging.basicConfig(
    format="[%(asctime)s] [%(name)s] [%(levelname)s] - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger("client")


def sync_make_request(payload):
    url = "http://server:5001/handler"
    thread = current_thread()
    logger.info(f"TREAD: {thread.name}, DATA: {payload}")
    response = requests.post(url, data=json.dumps(payload))
    return response.json()


async def handle(request):
    connection_count = request.rel_url.query.get("connection_count") or 10
    connection_value = request.rel_url.query.get("connection_value") or 10
    delay_range = request.rel_url.query.get("delay_range") or 5

    loop = asyncio.get_running_loop()
    payloads = [
        {
            "request": {
                "id": str(uuid.uuid4()),
                "delay": random.randrange(int(delay_range)),
            }
        }
        for _ in range(int(connection_value))
    ]
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=int(connection_count)
    ) as pool:
        tasks = [
            loop.run_in_executor(
                pool,
                functools.partial(sync_make_request, payload),
            )
            for payload in payloads
        ]
        results = await asyncio.gather(*tasks)

    return web.Response(body=str(results))


app = web.Application()
app.add_routes([web.get("/", handle)])

if __name__ == "__main__":
    web.run_app(app, port=5000)
