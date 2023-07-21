<p align="center">
  <a href="https://v2.nonebot.dev/store">
    <img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
  </a>
</p>



<div align="center">

# nonebot-plugin-dog

_✨随机返回一句舔狗日记...(~~舔狗，舔到最后一无所有~~)✨_  

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/Mrs4s/go-cqhttp/master/LICENSE">
    <img src="https://img.shields.io/github/license/Mrs4s/go-cqhttp" alt="license">
  </a>
  <a href="https://camo.githubusercontent.com/c5bfbde247cd10e93ff50a518b0f5e441a6e9959495f6bf0f1a1913d2b1b7a8d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d332e382b2d626c75652e737667">
    <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="python">
  </a>
  <a href="https://github.com/howmanybots/onebot/blob/master/README.md">
    <img src="https://img.shields.io/badge/NoneBot2-blue?style=flat&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==" alt="cqhttp">
  </a>
</p>






## 介绍

当在群聊里发送“舔狗日记/一言”（等）命令时，bot会回复一句舔狗日记/一言文案......（等）

有可能需要加指令头 " / "，取决于你的command_start设置

SUPERUSER | 群主 | 管理 可以使用：“开启/关闭文案”来控制指令开关（默认=true）

群数据在/bot目录/Date/dog/下

⚠️插件支持手动检查更新：Command: "/检查更新"

## 安装方式

### nb-cli安装(推荐)

```
nb plugin install nonebot_plugin_dog
```

<details>
    <summary><h3>pip</h3></summary>


```
pip install nonebot-plugin-dog
```

打开 nonebot2 项目的 `bot.py` 文件, 在其中写入


    nonebot.load_plugin("nonebot_plugin_dog")

在’pyproject.toml‘文件中写入

    "nonebot_plugin_dog"

</details>

<details>
    <summary><h3>git clone</h3></summary>


```
git clone https://github.com/Reversedeer/nonebot_piugin_dog.git
```

</details>

### 更新

```
pip install --upgrade nonebot-plugin-dog
```

## 配置

在bot目录对应的.env.*文件中添加（有默认值，cd=0为不限制）

|   config    | type | default |    example     |           usage            |
| :---------: | :--: | :-----: | :------------: | :------------------------: |
|   dog_cd    | int  |   20    |  dog_cd = 20   |  调用''舔狗日记'cd默认值   |
|  laugh_cd   | int  |   20    |  laugh_cd=20   | 调用''讲个笑话''cd的默认值 |
| hitokoto_cd | int  |   20    | hitokoto_cd=20 |    调用"一言"cd的默认值    |
|  wenan_cd   | int  |   20    |  wenan_cd=20   |    调用“文案”cd的默认值    |

## 示例

<img width="300" src="https://github.com/Reversedeer/nonebot_piugin_dog/blob/main/image/image.jpg">

<img width="300 " src="https://github.com/Reversedeer/nonebot_plugin_dog/blob/main/image/image2.jpg">

## TODO

- [x] 增加指令开关

- [x] 增加CD限制
- [ ] 增加图片发送
- [x] 整合更多的API
- [x] 修复文本末尾多出的空行[#issue1](https://github.com/Reversedeer/nonebot_plugin_dog/issues/1)

<details>
    <summary><h2>更新日志</h2></summary>
- 0.2.7  #2023-3-13

  -更新api

- 0.2.7.1
  - 增加"舔狗日记"api
  
  - 插件支持~~自动/~~手动检测更新
  
- 0.2.7  # 2023-3-13
  - 修复api

- 0.2.6  #2023-3-5
  - 修复了文案中存在换行符，且无法换行的错误

  - 优化cd逻辑，可以分别对应每一个指令

  - 整合了更多的api

- 0.2.5  #2023-3-3
  - 整合了更多的api
  - 优化cd模式

- 0.2.3   #2023-2-1
  - 修复文本末多出的空行
  -  修复readme中的错误
  - 增加指令开关
  - 更改指令CD默认值为20
- 0.1.9   #2023-1-30
  - 增加cd限制  
- 0.1.0   #2023-1-29
  - 发布并优化代码   

</details>

## 关于 ISSUE

以下 ISSUE 会被直接关闭

- 提交 BUG 不使用 Template
- 询问已知问题
- 提问找不到重点
- 重复提问

> 请注意, 开发者并没有义务回复您的问题. 您应该具备基本的提问技巧。  
> 有关如何提问，请阅读[《提问的智慧》](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md)



## 其他插件

[QQ群消息，事件检测插件](https://github.com/Reversedeer/nonebot_plugin_eventmonitor)