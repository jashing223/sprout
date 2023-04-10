# 檔名：picture.py
# 功能：上傳、發送照片（簡單示範和照片有關的用法）

import asyncio
from discord.ext.commands.cog import Cog
from discord.ext import commands
import random

class Guess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="guess number game", brief = "guess number game")
    async def guess(self, ctx):
        await ctx.send("Guess a 4-digit number that doesn't contain 0.")
        #產生隨機數字答案
        ans = ''.join(random.sample("123456789",4))
        print("anwser:", ans)

        def is_valid(m):
            return m.author == ctx.author
    
        for i in range(30):
            #超過時間就game over
            try:
                guess = await self.bot.wait_for("message",check = is_valid, timeout = 300.0)
            except asyncio.TimeoutError:
                await ctx.send("Game Over")
                return

            guess = guess.content.strip()

            #設定結束遊戲的條件
            if guess == "quit":
                await ctx.send("Game End")
                return
            elif guess.isdigit() != True or len(guess) != 4 or "0" in guess:
                await ctx.send("Invaild guess")
            elif guess == ans:
                await ctx.send("Correct")
                return
            #遊戲進行時的判斷
            else:
                a_count = 0
                for i in range(len(guess)):
                    if i < len(ans) and guess[i] == ans[i]:
                        a_count += 1

                b_count = 0
                for i in range(len(ans)):
                    if guess[i] in ans:
                        b_count += 1
                b_count -= a_count

                await ctx.send(f"{a_count}A{b_count}B")

        await ctx.send("You Lose")

# 從主程式加入此功能需要用到的函數
def setup(bot):
    bot.add_cog(Guess(bot))
