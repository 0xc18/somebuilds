import asyncio
import io
import tarfile

import httpx

from config import packages

API_URL = "https://pypi.org/pypi/{}/json"


async def download(pkg: str):
    async with asyncio.Semaphore(4), httpx.AsyncClient(verify=False) as client:
        res = await client.get(
            url=API_URL.format(pkg),
        )
        data = res.json()
        for i in data["releases"][data["info"]["version"]]:
            if i.get("packagetype") == "sdist":
                print(f"Downloaing package {i.get('filename')}")
                sdist_data = await client.get(i.get("url"))
                sdist = io.BytesIO(sdist_data.content)
                tf = tarfile.open(fileobj=sdist, mode="r:gz")
                tf.extractall("./output")


async def main():
    await asyncio.gather(*[download(i) for i in packages])


if __name__ == "__main__":
    asyncio.run(main())
