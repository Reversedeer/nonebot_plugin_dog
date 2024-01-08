''' 插件入口'''
import os
import platform


from nonebot.params import ArgStr
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER
from nonebot import on_command, on_endswith
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11.permission import GROUP_OWNER, GROUP_ADMIN

from .utils import utils
from .handle import dog

on_endswith(
    "文案",
    permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER,
    priority=10,
    block=True,
    handlers=[dog.openstates]
)
on_command(
    "舔狗日记",
    aliases={"舔狗嘤嘤嘤"},
    priority=10,
    block=True,
    handlers=[dog.lickdog]
)
on_command(
    "讲个笑话",
    aliases={"说个笑话"},
    priority=10,
    block=True,
    handlers=[dog.laugh]
)
on_command(
    "一言",aliases={"一言"},
    priority=10,
    block=True,
    handlers=[dog.hitokoto]
)
on_command(
    "文案语录",
    aliases={"语录"},
    priority=10,
    block=True,
    handlers=[dog.wenan]
)
on_command(
    "检查更新",
    priority=1,
    permission=SUPERUSER,
    block=True,
    handlers=[dog.check]
)
restart = on_command(
    "重启",
    aliases={"restart"},
    priority=1,
    permission=SUPERUSER,
    block=True
)

@restart.got("flag", prompt="确定是否重启？确定请回复[是|好|确定]（重启失败咱们将失去联系，请谨慎！）")
async def _(matcher: Matcher, flag: str = ArgStr("flag")):
    if flag.lower() in {"true", "是", "好", "确定", "确定是"}:
        await matcher.send("开始重启..请稍等...")
        open("data/dog/new_version", "w")
        if str(platform.system()).lower() == "windows":
            import sys

            python = sys.executable
            os.execl(python, python, *sys.argv)
        else:
            os.system("./restart.sh")
    else:
        await matcher.send("已取消操作...")

__plugin_meta__ = PluginMetadata(
    name="dog",
    description="随机返回一句舔狗日记...嘤嘤嘤和其他文案的插件",
    usage=utils.usage,
    type="application",
    homepage="https://github.com/Reversedeer/nonebot_plugin_dog",
    supported_adapters={"~onebot.v11"},
    extra={
        "author": "Reversedeer",
        "version": "0.3.0",
        "priority": 10,
    }
)