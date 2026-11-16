# 使用与下载教程

[返回项目首页](../README.md)

## 先选你需要的方式

| 你的目标 | 建议方式 |
| --- | --- |
| 直接把小杰当作伙伴使用 | 打开[公开分享页](https://chatgpt.com/s/sharepet_6af9c4f76ec481919fca50a0cffb36e1)添加 |
| 先看看效果 | 打开[完整动图](../previews/all-states.gif)或[视频](../previews/all-states.mp4) |
| 保存到电脑、以后再安装 | 从 [Releases](https://github.com/tblshigg/fantasy-xiaojie-pixel/releases/latest) 下载 PNG 或完整 ZIP |
| 修改颜色、表情或动作 | 下载完整项目，阅读[开发说明](DEVELOPMENT.md) |

下载和观看预览不需要安装 Python。伙伴功能是否可用，取决于你所用应用的版本、账户和工作区。

## 方式一：通过公开分享页添加

1. 打开[范特西小杰分享页](https://chatgpt.com/s/sharepet_6af9c4f76ec481919fca50a0cffb36e1)。
2. 如页面要求登录，使用你准备安装伙伴的账户登录。
3. 按页面显示的添加或安装提示，将小杰加入自己的伙伴收藏。
4. 打开支持 Pets 的桌面应用，进入 **Settings → Pets**，选择“范特西小杰”。
5. 在聊天中输入 `/pet`，或从命令菜单选择 **Show pet**，显示悬浮伙伴。

如果分享页未显示添加入口，继续尝试下面的本地安装方式；不同应用和账户可能提供不同入口。不要把截图或 GIF 当作精灵图上传。

## 方式二：下载完整包并打开安装页

1. 进入 [最新 Release](https://github.com/tblshigg/fantasy-xiaojie-pixel/releases/latest)。
2. 展开页面下方的 **Assets**，下载 `fantasy-xiaojie-pixel-v1.0.0.zip`。
3. 解压 ZIP，找到项目根目录中的 `install.html`。
4. 用浏览器打开该文件，点击页面中的桌面安装按钮。
5. 如浏览器询问是否打开已安装的应用，确认目标应用正确后按提示继续。
6. 完成应用内的安装流程，再从伙伴设置中选择小杰。

该安装页使用官方支持的 `codex://pets/install` 深链接，并从本仓库的公开 HTTPS 地址获取 v2 精灵图。需要已安装兼容的桌面应用、可访问的网络和已启用的伙伴安装功能。安装入口参数见 [OpenAI 官方 Commands 文档](https://learn.chatgpt.com/docs/reference/commands)。

如果浏览器提示无法识别 `codex://` 协议，可改用分享页，或使用应用中实际提供的自定义伙伴上传入口。

## 方式三：手动上传 PNG

### 选择文件

| 文件 | 规格 | 内容 |
| --- | --- | --- |
| [fantasy-xiaojie-v2.png](../assets/fantasy-xiaojie-v2.png) | 1536 × 2288，8 列 × 11 行 | 九组标准动作、十六个视线方向，共 73 帧 |
| [fantasy-xiaojie-v1.png](../assets/fantasy-xiaojie-v1.png) | 1536 × 1872，8 列 × 9 行 | 九组标准动作，共 57 帧 |

这里的 **v1 / v2 是精灵图格式**，`v1.0.0` 是本项目的发布版本号。

- 支持 v2 格式的安装入口，优先使用 v2 文件。
- 如果上传界面明确要求 **1536 × 1872**，使用 v1 文件。
- 保留原始 PNG 文件和透明背景，直接上传；不要截图、裁剪、缩放或转成 JPEG。

### 网页版入口

根据 [OpenAI 官方 Pets 文档](https://learn.chatgpt.com/docs/pets)，在提供该功能的网页账户中：

1. 进入 **Settings → Personalization → Pet → Select pet**。
2. 选择 **Upload pet**，上传 `fantasy-xiaojie-v1.png`。
3. 上传完成后选择该伙伴。

官方网页上传说明列出的格式为透明 PNG / WebP、**1536 × 1872**、不超过 **20 MiB**，因此本项目额外提供 v1 兼容文件。桌面深链接的格式参数可显式选择 v2。请以你当前上传界面的要求为准。

网页版伙伴显示在支持的 ChatGPT Work 聊天界面中，桌面悬浮窗口是另一种显示方式。

## 如何下载文件

### 从 Releases 下载

打开 [最新 Release](https://github.com/tblshigg/fantasy-xiaojie-pixel/releases/latest)，在 **Assets** 中点击对应文件名。完整 ZIP 适合保存全部内容，单个 PNG 适合只安装伙伴。

[直接下载 v1.0.0 完整包](https://github.com/tblshigg/fantasy-xiaojie-pixel/releases/download/v1.0.0/fantasy-xiaojie-pixel-v1.0.0.zip)

### 从仓库下载

在仓库首页选择 **Code → Download ZIP**，下载并解压。该方式获取的是当前默认分支内容，可能比正式 Release 更新。

只下载单个 PNG 时，打开文件页面并使用 **Download raw file**；如果保存结果是 HTML 网页，请重新使用下载按钮。

### 使用 Git 下载

~~~bash
git clone https://github.com/tblshigg/fantasy-xiaojie-pixel.git
cd fantasy-xiaojie-pixel
~~~

## 调整显示效果

桌面应用中可以在 **Settings → Pets → Customize** 调整 **Pet size**。本项目的默认站姿和比例按大头小身的像素伙伴设计；README 和 GIF 为便于观察做了放大。

- 显示伙伴：`/pet` 或命令菜单 **Show pet**。
- 隐藏伙伴：命令菜单 **Hide pet**，或伙伴右键菜单中的 **Hide**。
- 系统开启“减少动态效果”时，应用可能显示静态帧，而不是播放动作。
- 网页版和桌面版的显示位置与控制方式可能不同。

上述入口依据 [官方 Pets 使用说明](https://learn.chatgpt.com/docs/pets)。

## 常见问题

### 我没有看到 Pets 菜单

先确认使用的是提供伙伴功能的应用界面和账户。该功能可能受版本、工作区策略或功能开放情况影响。Codex IDE 扩展不提供桌面伙伴选择器和悬浮窗口；可以使用支持的桌面应用。

### 上传提示尺寸不正确

核对上传入口要求，优先检查是否把 v2 文件上传到了只接受 v1 的入口。原始文件尺寸分别为 **1536 × 2288** 和 **1536 × 1872**。

### 我下载到的是 GIF、视频或网页

安装需要 `assets/` 下的完整透明 PNG 精灵图。GIF、MP4 和效果截图用于预览。

### 背景出现黄色

`sources/` 是制作源图，部分带黄色抠图背景。请安装 `assets/fantasy-xiaojie-v2.png` 或 v1 兼容文件。

### 添加后没有自动切换

打开实际使用账户的伙伴设置，选择“范特西小杰”，再显示伙伴。收藏、选择和显示是不同步骤。

### 会改变模型、回答风格或账户功能吗

本项目提供外观与动画素材。实际对话、语音和任务功能由宿主应用及你的账户提供。

### 想报告问题

到 [Issues](https://github.com/tblshigg/fantasy-xiaojie-pixel/issues) 说明应用版本、使用的 v1 / v2 文件、系统和出现问题的动作。截图前请检查其中是否包含个人信息。

