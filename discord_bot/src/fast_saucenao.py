import aiohttp
import asyncio
from bs4 import BeautifulSoup
import os
import proxy_alive
import time

class Result:

    def __init__(self,title,author,similarity,link,thumbnail,deep_search):
        self.title = title
        self.author = author
        self.link = link
        self.similarity = similarity
        self.thumbnail = thumbnail
        self.deep_search = deep_search

    def __lt__(self, other):
        return float(other.similarity.replace("%","")) < float(self.similarity.replace("%",""))

def is_valid(file = None, url = None):

    if file is None and url is None:
        return "NoDateGivenError"
    
    elif file is not None and url is not None:
        return "MuiltipleArgumentError"

    elif file is not None:
        if os.path.exists(file):
            if (file.lower().endswith(('.bmp', '.png', '.jpg', '.jpeg','gif'))):
                file = {'file':open(file,"rb")}
                return file
            else:
                return "UncorrectFileFormat"
        else:
            return "NoFileError"

    elif url is not None:
        if (url.lower().endswith(('.bmp', '.png', '.jpg', '.jpeg', 'gif', "webp"))):
            data = {
                    "file": "",
                    "url": url
                    }
            return data
        else:
            return "UncorrectUrlFormat"
    
    else:
        return "UnKnownError"

def filter(response):
    soup = BeautifulSoup(response,"html.parser")

    # main part
    results = []
    try:
        
        for table in soup.find_all("tr"):

            #get all information from saucenao

            # matchinfo
            matchinfo = table.find("td", class_ = "resulttablecontent").find("div", class_ = "resultmatchinfo")
            # similarity
            similarity = matchinfo.find("div", class_ = "resultsimilarityinfo").text
            # other link
            if matchinfo.find("div",class_ = "resultmiscinfo").find_all("a") != []:
                for links in matchinfo.find("div",class_ = "resultmiscinfo").find_all("a"):
                    link = links['href']
            else:
                link = None
            # content part
            content = table.find("td", class_ = "resulttablecontent").find("div", class_ = "resultcontent")

            # title
            try:
                title = content.find("div", class_ = "resulttitle").text
            except:
                title = "No title"
            # author
            try:
                author = content.find("div", class_ = "resultcontentcolumn").find_all("strong")[-1].next_sibling
                try:
                    author = author.text
                except:
                    pass
            except:
                author = []
            # link
            if link is None:
                try:
                    link = content.find("div", class_ = "resultcontentcolumn").find("a")['href']
                except:
                    link = content.find("div", class_ = "resultcontentcolumn").text
            # thumbnail and deep_search
            pic_part = table.find("td", class_ = "resulttableimage").find("div", class_ = "resultimage").find("a")
            deep_search = pic_part['href']
            thumbnail = pic_part.find("img")['src']
            if (".jpg" or ".jpeg" or ".png" or ".bmp") not in thumbnail.lower():
                thumbnail = "https://static.thenounproject.com/png/116547-200.png"

            results.append(Result(title,author,similarity,link,thumbnail,deep_search))

        return results
    except:
        return []
    

async def get_session():
    session = aiohttp.ClientSession(trust_env=True)
    return session

async def get_page(data, proxy = None):
    #timeout =aiohttp.ClientTimeout(total=2)
    #timeout=timeout
    count = 0
    try:
        async with await get_session() as session:
            async with session.post("http://saucenao.com/search.php", data=data, proxy="http://"+proxy) as response:
                response = await response.text()
                result = filter(response)
                if result != []:
                    print(proxy)
                    print(data['url'])
                    return [data['url'],result]
                        
                else:
                    await asyncio.sleep(7)
    except Exception as e: #很重要
        await asyncio.sleep(7)

async def get_all(data, proxys):
    tasks = []
    for proxy in proxys:
        task = asyncio.create_task(get_page(data, proxy))
        tasks.append(task)
    
    #result = await asyncio.gather(*tasks)
    result, unfinished = await asyncio.wait(tasks,return_when=asyncio.FIRST_COMPLETED)
    return result

async def final(urls, proxys):

    tasks = []
    for url in urls:
        print(url.strip())
        data = is_valid(url = url.strip())
        task = asyncio.create_task(get_all(data, proxys))
        tasks.append(task)

    result = await asyncio.gather(*tasks)

    return result

async def merge(urls):
    first = time.perf_counter()
    #with open("url.txt","r") as fr:
    #    urls = map(lambda x:x.strip("\n"),fr.readlines())
    results = {}
    end = []
    proxies = await proxy_alive.proxys()
    print(len(proxies))
    tasks = await final(urls, proxies)
    for task in tasks:
        task = list(task)[0].result()
        if task is None:
            print("NoResult")
            return "NoResult"
        results[task[0]] = task[1]
    for url in urls:
        end.append(results[url])
    print(f"end: {time.perf_counter()-first}")
    return end

def get_result(urls):
    #asyncio.set_event_loop(asyncio.SelectorEventLoop())
    #print(asyncio.get_event_loop())
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    result = None
    while result is None:
        try:
            result = asyncio.run(merge(urls))
            if result == "NoResult":
                raise Exception("agn")
            return result
        except:
            pass
        

if __name__ == "__main__":
    get_result(["https://cdn.discordapp.com/attachments/830639515647082549/865262289962795008/8f1c82448ddc0dad4665d61b5eb59c40.JPG"])