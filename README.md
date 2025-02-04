# redbag_platform

给 Aurora 红包题随便搓的 flag 提交平台

启动前请修改 `src/config.json` 中的 `default_user` 默认账密

## 说明

`/flag` 页面用于选手提交 flag, 当 flag 正确时显示对应的红包口令

![flag](img/flag.png)

选手提交 flag 时需要输入标识个人身份的 token, 为了避免无关人士获取 token, 平台设置了**入场口令**

入场口令默认为 `Aurora祝您新年快乐`

如果需要变更入场口令, 请修改 `src/config.json` 中的 `enter_password`

`/admin` 是管理员页面, 实现了管理红包和题目的功能

![dashboard](img/dashboard.png)

在 `/admin/login` 进行管理员登录

## 快速使用

构建 docker 镜像

```
git clone https://github.com/Caterpie771881/redbag_platform.git

cd redbag_platform

docker build . -t redbag_platform
```

或者 直接使用 python 启动

```
git clone https://github.com/Caterpie771881/redbag_platform.git

cd redbag_platform

pip install -r requirements.txt

cd src

python app.py
```