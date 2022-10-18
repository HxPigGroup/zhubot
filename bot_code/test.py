from mirai import Mirai, WebSocketAdapter, FriendMessage
from mirai import GroupMessage, At, Plain
import re
# login 3510871411 zcyyyhtql123
import httpx
import asyncio
import datetime
from mirai import Startup, Shutdown
from text_generate_easy import Dialog
_task = None

D = Dialog()
D.load(r'./save/dict')

bot = Mirai(
        qq=3510871411,
        adapter=WebSocketAdapter(
            verify_key='yirimirai', host='localhost', port=8080
        )
    )

@bot.on(FriendMessage)
def on_friend_message(event: FriendMessage):
    if str(event.message_chain) == '你好':
        return bot.send(event, 'Hello, World!')

@bot.on(GroupMessage)
def on_group_message(event: GroupMessage):
    if At(bot.qq) in event.message_chain:
        return bot.send(event, [At(event.sender.id), '你觉得hx是呆逼吗？请以猪话开头说话，传说hx会告诉你。'])

@bot.on(GroupMessage)
async def on_group_message(event: GroupMessage):
    msg = "".join(map(str, event.message_chain[Plain]))
    
    #m = re.match(r'^猪话\s*(\w+)\s*$', msg.strip())
    msg = msg.strip()
    if len(msg)>=2 and msg[0] == "猪" and msg[1] == "话":
    #if m:
        #sentence = m.group(1)
        sentence = msg[2:]
        sentence = sentence.strip()
        if sentence == "猪话":
            output = "这个群我说话都没人理我，还想着要猪说话，滚！"
        else:
            output = D.cheng(sentence)
        if output != "":
            await bot.send(event, output)
    else:
        if len(msg)>=2 and msg[-1] in ['吗', '呢', '啊', '呀', '草', '艹', '哈', '逼']:
            output = "xs"
            await bot.send(event, output)
    D.add_new_line(msg)
@bot.on(Startup)
async def save_data(_):
    async def save():
        save_finished = False
        while True:
            await asyncio.sleep(1)
            now = datetime.datetime.now()
            if now.minute % 30 == 0:
                D.save_data()
                save_finished = True
            if now.minute % 30 == 1:
                save_finished = False
    global _save_task
    _save_task = asyncio.create_task(save())
    
@bot.on(Startup)
async def start_scheduler(_):
    async def timer():
        zhongwu_finished = False
        wanshang_finished = False
        while True:
            await asyncio.sleep(1)
            now = datetime.datetime.now()
            if now.hour == 17 and now.minute == 41 and not wanshang_finished:
                await bot.send_group_message(799198588, "cs")
                wanshang_finished = True
            if now.hour == 17 and now.minute == 42:
                wanshang_finished = False
            if now.hour == 12 and now.minute == 0 and not zhongwu_finished:
                await bot.send_group_message(799198588, "cs")
                zhongwu_finished = True
            if now.hour == 12 and now.minute == 1:
                zhongwu_finished = False

    global _task
    _task = asyncio.create_task(timer())

@bot.on(Shutdown)
async def stop_scheduler(_):
    # 退出时停止定时任务
    if _task and not task.done():
        _task.cancel()
    if _save_task and not _save_task.done():
        _save_task.cancel()

if __name__ == '__main__':
    
    bot.run()