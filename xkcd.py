import requests
from bs4 import BeautifulSoup
import os

if os.path.isdir("Download") == True:
    pass
else:
    os.makedirs("Download")
os.chdir(r"./Download")
print(os.getcwd())

r = requests.get("https://xkcd.com")
soup = BeautifulSoup(r.text,"html.parser")

