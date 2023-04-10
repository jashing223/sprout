import requests
from bs4 import BeautifulSoup
import os

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
                return "file"
            else:
                return "UncorrectFileFormat"
        else:
            return "NoFileError"

    elif url is not None:
        if (url.lower().endswith(('.bmp', '.png', '.jpg', '.jpeg', 'gif', "webp"))):
            return "url"
        else:
            return "UncorrectUrlFormat"
    
    else:
        return "UnKnownError"

def get_result(url = None, file = None, debug = False):

    data_type = is_valid(file, url)
# 判斷data_type=================================================================================

    if data_type == "file":

        r = requests.post("https://saucenao.com/search.php", files = {'file':open(file,"rb")})

    elif data_type == "url":

        data = {
            "file": "",
            "url": url
        }

        r = requests.post("https://saucenao.com/search.php", data = data)

    else:
        return data_type
# 判斷data_type==================================================================================

    soup = BeautifulSoup(r.text,"html.parser")

    # main part
    result = []
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

        result.append(Result(title,author,similarity,link,thumbnail,deep_search))

    if debug is True:
        print("file: " + str(file) + "\n","url: " + str(url) + "\n")
        for line in result:
            print("title: " + line.title + "\n",
            "author: " + line.author + "\n",
            "link:" + line.link + "\n",
            "similarity: " + line.similarity + "\n",
            "thumbnail: " + line.thumbnail + "\n",
            "deep_search: " + line.deep_search + "\n")

    elif debug is False:
        pass

    else:
        pass
    # 按照相似度由高到低排列
    #result.sort()
    if len(result) == 0:
        return "UncorrectUrlFormat"
    return result

if __name__ == "__main__":
    get_result()