
# GPT-SoVITS运行的URL
url = 'http://127.0.0.1:9880'

# 默认的GPT模型路径 上GPT-SoVITS配置文件里找
default_gpt_weights = 'GPT_SoVITS/pretrained_models/s1v3.ckpt'
# 默认的SoVITS模型路径 上GPT-SoVITS配置文件里找
default_sovits_weights = 'GPT_SoVITS/pretrained_models/v2Pro/s2Gv2ProPlus.pth'

# 每个角色完整的配置数据
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

# 清洗文本用，怕tts不识别
def cleanText(text: str) -> str:
    text = text.replace('——', '，')   # 中文双破折号 → 逗号
    text = text.replace('—', '，')    # 英文破折号 → 逗号
    text = text.replace('--', '，')   # 双连字符 → 逗号
    text = text.replace('…', '。')
    return text

# 是否启用清洗
isCleanText = True

# rpy文件白名单 (不进行处理的)
rpy_white_list = [
    'gui.rpy', 'options.rpy', 'screens.rpy',
]