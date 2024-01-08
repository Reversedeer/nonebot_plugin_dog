import os
import json
import nonebot

class Utils:
    def __init__(self) -> None:

        self.usage = """
        指令1：/舔狗日记
        指令2：/讲个笑话
        指令3：/一言
        指令4：/文案语录
        指令5：/检查更新
        指令6：/重启
        指令7：/开启|关闭文案
        """
        self.dog_CD_dir = {}  # 记录舔狗日记cd的字典
        self.laugh_CD_dir = {}  # 记录讲个笑话cd的字典
        self.hitokoto_CD_dir = {}  # 记录一言cd的字典
        self.wenan_CD_dir = {}  # 记录文案cd的字典
        self.current_version = '0.3.0'
        config = nonebot.get_driver().config  # 获取配置
        self.dog_cd: int = getattr(config, "dog_cd", 20)
        self.laugh_cd: int = getattr(config, "laugh_cd", 20)
        self.hitokoto_cd: int = getattr(config, "hitokoto_cd", 20)
        self.wenan_cd: int = getattr(config, "wenan_cd", 20)
        self.notAllow = "群内还未开启文案功能, 请管理员或群主发送\"开启文案\", \"关闭文案\"以开启/关闭该功能"

utils = Utils()

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




