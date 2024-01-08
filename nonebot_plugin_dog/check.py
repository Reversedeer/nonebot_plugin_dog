import os
import httpx
import shutil
import tarfile

from pathlib import Path
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, Message

from .update import config
from .utils import utils


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
    global latest_version
    logger.info("开始更新插件...")
    data = await config.get_latest_version_data()
    if data:
        latest_version = data["name"]
        if utils.current_version != latest_version:
            tar_gz_url = data["tarball_url"]
            logger.info(f"检测插件dog:有更新，当前版本：{utils.current_version}，最新版本：{latest_version}")
            await bot.send_private_msg(
                user_id=int(list(bot.config.superusers)[0]),
                message=f"检测插件:dog有更新，当前版本：{utils.current_version}，最新版本：{latest_version}\n" f"开始更新.....",
            )
            tar_gz_url = (await fetch_data(tar_gz_url)).headers.get("Location")
            if await download_file(tar_gz_url, config.latest_tar_gz):
                logger.info("下载插件最新版文件完成....")
                error = await _file_handle(latest_version)
                if error:
                    return 998, error
                logger.info("更新完毕，清理文件完成....")
                await bot.send_private_msg(
                    user_id=int(list(bot.config.superusers)[0]),
                    message=Message(
                            f"插件更新完成，版本：{utils.current_version} -> {latest_version}\n"
                            f"插件更新日期：{data['created_at']}\n"
                    ),
                )
                return 200, ""
            else:
                logger.warning(f"下载最新版本失败..请检查网络是否通畅.版本号：{latest_version}")
                await bot.send_private_msg(
                    user_id=int(list(bot.config.superusers)[0]),
                    message=f"下载最新版本失败qwq..请检查网络是否通畅.版本号：{latest_version}",
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
    # 接收最新版本号作为参数，并返回处理结果字符串
    
    if not config.temp_dir.exists():
        # 检查临时目录是否存在，如果不存在则创建
        config.temp_dir.mkdir(exist_ok=True, parents=True)
    
    if config.backup_dir.exists():
        # 如果备份目录存在，则删除整个备份目录
        shutil.rmtree(config.backup_dir)
    
    tf = None
    # 初始化一个tarfile对象tf
    
    config.backup_dir.mkdir(exist_ok=True, parents=True)
    # 创建备份目录，如果备份目录已存在，则不会重新创建
    
    logger.info("开始解压文件压缩包....")
    # 记录日志，表示开始解压文件压缩包
    tf = tarfile.open(config.latest_tar_gz)
    # 打开文件压缩包，获取tarfile对象tf
    tf.extractall(config.temp_dir)
    # 将压缩包中的所有文件解压到临时目录temp_dir中
    logger.info("解压文件压缩包完成....")
    # 记录日志，表示解压文件压缩包完成
    
    latest_file = Path(config.temp_dir) / os.listdir(config.temp_dir)[0]
    # 获取临时目录中的第一个文件，作为最新版本的文件夹路径
    update_info_file = Path(latest_file) / os.listdir(latest_file)[1]
    # 获取最新版本文件夹中的第二个文件，作为更新信息文件的路径
    try:

        pycache_dir = os.path.join(config.destination_directory, '__pycache__')
        if os.path.exists(pycache_dir):
            shutil.rmtree(pycache_dir)

        for file in os.listdir(config.destination_directory):
            if file != '__pycache__':
                logger.info("正在备份插件目录...")
                temp_file = os.path.join(config.destination_directory, file)
                backup_file = os.path.join(config.backup_dir, file)
                shutil.copy2(temp_file, backup_file)
                logger.info("文件备份成功")

        
        for file in os.listdir(update_info_file):
            logger.info("开始更新插件...")
            updata_file = os.path.join(update_info_file, file)
            destination_file = os.path.join(config.destination_directory, file)
            shutil.copy2(updata_file, destination_file)
            logger.info("插件更新成功!")
    except Exception as e:
        raise e

    if tf:
        tf.close()
        # 关闭tarfile对象，释放资源
    if config.temp_dir.exists():
        shutil.rmtree(config.temp_dir)
        # 删除临时目录及其中的所有文件
    if config.latest_tar_gz.exists():
        config.latest_tar_gz.unlink()
        # 删除最新版本的压缩包文件

    with open(config.version_file, "w", encoding="utf-8") as f:
        f.write(f"{latest_version}")
        # 将最新版本号写入版本文件中

    os.system(f"poetry run pip install -r {(update_info_file / 'pyproject.toml').absolute()}")
    # 使用os.system命令执行shell命令，安装更新后的依赖包

    return ""
    # 返回一个空字符串

