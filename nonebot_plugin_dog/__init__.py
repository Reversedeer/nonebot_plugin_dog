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
