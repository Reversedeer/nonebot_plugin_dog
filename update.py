import os
import nonebot
import platform
from pathlib import Path
from nonebot.adapters.onebot.v11 import Bot

driver = nonebot.get_driver()

@driver.on_bot_connect
async def remind(bot: Bot):
    system = platform.system()
    if system == 'Linux':
        restart = Path() / "restart.sh"
        if not restart.exists():
            with open(restart, "w", encoding="utf8") as f:
                f.write(
                    (
                        f"pid=$(netstat -tunlp | grep {str(bot.config.port)}"
                         " | awk '{print $7}')\n"
                        "pid=${pid%/*}\n"
                        "kill -9 $pid\n"
                        "cd /bot/Nonebot2/"
                        "pip install --upgrade nonebot-plugin-dog\n"
                        "python3 bot.py"
                    )
                 )
            os.system("chmod +x ./restart.sh")
        Version = Path() / "new_version"
        if Version.exists():
            await bot.send_private_msg(
               user_id=int(list(bot.config.superusers)[0]), message="插件更新成功"
            )
            Version.unlink()