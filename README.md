<p align="center">
  <a href="https://nonebot.dev">
    <img src="https://nonebot.dev/logo.png" width="180" height="180" alt="NoneBot">
  </a>
</p>





<div align="center">

# nonebot-plugin-dog

_✨随机返回一句舔狗日记...(~~舔狗，舔到最后一无所有~~)✨_  

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/Reversedeer/nonebot_plugin_dog/main/LICENSE">
    <img src="https://img.shields.io/github/license/Reversedeer/nonebot_plugin_dog" alt="license">
  </a>
  <a href="https://camo.githubusercontent.com/c5bfbde247cd10e93ff50a518b0f5e441a6e9959495f6bf0f1a1913d2b1b7a8d/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f707974686f6e2d332e382b2d626c75652e737667">
    <img src="https://img.shields.io/badge/python-3.8+-blue?logo=python&logoColor=edb641" alt="python">
  </a>
  <a href="https://github.com/nonebot/nonebot2">
    <img src="https://img.shields.io/badge/nonebot-2+-red.svg">
  </a>
</p>

## 介绍: 点点Star✨

> 在群聊里发送“舔狗日记/一言”（等）命令时，bot返回一句舔狗日记/一言等文案
>
> 你可能需要在env里配置指令响应头 " / "，取决于你的command_start设置
>
> SUPERUSER | 群主 | 管理 可以使用：“开启/关闭文案”来控制指令开关（默认=true）
>
> 插件所有配置文件和备份目录在/date/dog/下
>
> ⚠️插件支持手动检查更新：Command: "/检查更新"，如果没有报错，发送: "/重启"完成bot更新，可不使用pip install --upgrade 更新

## 安装方式

### nb-cli(推荐)

```
nb plugin install nonebot_plugin_dog
```

<details>
    <summary><h3>pip</h3></summary>

```
pip install nonebot_plugin_dog
```

</details>

### 更新

```
pip install --upgrade nonebot-plugin-dog
```

#### 还可以在群内发送指令："/检查更新"来检查更新;  发送  "/重启"完成bot更新(推荐)

## 配置

在bot目录对应的.env.*文件中添加（有默认值，cd=0为不限制）

|   config    | type | default |    example     |           usage            |
| :---------: | :--: | :-----: | :------------: | :------------------------: |
|   dog_cd    | int  |   20    |  dog_cd = 20   |  调用''舔狗日记'cd默认值   |
|  laugh_cd   | int  |   20    |  laugh_cd=20   | 调用''讲个笑话''cd的默认值 |
| hitokoto_cd | int  |   20    | hitokoto_cd=20 |    调用"一言"cd的默认值    |
|  wenan_cd   | int  |   20    |  wenan_cd=20   |    调用“文案”cd的默认值    |

## 示例

<img width="100%" src="https://github.com/Reversedeer/nonebot_piugin_dog/blob/dev/image/image.png">

<img width="100% " src="https://github.com/Reversedeer/nonebot_plugin_dog/blob/dev/image/image2.png">

## TODO

- [x] 增加指令开关
- [x] 增加插件热更新
- [x] 增加CD限制
- [ ] 增加图片发送
- [x] 整合更多的API

<details>
    <summary><h2>更新日志</h2></summary>

- 0.3.0
  
  - 适配插件元数据
  
  - 优化代码
  
- 0.2.9
  - 修复热更新bug

- 0.2.8
  - 实现插件热更新

- 0.2.7.1
  - 增加"舔狗日记"api

  - 插件支持手动检测更新
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