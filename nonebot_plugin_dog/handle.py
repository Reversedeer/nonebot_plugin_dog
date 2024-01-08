import re
import httpx
import random
import nonebot

from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, GroupMessageEvent, Bot

from .check import check_update
from .utils import utils, check_group_allow, write_group_data, groupdata

class Dog:
    @staticmethod
    async def lickdog(matcher: Matcher, event: GroupMessageEvent):     # 定义异步函数 dog
        if not (await check_group_allow(str(event.group_id))):
            await matcher.finish(utils.notAllow, at_sender=True)
        uid = event.get_user_id()                                         # 获取用户id
        try:
            cd = event.time - utils.dog_CD_dir[uid]                             # 计算cd
        except KeyError:
            cd = utils.dog_cd + 1                                        # 没有记录则cd为cd_time+1
        if (
            cd > utils.dog_cd
            or event.get_user_id() in nonebot.get_driver().config.superusers
        ):                                                                     # 记录cd
            utils.dog_CD_dir.update({uid: event.time})
            urls = ["https://api.mxycn.cn/api/tgrj.php", "https://api.oick.cn/dog/api.php"]
            url = random.choice(urls)
            try:
                # 使用 httpx.AsyncClient 获取 API，存储为 response 变量
                async with httpx.AsyncClient() as client:
                    response = await client.get(url)
                    response_text = response.text
            except Exception as error:
                await matcher.finish(MessageSegment.text(str(error)))
            await matcher.finish(MessageSegment.text(response_text.strip()), block=True)
        else:
            await matcher.finish(
                MessageSegment.text(f"不要深情了喵，休息{utils.dog_cd - cd:.0f}秒后再找我喵~"),
                at_sender=True, block=True)

    @staticmethod
    async def laugh(event: GroupMessageEvent, matcher: Matcher):     # 定义异步函数 laugh
        if not (await check_group_allow(str(event.group_id))):
            await matcher.finish(utils.notAllow, at_sender=True)
        uid = event.get_user_id()                                           # 获取用户id
        try:
            cd = event.time - utils.laugh_CD_dir[uid]                             # 计算cd
        except KeyError:
            cd = utils.laugh_cd + 1                                          # 没有记录则cd为cd_time+1
        if (
            cd > utils.laugh_cd
            or event.get_user_id() in nonebot.get_driver().config.superusers
        ):                                                                       # 记录cd
            utils.laugh_CD_dir.update({uid: event.time})
            try:
                # 使用 httpx.AsyncClient 获取 API，存储为 response 变量
                async with httpx.AsyncClient() as client:
                    response = await client.get("https://api.mxycn.cn/api/qwxh.php")
                    response_text = response.text
            except Exception as error:
                await matcher.finish(MessageSegment.text(str(error)))
            response_text = re.sub(r'。。\\n', '\n', response_text)
            response_text = response_text.replace('。。', '')
            await matcher.finish(MessageSegment.text(response_text.strip()), block=True)
        else:
            await matcher.finish(
                MessageSegment.text(f"我在准备更精彩的笑话喵，等待{utils.laugh_cd - cd:.0f}秒后再找我喵~"),
                at_sender=True, block=True)


    @staticmethod
    async def hitokoto(event: GroupMessageEvent, matcher: Matcher):  # 定义异步函数hitokoto
        if not (await check_group_allow(str(event.group_id))):
            await matcher.finish(utils.notAllow, at_sender=True)
        uid = event.get_user_id()                                            # 获取用户id
        try:
            cd = event.time - utils.hitokoto_CD_dir[uid]                           # 计算cd
        except KeyError:
            # 没有记录则cd为cd_time+1
            cd = utils.hitokoto_cd + 1
        if (
            cd > utils.hitokoto_cd
            or event.get_user_id() in nonebot.get_driver().config.superusers
        ):                                                                        # 记录cd
            utils.hitokoto_CD_dir.update({uid: event.time})
            try:
                async with httpx.AsyncClient() as client:
                    response = await client.get("https://v1.hitokoto.cn?c=a&c=b&c=c&c=d&c=e&c=f&c=j")
            except Exception as error:
                await matcher.finish(
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
            await matcher.finish(
                MessageSegment.text(f"休息 {utils.hitokoto_cd - cd:.0f}秒后才能再使用喵~"),
                at_sender=True, block=True)


    @staticmethod
    async def wenan(event: GroupMessageEvent, matcher: Matcher):  # 定义异步函数wenan
        if not (await check_group_allow(str(event.group_id))):
            await matcher.finish(utils.notAllow, at_sender=True)
        uid = event.get_user_id()                                            # 获取用户id
        try:
            cd = event.time - utils.wenan_CD_dir[uid]                           # 计算cd
        except KeyError:
            cd = utils.wenan_cd + 1                                           # 没有记录则cd为cd_time+1
        if (
            cd > utils.wenan_cd
            or event.get_user_id() in nonebot.get_driver().config.superusers
        ):                                                                        # 记录cd
            utils.wenan_CD_dir.update({uid: event.time})
            try:
                # 使用 httpx.AsyncClient 获取 API，存储为 response 变量
                async with httpx.AsyncClient() as client:
                    response = await client.get("https://api.mxycn.cn/api/sgyl.php")
                    response_text = response.text
            except Exception as error:
                await matcher.finish(MessageSegment.text(str(error)))
            await matcher.finish(MessageSegment.text(response_text.strip()), block=True)
        else:
            await matcher.finish(
                MessageSegment.text(f"文案准备中喵，等待{utils.wenan_cd - cd:.0f}秒后再找我喵~"),
                at_sender=True, block=True)

    @staticmethod
    async def openstates(event: GroupMessageEvent, matcher: Matcher):
        gid = str(event.group_id)  # 群号
        # 获取用户输入的参数
        command = event.message.extract_plain_text().replace("文案", "")
        if command == "开启":
            if gid in groupdata:
                groupdata[gid]["allow"] = True
            else:
                groupdata.update({gid: {"allow": True}})
            write_group_data()
            await matcher.finish("功能已开启喵~")
        elif "关闭" in command:
            if gid in groupdata:
                groupdata[gid]["allow"] = False
            else:
                groupdata.update({gid: {"allow": False}})
            write_group_data()
            await matcher.finish("功能已禁用喵~")
        else:
            return

    @staticmethod
    async def check(bot: Bot, event: MessageEvent):
        try:
            code, error = await check_update(bot)
            if error:
                logger.error(f"错误: {error}", "插件检查更新")
                await bot.send_private_msg(
                    user_id=event.user_id, message=f"更新插件dog更新时发生未知错误 {error}"
                )
        except Exception as e:
            logger.error("更新插件dog时发生未知错误", "检查更新", e=e)
            await bot.send_private_msg(
                user_id=event.user_id,
                message=f"更新插件dog时发生未知错误 {type(e)}: {e}",
            )
        else:
            if code == 200:
                await bot.send_private_msg(user_id=event.user_id, message="更新完毕，请重启bot....")

dog = Dog()