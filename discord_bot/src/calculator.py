from discord.ext import commands
import math

class Calculator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help = """
        C n 取 k 的計算，表示為: ~c n,k
        舉例來說
        $c 5,3
        """,
        brief = "C n 取 k 的計算")
    async def c(self,ctx,arg=None):
        arg = arg.lower()
        if arg is None:
            await ctx.send("沒有輸入要計算的值")
            return
        try:
            k,n = int(arg.split(",")[0]),int(arg.split(",")[1])
            ans = math.factorial(k)/(math.factorial(n)*math.factorial(k-n))
            await ctx.send(f"C({k},{n}) = {ans}")
        except:
            await ctx.send("無效的計算")

    @commands.command(
        help = """
        P n 取 k 的計算，表示為: ~p n,k
        舉例來說
        $p 5,3
        """,
        brief = "P n 取 k 的計算")
    async def p(self,ctx,arg=None):
        arg = arg.lower()
        if arg is None:
            await ctx.send("沒有輸入要計算的值")
            return
        try:
            k,n = int(arg.split(",")[0]),int(arg.split(",")[1])
            ans = math.factorial(k)/math.factorial(k-n)
            await ctx.send(f"P({k},{n}) = {ans}")
        except:
            await ctx.send("無效的計算")
            
    @commands.command(
        help = """
        接乘的計算，表示為: ~fac n
        舉例來說
        $fac 5
        """,
        brief = "接乘的計算")
    async def fac(self,ctx,arg=None):
        arg = int(arg)
        if arg is None:
            await ctx.send("沒有輸入要計算的值")
            return
        try:
            ans = math.factorial(arg)
            await ctx.send(f"{arg}! = {ans}")
        except:
            await ctx.send("無效的計算")

def setup(bot):
    bot.add_cog(Calculator(bot))