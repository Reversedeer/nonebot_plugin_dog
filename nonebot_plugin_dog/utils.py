import os
import json
import nonebot
from nonebot.adapters.onebot.v11 import GroupMessageEvent

if os.path.exists("data/dog/groupdata.json"):  # 读取用户数据
    with open("data/dog/groupdata.json", "r", encoding="utf-8") as f:
        groupdata = json.load(f)
else:   # 不存在则创建
    if not os.path.exists("data/dog"):
        os.makedirs("data/dog")  # 创建文件夹
    groupdata = {}

async def check_group_allow(gid: str) -> bool:
    #检查群是否允许
    if gid not in groupdata:
        groupdata[gid] = {"allow": True}# 写入默认值为true
    return groupdata[gid]["allow"]

def write_group_data() -> None:
    #写入群配置
    with open("data/dog/groupdata.json", "w", encoding="utf-8") as f:
        json.dump(groupdata, f, indent=4)

notAllow = "群内还未开启文案功能, 请管理员或群主发送\"开启文案\", \"关闭文案\"以开启/关闭该功能"