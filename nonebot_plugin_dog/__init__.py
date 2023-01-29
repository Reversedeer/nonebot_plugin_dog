import httpx
from nonebot import logger, on_command
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.params import CommandArg

dog_matcher = on_command("舔狗日记", aliases={"舔狗嘤嘤嘤"})

@dog_matcher.handle()
async def dog(matcher: Matcher, args: Message = CommandArg()):
    if args:
        return
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.juncikeji.xyz/api/tgrj.php")
    if response.is_error:
        logger.error("获取失败")
        return
    data = response.text
    await matcher.finish(data)


# from nonebot.plugin.on import on_command
# from nonebot.adapters.onebot.v11 import Message
# from nonebot.params import CommandArg
# from httpx import AsyncClient


# dog = on_command('舔狗日记 ', aliases={'舔狗日记 '}, priority=60, block=True)

# @dog.handle()
# async def _(msg: Message = CommandArg()):
#     url = msg.extract_plain_text().strip()
#     api = f'https://api.juncikeji.xyz/api/tgrj.php'

#     message = await api_call(api)

#     await dog.finish(message)



# async def api_call(api):
#     async with AsyncClient() as client:
#             res = (await client.get(api)).json()
#             if res["code"] == 200:
#                 url = (res["data"]["域名"])
#                 ip = (res["data"]["IP"])
#                 max = (res["data"]["最大延迟"])
#                 min = (res["data"]["最小延迟"])
#                 place = (res["data"]["服务器归属地"])
#                 res = f"域名: {url}\nIP: {ip}\n最大延迟: {max}\n最小延迟: {min}\n服务器归属地: {place}"
#                 return res
#             elif res["code"] == 201:
#                 res = (res["data"])
#                 return res
#             else:
#                 return "寄"