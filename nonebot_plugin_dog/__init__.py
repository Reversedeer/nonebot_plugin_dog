import httpx
import asyncio
import nonebot
import re
from re import I
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN
from nonebot.adapters.onebot.v11 import MessageSegment,GroupMessageEvent

from .utils import *

openstats = on_regex(r"^(开启文案|关闭文案)", permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
                     flags=I, priority=10, block=True)

dog_matcher = on_command("舔狗日记", aliases={"舔狗嘤嘤嘤"},
                        priority=10, block=True)

laugh_matcher = on_command("讲个笑话", aliases={"说个笑话"},
                        priority=10, block=True)

hitokoto_matcher = on_command("一言", aliases={"一句一言"},
                        priority=10, block=True)



try:
    cd_time = nonebot.get_driver().config.cd_time       # 从配置文件中读取cd_time
except:
    cd_time = 20      		# cd默认值
    
dog_CD_dir = {}  # 记录舔狗日记cd的字典
laugh_CD_dir = {}  #记录讲个笑话cd的字典
hitokoto_CD_dir = {}   #记录一言cd的字典

@dog_matcher.handle()
async def dog(event: GroupMessageEvent, matcher: Matcher):     # 定义异步函数 dog
    if not (await check_group_allow(str(event.group_id))):
        await dog_matcher.finish(notAllow, at_sender=True)
    uid = event.get_user_id()                                         # 获取用户id
    try:
        cd = event.time - dog_CD_dir[uid]                             # 计算cd
    except KeyError:
        cd = cd_time + 1                                        # 没有记录则cd为cd_time+1
    if (
        cd > cd_time    
        or event.get_user_id() in nonebot.get_driver().config.superusers
    ):                                                                     # 记录cd    
        dog_CD_dir.update({uid: event.time})
        try:
            async with httpx.AsyncClient() as client:                      # 使用 httpx.AsyncClient 获取 API，存储为 response 变量
                response = await client.get("https://api.juncikeji.xyz/api/tgrj.php")
                response_text = response.text
        except Exception as error:
            await dog_matcher.finish(MessageSegment.text(str(error)))
        await matcher.finish(MessageSegment.text(response_text.strip()), block=True)
    else:
        await dog_matcher.finish(
            MessageSegment.text(f"不要深情了喵，休息{cd_time - cd:.0f}秒后再找我喵~"),
            at_sender=True, block=True)

@laugh_matcher.handle()
async def laugh(event: GroupMessageEvent, matcher: Matcher):     # 定义异步函数 laugh
    if not (await check_group_allow(str(event.group_id))):
        await dog_matcher.finish(notAllow, at_sender=True)
    uid = event.get_user_id()                                           # 获取用户id
    try:
        cd = event.time - laugh_CD_dir[uid]                             # 计算cd
    except KeyError:
        cd = cd_time + 1                                          # 没有记录则cd为cd_time+1
    if (
        cd > cd_time    
        or event.get_user_id() in nonebot.get_driver().config.superusers
    ):                                                                       # 记录cd    
        laugh_CD_dir.update({uid: event.time})
        try:
            async with httpx.AsyncClient() as client:                        # 使用 httpx.AsyncClient 获取 API，存储为 response 变量
                response = await client.get("https://api.juncikeji.xyz/api/qwxh.php")
                response_text = response.text
        except Exception as error:
            await laugh_matcher.finish(MessageSegment.text(str(error)))
        while "\n" in response_text:
             response_text = response_text.replace("\n", "")
        await matcher.finish(MessageSegment.text(response_text.strip()), block=True)
    else:
        await laugh_matcher.finish(
            MessageSegment.text(f"我在准备更精彩的笑话喵，等待{cd_time - cd:.0f}秒后再找我喵~"),
            at_sender=True, block=True)

@hitokoto_matcher.handle()
async def hitokoto(event: GroupMessageEvent, matcher: Matcher):   #定义异步函数hitokoto
    if not (await check_group_allow(str(event.group_id))):
        await dog_matcher.finish(notAllow, at_sender=True)
    uid = event.get_user_id()                                            # 获取用户id
    try:
        cd = event.time - hitokoto_CD_dir[uid]                           # 计算cd
    except KeyError:
        cd = cd_time + 1                                           # 没有记录则cd为cd_time+1
    if (
        cd > cd_time    
        or event.get_user_id() in nonebot.get_driver().config.superusers
    ):                                                                        # 记录cd    
        hitokoto_CD_dir.update({uid: event.time})
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://v1.hitokoto.cn?c=a&c=b&c=c&c=d&c=e&c=f&c=j")
        except Exception as error:
            await hitokoto_matcher.finish(MessageSegment.text(f"获取一言失败"), at_sender=True, block=True)
        data = response.json()
        msg = data["hitokoto"]
        add = ""
        if works := data["from"]:
            add += f"《{works}》"
        if from_who := data["from_who"]:
            add += f"{from_who}"
        if add:
            msg += f"\n——{add}"
        await matcher.finish(msg)
    else:
        await laugh_matcher.finish(
            MessageSegment.text(f"休息 {cd_time - cd:.0f}秒后才能再使用喵~"),
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