[English](#renvoice-en) | [中文](#renvoice-zh)

# RenVoice-en
> A batch AI voice generation tool for Ren'Py visual novels based on GPT-SoVITS.

## Quick Start

1. Install dependencies: `pip install requests`
2. Start the GPT-SoVITS API service
3. Modify the reference audio path and text in `config.py`
4. Run `python RenVoice.py`, select the `game` folder
5. Test in game

## How It Works?
1. First, it asks you to select the game folder (filedialog)
2. Wait for GPT-SoVITS to start
3. Read all .rpy files in the folder (including subfolders), create a `baks` folder at the same level as the `game` directory, and back up the .rpy files involved
4. Then call TTS, generate audio under `game/audio/voice/<character variable name>/`
5. After all TTS calls are done, generate `VoiceMap.json` in the folder, a large mapping table. See the `VoiceMap mapping table` section below for details
6. Finally, read `VoiceMap.json`, create `<filename>.tmp` and write the processed rpy script, and after writing, **replace your original script**!

## config.py
This is the core configuration of the entire program. Each configuration item is explained below.

The `roles` configuration item has special instructions below.

| Name | Type | Description | Default |
| :--- | :--- | :--- | :--- |
| url | str | URL where GPT-SoVITS runs | http://127.0.0.1:9880 |
| default_gpt_weights | str | Default GPT model path, find it in the GPT-SoVITS config file | GPT_SoVITS/pretrained_models/s1v3.ckpt |
| default_sovits_weights | str | Default SoVITS model path, find it in the GPT-SoVITS config file | GPT_SoVITS/pretrained_models/v2Pro/s2Gv2ProPlus.pth |
| roles | dict | Character TTS configuration | {} |
| cleanText | function | Text cleaning function | See `config.py` |
| isCleanText | bool | Whether to clean the text sent to TTS | True |
| rpy_white_list | list | .rpy filenames not to process | `['gui.rpy','options.rpy', 'screens.rpy']` |

### roles
roles is a large dict. It looks roughly like this. See the comments below for the meaning of each part.
```python
roles = {
    "kazuha": {    # Character variable name
        'lang': 'zh',   # Language
        'ref_audio_path': r"C:\Your\ref\audio\path\xxx.wav",    # Reference audio path (abs)
        'ref_audio_text': 'xxxxxxxxxxxx',     # Reference audio content (must match the reference audio exactly)
        'aux_ref_audio_list':[      # Auxiliary reference audio path list (abs) (optional)
            r"C:\xxx\x1.wav",
            r"C:\xxx\x2.wav",
            r"C:\xxx\x3.wav",
        ],
        'seed': -1,      # Seed (-1 for random)
        'model':{
            'gpt':{     
                'enabled':False,    # Whether to use your trained GPT model
                'path':''           # GPT model path (abs) (optional)
            },
            'sovits':{
                'enabled':False,    # Whether to use your trained SoVITS model
                'path':''           # SoVITS model path (abs) (optional)
            }
        }
    }
}
```

## VoiceMap.json
This is the audio mapping table. It looks roughly like this. Please note, **pseudocode, using Python for illustration for easier commenting**
```python 
voicemap = {
    "$var_map": {       # Automatically generated
        "你好啊，[player_name]。|kazuha": "旅行者"      # Original text + | + <character variable name> -> content to read the variable as
    },
    "$failed": [        # Texts that failed TTS processing     Automatically generated
        "……|kazuha",    # Text + | + <character variable name>     
        "……|wanderer",
        "……|wanderer"
    ],
    "kazuha": {         # Your character variable name
        "last_index": 2,    # The name index of the next audio file
        "data": {       # Data section
            "你好。": "voice/kazuha/0.wav",     # Cleaned text!!! -> audio path
            "风带来了你的声音。": "voice/kazuha/1.wav"
        },
        "manual": {     # Your custom section, highest priority, used for specifying audio
            "呵呵": "voice/kazuha/myAudio.wav"
        }
    }
}
```
### Important Notes
1. Do not write audio tags in your original .rpy files! The tool will discard all `voice` statements during processing! If you need to keep them, write them in the `manual` section of the corresponding character variable name.
2. TTS processing failures are usually caused by things like ellipses that have no actual characters.

## Notes
(Example shown in Chinese, as the tool was originally built for Chinese scripts.)
This tool supports single-line dialogue and does not support multi-line strings (triple quotes).
This is a known limitation and may be improved in future versions. Like this:
```renpy
k """
你好
你好 
"""
```
If you encounter something like this:
```renpy
k "[player_name]，跟我一起出发吧。"
```
where the statement contains variables, it will interactively ask you what you want it to read as, and after input, it will be saved to VoiceMap.

It currently only supports interactive CLI, not GUI or command invocation.

## Disclaimer

This is a personal hobby project, made mainly for fun and experimentation. It is not a professional product, and I cannot guarantee it will work perfectly in every environment.

The tool is provided "as is", without any warranty. Use it at your own risk. I am not responsible for any data loss, damage, or other issues caused by using this tool.

This project uses GPT-SoVITS for AI voice generation. Please make sure you have the legal right to use any reference audio, and comply with the relevant licenses and terms of service. Prohibited for illegal use.

If you are using this tool for fan works, please respect the original copyright holders. This project is not official and is not affiliated with any game company or voice actor.

Feedback and bug reports are welcome, but please understand that this is just a side project and updates may be slow.

Thanks.

## About
- Author: Xiaoshi
- Repository: [RenVoice](https://github.com/XiaoShi-studio/RenVoice)
- License: MIT License (see LICENSE file for details)
- Ver: 1.2

---

# RenVoice-zh
> 基于GPT-SoVITS的Ren'Py视觉小说批量AI语音生成工具。

## 快速开始

1. 安装依赖：`pip install requests`
2. 启动 GPT-SoVITS API 服务
3. 修改 `config.py` 里的参考音频路径和文本
4. 运行 `python RenVoice.py`，选择 `game` 文件夹
5. 进游戏测试

## 怎么运作？
1. 先让你选择game文件夹(filedialog)
2. 启动GPT-SoVITS
3. 读取文件夹下的所有.rpy文件(含子文件夹), 在与`game`目录同级创建`baks`文件夹，把涉及处理的.rpy文件进行备份
4. 然后调用TTS, 在`game/audio/voice/<角色变量名>/`下生成音频
5. 全部TTS调用完之后, 在文件夹下生成`VoiceMap.json`, 一张大映射表，详细信息见下面`VoiceMap映射表`部分
6. 最终读取`VoiceMap.json`，创建`<文件名>.tmp`并写入处理后的rpy脚本，并且写入后将**替换掉你的原脚本**!

## config.py
这是整个程序的核心配置处，下面将为你讲解每个配置项

配置项`roles`在下方有特殊说明，请见下方。

| 名称 | 类型 | 说明 | 默认 |
| :--- | :--- | :--- | :--- |
| url | str | GPT-SoVITS运行的URL | http://127.0.0.1:9880 |
| default_gpt_weights | str | 默认的GPT模型路径 上GPT-SoVITS配置文件里找 | GPT_SoVITS/pretrained_models/s1v3.ckpt |
| default_sovits_weights | str | 默认的SoVITS模型路径 上GPT-SoVITS配置文件里找 | GPT_SoVITS/pretrained_models/v2Pro/s2Gv2ProPlus.pth |
| roles | dict | 角色TTS配置 | {} |
| cleanText | function | 清洗文本函数 | 见`config.py` |
| isCleanText | bool | 是否对发向TTS的文本进行清洗 | True |
| rpy_white_list | list | 不进行处理的rpy文件名 | `['gui.rpy','options.rpy', 'screens.rpy']` |

### roles
roles是一个大dict，它大概就长这样，各部分含义见下方注释
```python
roles = {
    "kazuha": {    # 角色变量名
        'lang': 'zh',   # 语言
        'ref_audio_path': r"C:\Your\ref\audio\path\xxx.wav",    # 参考音频路径(abs)
        'ref_audio_text': 'xxxxxxxxxxxx',     # 参考音频内容 (必须与参考音频一字不差)
        'aux_ref_audio_list':[      # 辅助参考音频路径列表(abs) (非必须)
            r"C:\xxx\x1.wav",
            r"C:\xxx\x2.wav",
            r"C:\xxx\x3.wav",
        ],
        'seed': -1,      # Seed (-1为随机)
        'model':{
            'gpt':{     
                'enabled':False,    # 是否使用你训练的GPT模型
                'path':''           # GPT模型路径 (abs) (非必须)
            },
            'sovits':{
                'enabled':False,    # 是否使用你训练的SoVITS模型
                'path':''           # SoVITS模型路径 (abs) (非必须)
            }
        }
    }
}
```

## VoiceMap.json
这是音频映射表，大概就长这样，请看，**伪代码，为便于注释，这里使用Python展示**
```python 
voicemap = {
    "$var_map": {       # 自动生成
        "你好啊，[player_name]。|kazuha": "旅行者"      # 原始文本+|+<角色变量名> -> 变量要读成的内容
    },
    "$failed": [        # TTS处理失败的文本     自动生成
        "……|kazuha",    # 文本+|+<角色变量名>     
        "……|wanderer",
        "……|wanderer"
    ],
    "kazuha": {         # 你的角色变量名
        "last_index": 2,    # 下一个音频的名字序号
        "data": {       # 数据区
            "你好。": "voice/kazuha/0.wav",     # 清洗后的文本!!! -> 音频路径
            "风带来了你的声音。": "voice/kazuha/1.wav"
        },
        "manual": {     # 你的自定义区，优先级最高，适用于指定音频的情况
            "呵呵": "voice/kazuha/myAudio.wav"
        }
    }
}
```
### 着重说明
1. 不要在你的原.rpy文件中写入音频标记！工具在处理时会丢弃所有`voice`语句！需要保留的请写在对应角色变量名的`manual`里。
2. TTS处理失败的通常都由于是省略号之类的没字的东西

## 你需要注意的点
本工具支持单行台词，不支持跨行字符串（三引号）。
这是已知限制，后续版本可能改进。像这样
```renpy
k """
你好
你好 
"""
```
如果遇到像这种：
```renpy
k "[player_name]，跟我一起出发吧。"
```
语句中含有变量的，会交互式询问你想把它读成什么，输入后会保存至VoiceMap中。

它当前仅支持交互式CLI，不支持GUI与命令调用。

## 免责声明

这是一个个人业余作品，主要供自己学习和娱乐使用，不是专业产品，不保证在所有环境下都能正常运行。

本工具按“现状”提供，不提供任何担保。使用本工具产生的任何风险由使用者自行承担，作者不对任何数据丢失、损坏或其他问题负责。

本项目使用 GPT-SoVITS 进行 AI 语音生成，请确保你对参考音频拥有合法使用权，并遵守相关许可协议和服务条款。禁止用于非法用途。

如果是用于同人创作，请尊重原版权方。本项目非官方项目，与任何游戏公司或声优无关。

欢迎反馈问题，但请理解这只是个人业余项目，更新可能较慢。

感谢您的使用！

## 关于
- 作者: 小石
- 仓库: [RenVoice](https://github.com/XiaoShi-studio/RenVoice)
- 许可证: MIT LICENSE (详见LICENSE文件)
- 版本: 1.2