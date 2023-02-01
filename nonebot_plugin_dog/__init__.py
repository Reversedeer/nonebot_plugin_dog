import httpx
import asyncio
import nonebot
from re import I
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot import logger, on_command, on_regex
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN
from nonebot.adapters.onebot.v11 import MessageSegment,GroupMessageEvent

from .utils import *

openstats = on_regex(r"^(开启文案|关闭文案)", permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
                     flags=I, priority=10, block=True)

dog_matcher = on_command("舔狗日记", aliases={"舔狗嘤嘤嘤"},
                         priority=10, block=True)

try:
    cd_time = nonebot.get_driver().config.dog_cd_time       # 从配置文件中读取cd_time
except:
    cd_time = 20       		# 默认值
    
dog_cd_dir = {}  # 记录cd的字典

@dog_matcher.handle()
async def dog(event: GroupMessageEvent, matcher: Matcher):     # 定义异步函数 dog
    if not (await check_group_allow(str(event.group_id))):
        await dog_matcher.finish(notAllow, at_sender=True)
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
        await matcher.finish(MessageSegment.text(response_text.strip()), block=True)
    else:

        await dog_matcher.finish(
            MessageSegment.text(f"不要深情了喵，休息, {cd_time - cd:.0f}秒后才能再次使用"),
            at_sender=True, block=True)

@openstats.handle()
async def _(event: GroupMessageEvent, state: T_State):
    gid = str(event.group_id)  # 群号
    # 获取用户输入的参数
    args = list(state["_matched_groups"])
    command = args[0]
    if "开启文案" in command:
        if gid in groupdata:
            groupdata[gid]["allow"] = True
            write_group_data()
            await openstats.finish("功能已开启喵~")
        else:
            groupdata.update({gid: {"allow": True}})
            write_group_data()
            await openstats.finish("功能已开启喵~")
    elif "关闭文案" in command:
        if gid in groupdata:
            groupdata[gid]["allow"] = False
            write_group_data()
            await openstats.finish("功能已禁用喵~")
        else:
            groupdata.update({gid: {"allow": False}})
            write_group_data()
            await openstats.finish("功能已禁用喵~")