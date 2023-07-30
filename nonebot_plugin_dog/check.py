import os
import shutil
import tarfile


from nonebot.adapters.onebot.v11 import Bot, Message

from .update import *
from .utils import *
# from .http_utils import AsyncHttpx

async def fetch_data(tar_gz_url):
    async with httpx.AsyncClient() as client:
        return await client.get(tar_gz_url)

async def download_file(tar_gz_url, latest_tar_gz):
    async with httpx.AsyncClient() as client:
        response = await client.get(tar_gz_url)
        if response.status_code == 200:
            with open(latest_tar_gz, "wb") as f:
                f.write(response.content)
                return True
        else:
            return False



async def check_update(bot: Bot):
    logger.info("开始更新插件...")
    data = await get_latest_version_data()
    if data:
        latest_version = data["name"]
        if current_version != latest_version:
            tar_gz_url = data["tarball_url"]
            logger.info(f"检测插件有更新，当前版本：{current_version}，最新版本：{latest_version}")
            await bot.send_private_msg(
                user_id=int(list(bot.config.superusers)[0]),
                message=f"检测插件有更新，当前版本：{current_version}，最新版本：{latest_version}\n" f"开始更新.....",
            )
            tar_gz_url = (await fetch_data(tar_gz_url)).headers.get("Location")
            if await download_file(tar_gz_url, latest_tar_gz):
                logger.info("下载插件最新版文件完成....")
                error = await _file_handle(latest_version)
                if error:
                    return 998, error
                logger.info("更新完毕，清理文件完成....")
                await bot.send_private_msg(
                    user_id=int(list(bot.config.superusers)[0]),
                    message=Message(
                            f"插件更新完成，版本：{current_version} -> {latest_version}\n"
                            f"更新日期：{data['created_at']}\n"
                    ),
                )
                return 200, ""
            else:
                logger.warning(f"下载最新版本失败...版本号：{latest_version}")
                await bot.send_private_msg(
                    user_id=int(list(bot.config.superusers)[0]),
                    message=f"下载最新版本失败qwq...版本号：{latest_version}",
                )
        else:
            logger.info(f"自动获取版本成功：{latest_version}，当前版本为最新版，无需更新...")
            await bot.send_private_msg(
                user_id=int(list(bot.config.superusers)[0]),
                message=f"自动获取版本成功：{latest_version}，当前版本为最新版，无需更新...",
            )
    else:
        logger.warning("自动获取版本失败....")
        await bot.send_private_msg(
            user_id=int(list(bot.config.superusers)[0]), message="自动获取版本失败...."
        )
    return 999, ""


async def _file_handle(latest_version: str) -> str:
    if not temp_dir.exists():
        temp_dir.mkdir(exist_ok=True, parents=True)
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    tf = None
    backup_dir.mkdir(exist_ok=True, parents=True)
    logger.info("开始解压真寻文件压缩包....")
    tf = tarfile.open(latest_tar_gz)
    tf.extractall(temp_dir)
    logger.info("解压真寻文件压缩包完成....")
    latest_file = Path(temp_dir) / os.listdir(temp_dir)[0]
    update_info_file = Path(latest_file) / os.listdir(latest_file)[1]
    update_info = json.load(open(update_info_file, "r", encoding="utf8"))
    update_file = update_info["update_file"]
    add_file = update_info["add_file"]
    delete_file = update_info["delete_file"]
    config_file = config_path / "configs" / "config.py"
    config_path_file = config_path / "configs" / "path_config.py"

    for file in delete_file + update_file:
        if file != "configs":
            file = Path() / file
            backup_file = Path(backup_dir) / file
            if file.exists():
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                if backup_file.exists():
                    backup_file.unlink()
                if file not in [config_file, config_path_file]:
                    shutil.move(file.absolute(), backup_file.absolute())
                else:
                    with open(file, "r", encoding="utf8") as rf:
                        data = rf.read()
                    with open(backup_file, "w", encoding="utf8") as wf:
                        wf.write(data)
                logger.info(f"已备份文件：{file}")
    for file in add_file + update_file:
        new_file = Path(latest_file) / file
        old_file = Path() / file
        if (
            old_file not in [config_file, config_path_file]
            and file != "configs"
            and not old_file.exists()
            and new_file.exists()
        ):
            shutil.move(new_file.absolute(), old_file.absolute())
            logger.info(f"已更新文件：{file}")
    if tf:
        tf.close()
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    if latest_tar_gz.exists():
        latest_tar_gz.unlink()
    local_update_info_file = Path() / "update_info.json"
    if local_update_info_file.exists():
        local_update_info_file.unlink()
    with open(version_file, "w", encoding="utf-8") as f:
        f.write(f"{latest_version}")
    os.system(f"poetry run pip install -r {(Path() / 'pyproject.toml').absolute()}")
    return ""
