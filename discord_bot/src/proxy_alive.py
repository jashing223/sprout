import aiohttp
import asyncio
import requests

def get_proxy():
    r = requests.get("https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=750&country=all&ssl=all&anonymity=all&simplified=true")
    ips = "".join(r.text.split("\r")).split("\n")
    return ips


async def get_page(url, proxy = None):
    timeout = aiohttp.ClientTimeout(total=1)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url,proxy="http://"+proxy) as response:
                await response.text()
                return proxy
    except:
        pass

async def get_all(url, proxys):
    tasks = []
    for proxy in proxys:
        task = asyncio.create_task(get_page(url, proxy))
        tasks.append(task)
    
    result = await asyncio.gather(*tasks)
    return result

#http://httpbin.org/ip
async def proxy_alive():
    proxys = get_proxy()
    data = await get_all("http://httpbin.org/ip",proxys)
    return data

async def proxys():

    proxys = []
    results = await proxy_alive()
    for result in results:
        if result is not None:
            proxys.append(result)

    return proxys

if __name__ == "__main__":
    ans = asyncio.run(proxys())
    print(ans)