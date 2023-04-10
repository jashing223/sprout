import asyncio
import discord
from discord.ext import commands, tasks
#from saucenao_api import SauceNao
import fast_saucenao
import pickle
import threading

pending_message = []

#儲存變數函式：
def dump_file(v,filename):
    try:    
        f=open(filename,'wb')
        pickle.dump(v,f)
        f.close()
        return filename
    except:
        return None

# 讀取變數函式：
def load_file(filename):
    try:
        f=open(filename,'rb')
        r=pickle.load(f)
        f.close()
        return r
    except:
        return None

def image_result(bot, msg_channel, urls):
    def execute():
        result = fast_saucenao.get_result(urls)
        for results in result:
            # 如果訊息中有多張圖的附件則可以多次搜尋
                    #try:
                        # 過去式--使用api key 配合 saucenao-api 來進行圖搜，取得作者和來源網址還有圖片相似度
                        # 過去式--results = SauceNao("60a603766c8a8724e3bffabe1a29812c5404bf53").from_url(line)
                #image_result(self.bot, ctx, url)
                # 相似度
            embed = discord.Embed(title = results[0].title,description = "Similarity: "+str(results[0].similarity),color=discord.colour.Color.green())
                # 圖片作者
            embed.add_field(name = "Author",value = results[0].author,inline = False)
                    # 預覽搜尋到的結果
            embed.set_thumbnail(url = results[0].thumbnail)
                # 圖搜結果的連結
            embed.add_field(name="Sauce", value = results[0].link, inline = False)
                # 今天起不再受到api的拘束
            embed.set_footer(icon_url = bot.user.avatar_url,text = "支持SauceNao從team Bot開始")
                # 過去式--因為是 api 的關係所以使用次數限制
                # 過去式-- embed.set_footer(icon_url = self.bot.user.avatar_url,text = f"今日剩餘次數: {results.long_remaining}")
            pending_message.append((msg_channel, embed))

    t = threading.Thread(target = execute)
    t.start()

class Cache:
    def __init__(self):
        self.cache_update_loop.start()

    @tasks.loop(seconds=1.0)
    async def cache_update_loop(self):
        while pending_message != []:
            msg_channel, embed = pending_message[0][0], pending_message[0][1]
            await msg_channel.send(embed=embed)
            del pending_message[:1]
            await asyncio.sleep(0.25)

    @cache_update_loop.before_loop
    async def before_cache_update_loop(self):
        print('send_msg func start (from image extension)')

async def main():
    cache = Cache()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

msg_datafile = "../storage/message.pickle"

class Image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        global data
        data = load_file(msg_datafile)
        if not isinstance(data, dict):
            data = {}

    # 搜尋圖片來源
    # 使用者輸入 $sauce 時會觸發
    # 利用回復圖片或網址的方式搜尋
    @commands.command(help = """
    搜尋圖片來源
    利用回復圖片或網址的方式搜尋
    使用者輸入 $sauce 時會觸發
    """, brief = "Get the sauce of image.")
    async def sauce(self,ctx):
        #排除錯誤的使用方法
        if ctx.message.reference == None:
            await ctx.send("Uncorrect usage!!!")
        else:
            channel = self.bot.get_channel(ctx.message.channel.id)
            message = await channel.fetch_message(ctx.message.reference.message_id)
            # 從回覆的訊息中找尋需要圖搜的圖
            if message.attachments == [] and message.content == "":
                await ctx.send("There's no attachments!!!")
            else:
                url = []
                if message.attachments != []:
                    for line in message.attachments:
                        url.append(str(line.url))
                elif message.content != "":
                    if (".jpg" or ".jpeg" or ".png" or".gif" or ".bmp") and "http" in message.content:
                        url.append(str(message.content))
                    else:
                        await ctx.send("No filelink defind")
                        return
                
                image_result(self.bot, ctx, url)

                

    # 擷取對話內容看是否包含圖片
    @commands.Cog.listener()
    async def on_message(self, message):
        # 排除機器人
        if message.author.bot == True:
            return

        if message.author.id not in data:
            data[message.author.id] = 0
        
        # 判斷是否有圖片
        if (".jpg" or ".jpeg" or ".png" or ".bmp") and "http" in message.content:
            data[message.author.id] += 1
            urls = [str(message.content)]
        if message.attachments != []:
            urls = []
            for line in message.attachments:
                urls.append(str(line.url))
                data[message.author.id] += 1
            if urls != []:
                image_result(self.bot, message.channel, urls)

        # 把紀錄結果儲存進message.pickle裡
        dump_file(data, msg_datafile)
    
    @commands.command(help="獲得圖片貢獻度排名", brief="獲得圖片貢獻度排名")
    async def img_rank(self, ctx):
        string = ""
        rank = sorted(data.items(), key=lambda x: x[1], reverse=True)
        for i in rank:
            # 可能會有其他伺服器的成員，所以找不到資料報錯
            try:
                # 取得成員的暱稱
                member = await self.bot.get_guild(ctx.guild.id).fetch_member(i[0])
                # 可能會有沒有暱稱的成員
                if member.nick is None:
                    name = member.name
                else:
                    name = member.nick
                # 由高到低展現圖片貢獻度
                string += str(name).split("#")[0] + " " + str(i[1]) + "\n"

            except:
                pass
        await ctx.send(string)

# 從主程式加入此功能需要用到的函數
def setup(bot):
    bot.add_cog(Image(bot))
