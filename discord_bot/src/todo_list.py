# 檔名：todo_list.py
# 功能：TODO list (新增、刪除、顯示)
# TODO：刪除、顯示、排序、清空、儲存記錄至檔案 (HINT: file I/O, pickle)

import discord
from discord.ext import commands
import re
import pickle

#儲存 todo_list data 的地方
filename = "../storage/todo_record.pickle"

#儲存變數函式：
def save_variable(v,filename):
    f=open(filename,'wb')
    pickle.dump(v,f)
    f.close()
    return filename 

# 讀取變數函式：
def load_variavle(filename):
    f=open(filename,'rb')
    r=pickle.load(f)
    f.close()
    return r

# 一項 Todo 的 class
class Todo:
    # 初始化
    def __init__(self, date, label, item):
        # 判斷是否為合法的日期 (不是很完整的判斷)
        d = re.compile("[0-9]{1,2}/[0-9]{1,2}")
        assert d.match(date)
        self.date = date
        self.label = label
        self.item = item

    # 小於 < (定義兩個 Todo 之間的「小於」，sort 時會用到)
    def __lt__(self, other):
        pass
        #################################################################
        # TODO: 實作小於判斷 (__lt__)
        # 分類: 作業 (5 pts)
        # HINT: 參考下方 __eq__
        #################################################################
        s_mon,s_day = map(int,self.date.split("/"))
        o_mon,o_day = map(int,other.date.split("/"))
        return o_mon > s_mon or (o_mon == s_mon and o_day > s_day)

    # 等於 = (判斷兩個 Todo 是否相等)
    def __eq__(self, other):
        return self.date==other.date and self.label==other.label and self.item==other.item

    # 回傳一個代表這個 Todo 的 string
    def __repr__(self):
        return f"{self.date} {self.label} {self.item}"

# Todo list 相關 commands
class Todo_list(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # 儲存 TODO list
        # 讀入todo_record.pickle內儲存的資料
        try:
            self.todo_list = load_variavle(filename)
        except:
            self.todo_list = []

    # $add date label item
    @commands.command(
        help = '''
        Add TODO.
        For example:
        $add 06/24 Sprout Discord Bot HW
        ''', # 輸入 $help add 時顯示
        brief = "Add TODO." # 輸入 $help 時顯示
    )
    async def add(self, ctx, date, label, *, item):
        try:
            # 依照輸入建立一個 Todo object
            t = Todo(date, label, item)
        except Exception as e:
            # 建立失敗
            print(e)
            await ctx.send("Invalid input ><")
            return
        # 把 Todo 加進 list
        self.todo_list.append(t)
        # 按照日期排序，若實作了 Todo 的 __lt__ 則可以直接用 sort() 排序
        self.todo_list.sort()
        # 儲存新增的內容
        save_variable(self.todo_list,filename)
        # 印出加入成功的訊息
        await ctx.send('"{}" added to TODO list'.format(item))

    # $done date label item
    @commands.command(
        help = '''
        Done TODO.
        For example:
        $done 6/24 Sprout Discord Bot HW
        ''', # 輸入 $help add 時顯示
        brief = "Done TODO." # 輸入 $help 時顯示
    )

    async def done(self, ctx, date, label, *, item): # * 代表 label 後面所有的字都會放到 item 內
        #################################################################
        # TODO: 實作刪除一項 Todo
        # 分類: 作業 (5 pts)
        # HINT: 參考上方 add，可以直接用 in 判斷一個 Todo 是否在 todo_list 中 (因為有實作 __eq__)
        #################################################################
        try:
            if Todo(date,label,item) in self.todo_list:
                await ctx.send(f"☑ ~~{Todo(date,label,item)}~~")
                self.todo_list.remove(Todo(date,label,item))
                # 儲存變更的內容
                save_variable(self.todo_list,filename)
            else:
                await ctx.send("沒有找到這個任務")
        except Exception as e:
            await ctx.send(e)

    # $show [label]
    @commands.command(
        help = '''
        Show all TODO with the label if specified sorted by date.
        For example:
        $show Sprout
        $show
        ''',
        brief = "Show all TODO with the label if specified sorted by date." # 輸入 $help 時顯示
    )
    async def show(self, ctx, label=None):
        #################################################################
        # TODO: 實作顯示 Todo，若有輸入 label 則顯示符合該 label 的 Todo，顯示時依日期排序
        # 分類: 作業 (5 pts)
        # HINT: 遍歷 todo_list
        #################################################################
        try:
            #沒指定印出所有任務
            if label is None:
                content = ""
                for task in self.todo_list:
                    content += str(task) + "\n"

            #指定label就印出符合label的項目
            else:
                content = ""
                for task in self.todo_list:
                    if label in task.label:
                        content += str(task) + "\n"

            #送出查詢結果
            if content == "":
                await ctx.send("No result")
            else:
                await ctx.send(content)

        except Exception as e:
            await ctx.send(e)

    # $clear
    @commands.command(help = "Clear TODO list.", brief = "Clear TODO list.")
    async def clear(self, ctx):
        #################################################################
        # TODO: 實作清空 TODO list
        # 分類: 作業 (5 pts)
        #################################################################
        self.todo_list = []
        # 儲存變更的內容
        save_variable(self.todo_list,filename)
        await ctx.send("已清空todo_list")

def setup(bot):
    bot.add_cog(Todo_list(bot))
