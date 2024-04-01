from aiohttp import web
import aiofiles


async def write_to_file_1(request):
    data = await request.json()
    async with aiofiles.open("1.txt", mode="a") as fp:
        await fp.write(
            " | "
            + data["id"]
            + " | "
            + data["time_from"]
            + " | "
            + data["time_to"]
            + " |\n"
        )
    return web.Response(body=str("DONE"))


async def write_to_file_2(request):
    data = await request.json()
    async with aiofiles.open("2.txt", mode="a") as fp:
        await fp.write(" | " + data["id"] + " | " + data["time_from"] + " |\n")
    return web.Response(body=str("DONE"))


app = web.Application()
app.add_routes(
    [
        web.post("/save_1", write_to_file_1),
        web.post("/save_2", write_to_file_2),
    ]
)

if __name__ == "__main__":
    web.run_app(app, port=5003)
