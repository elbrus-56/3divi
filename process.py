import asyncio
from time import sleep
from aiohttp import web
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Thread")


async def handle(request):
    data = await request.json()
    await asyncio.sleep(data["request"]["delay"])
    return web.Response(body=str("DONE"))


app = web.Application()
app.add_routes([web.post("/sleeper", handle)])

if __name__ == "__main__":
    web.run_app(app, port=5002)
