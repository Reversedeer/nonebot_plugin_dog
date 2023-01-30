from nonebot.adapters.onebot.v11 import Message, MessageSegment,MessageEvent
from nonebot import logger, on_command
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
import httpx
import asyncio
import nonebot

try:
    cd_time = nonebot.get_driver().config.dog_cd_time       # 从配置文件中读取cd_time
except:
    cd_time = 10       # 默认值
    
dog_cd_dir = {}  # 记录cd的字典

dog_matcher = on_command(
    "舔狗日记", aliases={"舔狗嘤嘤嘤"}, priority=5)

@dog_matcher.handle()
async def dog(event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):     # 定义异步函数 dog
    qid = event.get_user_id()                                                           # 获取用户id
    try:
        cd = event.time - dog_cd_dir[qid]                                               # 计算cd
    except KeyError:
        cd = cd_time + 1                                                                # 没有记录则cd为cd_time+1
    if (
        cd > cd_time    
        or event.get_user_id() in nonebot.get_driver().config.superusers
    ):                                                                                  # 记录cd    
        dog_cd_dir.update({qid: event.time})
        try:
            async with httpx.AsyncClient() as client:                                   # 使用 httpx.AsyncClient 获取 API，存储为 response 变量
                response = await client.get("https://api.juncikeji.xyz/api/tgrj.php")
                response_text = response.text
        except Exception as error:
            await dog_matcher.finish(MessageSegment.text(str(error)))
        await matcher.finish(MessageSegment.text(response_text))
    else:
        # handle valid response

        await dog_matcher.finish(
            MessageSegment.text(f"不要深情了喵，休息, {cd_time - cd:.0f}秒后才能再次使用"),
            at_sender=True
            )