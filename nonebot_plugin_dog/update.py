import os
import httpx
import nonebot
import platform

from pathlib import Path
from nonebot.log import logger

from nonebot.adapters.onebot.v11 import Bot


driver = nonebot.get_driver()

release_url = "https://api.github.com/repos/Reversedeer/nonebot_plugin_dog/releases/latest"

config_path = Path() / "data/dog"
latest_tar_gz = config_path / "latest_file.tar.gz"
temp_dir = config_path / "temp"
backup_dir = config_path / "backup"
version_file = config_path / "new_version"
# 目标文件夹
destination_directory = 'src/plugins/nonebot_plugin_dog'  

@driver.on_bot_connect
async def remind(bot: Bot):
    system = platform.system()
    if system != 'windows':
        restart = config_path / "restart.sh"
        if not restart.exists():
            with open(restart, "w", encoding="utf8") as f:
                f.write(
                    (
                        f"pid=$(netstat -tunlp | grep {str(bot.config.port)}"
                        + " | awk '{print $7}')\n"
                        "pid=${pid%/*}\n"
                        "kill -9 $pid\n"
                        "sleep 3\n"
                        "python3 bot.py"
                    )
                 )
            os.system("chmod +x ./restart.sh")
            logger.info("已自动生成 restart.sh(重启) 文件，请检查脚本是否与本地指令符合...")
        Version = version_file
        if Version.exists():
            await bot.send_private_msg(
               user_id=int(list(bot.config.superusers)[0]),
               message="插件更新成功"
            )
            Version.unlink()


async def get_latest_version_data() -> dict:
    for _ in range(3):
        try:
            async with httpx.AsyncClient() as client:
                res = await client.get(release_url)
                if res.status_code == 200:
                    return res.json()
        except TimeoutError:
            pass
        except Exception as e:
            logger.error("检查最新版本失败")
    return {}
