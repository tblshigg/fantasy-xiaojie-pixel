# 素材与二次制作说明

[返回项目首页](../README.md) · [使用与下载教程](INSTALL.md)

本仓库同时提供可以直接安装的成品和用于学习、修改的制作素材。图像由 AI 辅助生成，后续进行了透明背景处理、尺寸统一、排布、预览和视觉检查。提示词可以作为继续创作的起点；使用相同提示词不保证生成完全相同的图像。

## 目录

| 路径 | 内容 |
| --- | --- |
| `assets/` | 可安装的 v2 / v1 透明精灵图 |
| `previews/` | 各状态 GIF、完整 GIF、MP4、方向循环和静态效果 |
| `sources/base.png` | 主形象源图 |
| `sources/rows/` | 各动作和视线方向的生成源图 |
| `prompts/` | 主形象、动作和方向提示词 |
| `metadata/sprite.json` | 网格、帧数和方向等机器可读规格 |
| `metadata/validation.json` | 发布素材的验证摘要 |
| `tools/pet_assets.py` | 对现有精灵图进行格式检查、拆帧、预览和打包 |

制作源图可能包含黄色背景；安装文件位于 `assets/`。仓库未包含其他应用的内置伙伴图片，也不包含依赖某台电脑路径的制作环境。

## 精灵图规格

每一格固定为 **192 × 208 px**，每行从最左一格开始放置有效帧。未使用的格子保持完全透明。

| 行号（从 0 开始） | 状态 | 有效帧数 | 含义 |
| --- | --- | ---: | --- |
| 0 | `idle` | 6 | 安静呼吸、眨眼 |
| 1 | `running-right` | 8 | 朝画面右侧移动 |
| 2 | `running-left` | 8 | 朝画面左侧移动 |
| 3 | `waving` | 4 | 挥手打招呼 |
| 4 | `jumping` | 5 | 蓄力、起跳、腾空、落地 |
| 5 | `failed` | 8 | 失落后恢复 |
| 6 | `waiting` | 6 | 等待回应或输入 |
| 7 | `running` | 6 | 专注工作、思考 |
| 8 | `review` | 6 | 检查结果 |
| 9 | 前八个视线方向 | 8 | 000° 至 157.5° |
| 10 | 后八个视线方向 | 8 | 180° 至 337.5° |

`running` 这个状态名表示任务处理中，画面使用原地思考动作；真正的跑动由左右两个状态表示。

- **v2**：8 列 × 11 行，1536 × 2288 px，共 73 个有效帧。
- **v1**：v2 的前 9 行，8 列 × 9 行，1536 × 1872 px，共 57 个有效帧。
- 两种格式均保留 15 个未使用的透明格子。
- 视线方向使用画面坐标：**000° 是向上，090° 向右，180° 向下，270° 向左**。正面待机由第 0 行提供。

方向按顺时针排列：

~~~text
第 9 行：000, 022.5, 045, 067.5, 090, 112.5, 135, 157.5
第10行：180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5
~~~

## 环境准备

建议在虚拟环境中安装 Python 依赖。需要 Python 3.10 或更新版本。

Windows PowerShell：

~~~powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe tools/pet_assets.py validate
~~~

macOS / Linux：

~~~bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tools/pet_assets.py validate
~~~

基础图片处理使用 Pillow。需要重新编码 MP4 时，再安装视频所需的 `imageio-ffmpeg` 依赖，具体选项以工具的 `--help` 为准。查看仓库自带的 GIF / MP4 不需要安装这些依赖。

## 工具用法

以下命令从仓库根目录运行，默认读取 `assets/fantasy-xiaojie-v2.png`。

### 检查成品格式

~~~bash
python tools/pet_assets.py validate
~~~

格式检查用于发现尺寸、有效帧或透明格等结构问题。修改后的角色还需要人工检查身份一致性、动作含义、方向和实际播放效果。

发布版 v2 的 SHA-256：

~~~text
9cc563e1864af7d708d13ce493e1f75a6e27ba5e9020b896a3fa2457a5aa343d
~~~

### 拆出帧

~~~bash
python tools/pet_assets.py extract --output output/frames
~~~

在像素编辑器中检查原始 **192 × 208** 单元，避免把每一帧分别拉伸到满格。角色大小、脚底基线和相邻动作的过渡应保持一致。

### 重新输出预览

~~~bash
python tools/pet_assets.py previews --output output/previews
~~~

重点检查：

- 待机是否有自然的小幅变化。
- 左右移动的朝向和步伐是否正确。
- 挥手的手臂是否始终连在身体上。
- 跳跃是否真正离地，并回到同一落脚位置。
- 思考、等待和检查是否容易区分。
- 十六个方向是否按顺时针推进，两个行边界也能自然衔接。
- 是否存在黄色边缘、裁切、漂浮碎片、透明破洞或突然变大变小。

### 打包

~~~bash
python tools/pet_assets.py package --output dist/fantasy-xiaojie-pixel-v1.0.0.zip
~~~

发布前检查包内包含 README、许可、安装说明、可用精灵图和预览。不要把虚拟环境、临时文件、个人路径、账户信息或访问令牌放进仓库及 ZIP。

## 修改流程

1. 保存一份原始 `assets/` 文件。
2. 根据 `prompts/` 和 `sources/` 确定需要修改的外观或动作。
3. 修改源图或以主形象为参考重新生成受影响的动作组，保持同一组的大小和站姿一致。
4. 处理透明背景并按固定网格重新组装精灵图。
5. 运行格式检查，重新拆帧、输出预览并人工检查。
6. 在实际伙伴应用中安装测试，确认宿主接受该精灵图。
7. 更新元数据、变更记录和受影响的预览后，再发布版本。

本仓库的工具主要处理已经排好网格的精灵图，不会调用图像模型自动补齐角色或生成完整动画。AI 生成所需服务和人工视觉审核由创作者自行选择。

## 提交改进

欢迎通过 Issue 描述问题，或提交 Pull Request。涉及视觉修改时，附上修改前后的同一动作预览；涉及工具修改时，写明命令、输入文件规格和验证结果。

代码、文档和本项目可许可的原创素材采用 [MIT License](../LICENSE)，相关说明见 [NOTICE.md](../NOTICE.md)。

