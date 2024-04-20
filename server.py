from concurrent.futures import ThreadPoolExecutor
import datetime
import json
from queue import Queue
from threading import Thread, current_thread
from aiohttp import web
import logging

import aiohttp
import requests


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Thread")


queue = Queue()


async def async_make_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(data)) as resp:
            return await resp.text()


def sync_make_request(payload: dict):
    c = current_thread()
    logging.info(f"current_tread=> {c}")
    url = "http://process:5002/sleeper"
    response = requests.post(url, data=json.dumps(payload))
    return response.text


def put_queue(payloads: list):
    for payload in payloads:
        queue.put(payload)
    print(queue.qsize())


def get_queue():
    # while True:
    item = queue.get()
    # if item is None:
    #     break
    sync_make_request(item)
    queue.task_done()


async def handle(request):
    _ts = datetime.datetime.now()
    logging.info(f"recieve_time=> {_ts}")
    data = await request.json()
    logging.info(f"data=> {data}")
    res = await async_make_request("http://process:5002/sleeper", data)
    # queue.put(data)
    # logging.info(f"qsize=> {queue.qsize()}")
    # thread = Thread(target=sync_make_request, args=(data))
    # thread.start()
    # thread.join()
    # with ThreadPoolExecutor() as executor:
    #     future = executor.submit(sync_make_request, data)
    #     logging.info(future.result())
    _te = datetime.datetime.now()
    logging.info(f"process_time=> {_te}")
    # recieve_msg = {
    #     "id": data["request"]["id"],
    #     "time_from": str(_ts),
    # }
    # await async_make_request("http://save:5003/save_2", recieve_msg)
    # await async_make_request("http://process:5002/sleeper", data)
    # _te = datetime.datetime.now()
    # print(f"end, {data} => {_te}")
    result_msg = {
        "id": data["request"]["id"],
        "time_from": str(_ts),
        "time_to": str(_te),
        "data": data
    }
    logging.info(result_msg)
    # await async_make_request("http://save:5003/save_1", result_msg)
    return web.Response(body=json.dumps({"asyncAnswer": "Ok"}))


app = web.Application()
app.add_routes([web.post("/handler", handle)])

if __name__ == "__main__":
    web.run_app(app, port=5001)
