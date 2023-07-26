import re
import httpx
import nonebot
import random
import contextlib

from re import I
from nonebot.params import ArgStr
from nonebot.typing import T_State
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN
from nonebot.adapters.onebot.v11 import MessageSegment, GroupMessageEvent

from .utils import *


openstats = on_regex(
    r"^(开启文案|关闭文案)",
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    flags=I,
    priority=1,
    block=True
    )

dog_matcher = on_command(
    "舔狗日记",
    aliases={"舔狗嘤嘤嘤"},
    priority=10,
    block=True
    )

laugh_matcher = on_command(
    "讲个笑话",
    aliases={"说个笑话"},
    priority=10,
    block=True
    )

hitokoto_matcher = on_command(
    "一言",aliases={"一言"},
    priority=10,
    block=True
    )

wenan_matcher = on_command(
    "文案",
    aliases={"语录"},
    priority=10,
    block=True
    )
check = on_command(
    "检查更新",
    priority=1,
    permission=SUPERUSER,
    block=True
    )

restart = on_command(
    "重启",
    aliases={"restart"},
    priority=1,
    permission=SUPERUSER,
    block=True
    )

@dog_matcher.handle()
async def dog(event: GroupMessageEvent, matcher: Matcher):     # 定义异步函数 dog
    if not (await check_group_allow(str(event.group_id))):
        await dog_matcher.finish(notAllow, at_sender=True)
    uid = event.get_user_id()                                         # 获取用户id
    try:
        cd = event.time - dog_CD_dir[uid]                             # 计算cd
    except KeyError:
        cd = dog_cd + 1                                        # 没有记录则cd为cd_time+1
    if (
        cd > dog_cd
        or event.get_user_id() in nonebot.get_driver().config.superusers
    ):                                                                     # 记录cd
        dog_CD_dir.update({uid: event.time})
        urls = ["https://api.mxycn.cn/api/tgrj.php", "https://api.oick.cn/dog/api.php"]
        url = random.choice(urls)
        try:
            # 使用 httpx.AsyncClient 获取 API，存储为 response 变量
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                response_text = response.text
        except Exception as error:
            await dog_matcher.finish(MessageSegment.text(str(error)))
        await matcher.finish(MessageSegment.text(response_text.strip()), block=True)
    else:
        await dog_matcher.finish(
            MessageSegment.text(f"不要深情了喵，休息{dog_cd - cd:.0f}秒后再找我喵~"),
            at_sender=True, block=True)


@laugh_matcher.handle()
async def laugh(event: GroupMessageEvent, matcher: Matcher):     # 定义异步函数 laugh
    if not (await check_group_allow(str(event.group_id))):
        await dog_matcher.finish(notAllow, at_sender=True)
    uid = event.get_user_id()                                           # 获取用户id
    try:
        cd = event.time - laugh_CD_dir[uid]                             # 计算cd
    except KeyError:
        cd = laugh_cd + 1                                          # 没有记录则cd为cd_time+1
    if (
        cd > laugh_cd
        or event.get_user_id() in nonebot.get_driver().config.superusers
    ):                                                                       # 记录cd
        laugh_CD_dir.update({uid: event.time})
        try:
            # 使用 httpx.AsyncClient 获取 API，存储为 response 变量
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.mxycn.cn/api/qwxh.php")
                response_text = response.text
        except Exception as error:
            await laugh_matcher.finish(MessageSegment.text(str(error)))
        response_text = re.sub(r'。。\\n', '\n', response_text)
        response_text = response_text.replace('。。', '')
        await matcher.finish(MessageSegment.text(response_text.strip()), block=True)
    else:
        await laugh_matcher.finish(
            MessageSegment.text(f"我在准备更精彩的笑话喵，等待{laugh_cd - cd:.0f}秒后再找我喵~"),
            at_sender=True, block=True)


@hitokoto_matcher.handle()
async def hitokoto(event: GroupMessageEvent, matcher: Matcher):  # 定义异步函数hitokoto
    if not (await check_group_allow(str(event.group_id))):
        await dog_matcher.finish(notAllow, at_sender=True)
    uid = event.get_user_id()                                            # 获取用户id
    try:
        cd = event.time - hitokoto_CD_dir[uid]                           # 计算cd
    except KeyError:
        # 没有记录则cd为cd_time+1
        cd = hitokoto_cd + 1
    if (
        cd > hitokoto_cd
        or event.get_user_id() in nonebot.get_driver().config.superusers
    ):                                                                        # 记录cd
        hitokoto_CD_dir.update({uid: event.time})
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get("https://v1.hitokoto.cn?c=a&c=b&c=c&c=d&c=e&c=f&c=j")
        except Exception as error:
            await hitokoto_matcher.finish(
                MessageSegment.text("获取一言失败"), at_sender=True, block=True
            )
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
            MessageSegment.text(f"休息 {hitokoto_cd - cd:.0f}秒后才能再使用喵~"),
            at_sender=True, block=True)


@wenan_matcher.handle()
async def wenan(event: GroupMessageEvent, matcher: Matcher):  # 定义异步函数wenan
    if not (await check_group_allow(str(event.group_id))):
        await wenan_matcher.finish(notAllow, at_sender=True)
    uid = event.get_user_id()                                            # 获取用户id
    try:
        cd = event.time - wenan_CD_dir[uid]                           # 计算cd
    except KeyError:
        cd = wenan_cd + 1                                           # 没有记录则cd为cd_time+1
    if (
        cd > wenan_cd
        or event.get_user_id() in nonebot.get_driver().config.superusers
    ):                                                                        # 记录cd
        wenan_CD_dir.update({uid: event.time})
        try:
            # 使用 httpx.AsyncClient 获取 API，存储为 response 变量
            async with httpx.AsyncClient() as client:
                response = await client.get("https://api.mxycn.cn/api/sgyl.php")
                response_text = response.text
        except Exception as error:
            await laugh_matcher.finish(MessageSegment.text(str(error)))
        await matcher.finish(MessageSegment.text(response_text.strip()), block=True)
    else:
        await laugh_matcher.finish(
            MessageSegment.text(f"文案准备中喵，等待{wenan_cd - cd:.0f}秒后再找我喵~"),
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
        else:
            groupdata.update({gid: {"allow": True}})
        write_group_data()
        await openstats.finish("功能已开启喵~")
    elif "关闭文案" in command:
        if gid in groupdata:
            groupdata[gid]["allow"] = False
        else:
            groupdata.update({gid: {"allow": False}})
        write_group_data()
        await openstats.finish("功能已禁用喵~")

@check.handle()
async def check_update():
    async with httpx.AsyncClient() as client:
        response = await client.get('https://pypi.org/pypi/nonebot-plugin-dog/json')
        data = response.json()
        latest_version = data['info']['version']
        if current_version != latest_version:
            await check.finish((f'=======插件更新=======\nnonebot-plugin-dog\n当前Version: {current_version}\n最新Version: {latest_version}\n======插件可更新======'), block = False)
        else:
            await check.finish((f'=======插件更新=======\nnonebot-plugin-dog\n当前Version：{latest_version}\n======插件已最新======'), block=False)

@restart.got("flag", prompt="确定是否重启？确定请回复[是|好|确定]（重启失败咱们将失去联系，请谨慎！）")
async def _(flag: str = ArgStr("flag")):
    if flag.lower() in {"true", "是", "好", "确定", "确定是"}:
        await restart.send("开始重启..请稍等...")
        open("new_version", "w")
        os.system("./restart.sh")
    else:
        await restart.send("已取消操作...")
@restart.handle()
async def _():
        await restart.send("开始重启..请稍等...")
        open("new_version", "w")
        os.system("./restart.sh")

@restart.got("flag", prompt="确定是否重启？确定请回复[是|好|确定]（重启失败咱们将失去联系，请谨慎！）")
async def _(matcher: Matcher, flag: str = ArgStr("flag")):
    if flag.lower() in {"true", "是", "好", "确定", "确定是"}:
        await matcher.send("开始重启..请稍等...")
        open("new_version", "w")
        os.system("./restart.sh")
    else:
        await matcher.send("已取消操作...")


with contextlib.suppress(Exception):
    from nonebot.plugin import PluginMetadata

    __plugin_meta__ = PluginMetadata(
        name="dog",
        description="随机返回一句舔狗日记...嘤嘤嘤和其他文案的插件",
        usage=utils.usage,
        type="application",
        homepage="https://github.com/Reversedeer/nonebot_plugin_dog",
        supported_adapters={"onebot.v11"},
        extra={
            "author": "Reversedeer",
            "version": "0.2.8",
            "priority": 10,
        },
    )