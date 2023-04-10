import requests
from bs4 import BeautifulSoup
import os
import sys
import random
from PIL import Image

op = sys.argv[1]

if os.path.isdir("pic_save") != True:
    os.makedirs("pic_save")
    os.chdir("./pic_save")
else:
    os.chdir("./pic_save")

def command(op):

    r = requests.get("http://xkcd.com")
    soup = BeautifulSoup(r.text,"html.parser")
    lastest = soup.find("div",id="middleContainer").find("br").next_sibling.split("/")[-2]

    def get_img(num):

        try:
            res = requests.get(f"https://xkcd.com/{num}")
            soup = BeautifulSoup(res.text,"html.parser")
            result = soup.find("div",id="comic").find("img")['src']

            res = requests.get("https:"+result)
            with open(f"{num}.png","wb") as f:
                f.write(res.content)
        
        except:
            print(f"comic code: {num} have some problem")

    if op == "help":

        print(f"""
        command:

            bulk                  一次下載任意 50 張 xkcd 的漫畫

            download  [num]                 下載特定編號的漫畫  (有圖片檢視功能)
                      [r|random]            隨機下載1則 (有圖片檢視功能)
                      [num1,num2,num3....]  以,分隔的多個數字，代表下載多則 Example: download 145,154,1547
                      [num-num]             輸入一個 數字-數字 的範圍，代表下載多則 Example: download 158-1258
                      [comic name]          輸入一個漫畫的名稱，並下載一則  (有圖片檢視功能)

                      ★ 重要 : [num]為漫畫編號並且需介於1~{lastest}之間

        """,end="")

    elif op == "bulk":

        number = random.sample(range(1, int(lastest)), 50)

        for n in number:
            get_img(n)

    elif op == "download":

        try:
            value = sys.argv[2]

            if value.isdigit() == True:
                if value <= lastest:
                    print(f"downloading comic code: {value}")
                    get_img(value)
                    img = Image.open(f"{value}.png")
                    img.show()
                else:
                    print(f"要求的編號需介於1~{lastest}之間")
            
            elif value == "r" or value == "random":
                print("downloading ramdom comic")
                n = random.randint(1,int(lastest))
                get_img(n)
                img = Image.open(f"{n}.png")
                img.show()

            elif "," in value:
                #try:
                    print(f"downloading comic code: {value}")
                    value = value.split(",")
                    for n in value:
                        get_img(n)
                #except:
                    #return command("help")

            elif "-" in value:
                #try:
                    print(f"downloading comic: {value}")
                    for n in range(int(value.split("-")[0]),int(value.split("-")[1])+1):
                        get_img(n)
            
            else:
                res = requests.get(f"https://imgs.xkcd.com/comics/{value}.png")
                if res.status_code != 200:
                    print("This name is not available")
                else:
                    with open(f"{value}.png","wb") as f:
                        f.write(res.content)
                    img = Image.open(f"{value}.png")
                    img.show()
                #10_day_forecast.png
                #except:
                    #return command("help")
        except:
            return command("help")
    else:
        command("help")

command(op)