import requests
from bs4 import BeautifulSoup
import random
import discord
from discord.ext import commands

# 建立下載的函數
def get_img(num):
    try:
        res = requests.get(f"https://xkcd.com/{num}")
        soup = BeautifulSoup(res.text,"html.parser")
        result = soup.find("div",id="comic").find("img")['src']
        res = requests.get("https:"+result)
        with open(f"../storage/pic/{num}.png","wb") as f:
            f.write(res.content)
    
    except:
        print(f"comic code: {num} have some problem")

class dis_xkcd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # 取得最新的xkcd漫畫到第幾篇
        r = requests.get("http://xkcd.com")
        soup = BeautifulSoup(r.text,"html.parser")
        global latest
        latest = soup.find("div",id="middleContainer").find("br").next_sibling.split("/")[-2]

    # 下載指定的xkcd漫畫
    @commands.command(help = "取得特定編號的漫畫", brief = "取得特定編號的漫畫")
    async def xkcd_get(self, ctx, value = None):

        if value is None:
            await ctx.send("沒給編號")
            return

        if value <= latest:
            get_img(value)
            f = f"../storage/pic/{value}.png"
            picture = discord.File(f)
            await ctx.send(file = picture)
        else:
            await ctx.send(f"要求的編號需介於1~{latest}之間")

    # 隨機抽取一則xkcd漫畫
    @commands.command(help = "隨機抽一則漫畫", brief = "隨機抽一則漫畫")
    async def xkcd_r(self, ctx):

        try:
            n = random.randint(1,int(latest))
            get_img(n)
            f = f"../storage/pic/{n}.png"
            picture = discord.File(f)
            await ctx.send(file = picture)
        except Exception as e:
            await ctx.send(e)
    
    # 取得最新的xkcd漫畫到第幾篇
    @commands.command(help = "取得最新的xkcd漫畫到第幾篇", brief = "取得最新的xkcd漫畫到第幾篇")
    async def xkcd_latest(self, ctx):
        ctx.send(f"latest comic code is: {latest}")

def setup(bot):
    bot.add_cog(dis_xkcd(bot))