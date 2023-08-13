# Reversedeer's Hypixel Bot

### 安装依赖

```
pip3 install requests
```

```
pip3 install pillow
```

> Windows用户请替换 pip3 -> pip

### 使用go-cqhttp连接bot

使用HTTP通信方式

```
servers:
  - http: # HTTP 通信设置
      address: 0.0.0.0:5700 # HTTP监听地址
      timeout: 5      # 反向 HTTP 超时时间, 单位秒，<5 时将被忽略
      long-polling:   # 长轮询拓展
        enabled: false       # 是否开启
        max-queue-size: 2000 # 消息队列大小，0 表示不限制队列大小，谨慎使用
      middlewares:
        <<: *default # 引用默认中间件
      post:           # 反向HTTP POST地址列表
      #- url: ''                # 地址
      #  secret: ''             # 密钥
      #  max-retries: 3         # 最大重试，0 时禁用
      #  retries-interval: 1500 # 重试时间，单位毫秒，0 时立即
      #- url: http://127.0.0.1:5701/ # 地址
      #  secret: ''                  # 密钥
      #  max-retries: 10             # 最大重试，0 时禁用
      #  retries-interval: 1000      # 重试时间，单位毫秒，0 时立即
```

> 在bot.py里修改端口与HTTP监听端口一致

### 获取APIKEY

你需要从[Hypixel开发者仪表盘](https://developer.hypixel.net/)申请APIKEY(如何申请请自行搜索，没有账号请先注册论坛账号)

你还需要从[Antisniper Public API](https://api.antisniper.net/)申请API

然后写入bot.py中(搜关键词填写)

### 运行

```
./go-cqhttp --faststart
```

```
python3 bot.py
```

