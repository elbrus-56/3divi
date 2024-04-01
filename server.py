import datetime
import json
from aiohttp import web
import logging

import aiohttp


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Thread")


async def async_make_request(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=json.dumps(data)) as resp:
            return await resp.text()


async def handle(request):
    _ts = datetime.datetime.now()
    data = await request.json()
    recieve_msg = {
        "id": data["request"]["id"],
        "time_from": str(_ts),
    }
    await async_make_request("http://127.0.0.1:5003/save_2", recieve_msg)
    await async_make_request("http://127.0.0.1:5002/sleeper", data)
    _te = datetime.datetime.now()
    print(f"end, {data} => {_te}")
    result_msg = {
        "id": data["request"]["id"],
        "time_from": str(_ts),
        "time_to": str(_te),
    }
    await async_make_request("http://127.0.0.1:5003/save_1", result_msg)
    return web.Response(body=json.dumps({"asyncAnswer": "Ok"}))


app = web.Application()
app.add_routes([web.post("/handler", handle)])

if __name__ == "__main__":
    web.run_app(app, port=5001)
