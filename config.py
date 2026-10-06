
# GPT-SoVITS运行的URL
url = 'http://127.0.0.1:9880'

# 默认的GPT模型路径 上GPT-SoVITS配置文件里找
default_gpt_weights = 'GPT_SoVITS/pretrained_models/s1v3.ckpt'
# 默认的SoVITS模型路径 上GPT-SoVITS配置文件里找
default_sovits_weights = 'GPT_SoVITS/pretrained_models/v2Pro/s2Gv2ProPlus.pth'

# 每个角色完整的配置数据
roles = {
    "k": {    # 角色变量名
        'lang': 'zh',   # 语言
        'ref_audio_path': r"E:\vo_friendship\vo_kazuha\vo_kazuha_Dialog_close1_01_processed.wav",    # 参考音频路径(abs)
        'ref_audio_text': '有什么想说的，不必藏在心里。我能够听到自然万物的声音，其中，也包括你的声音。',     # 参考音频内容
        'aux_ref_audio_list':[      # 辅助参考音频路径列表(abs)
            r"C:\Users\Admin\Desktop\CallBuddy-chat\friends\kazuha-1.0\aux_ref_audios\ref_audio1.wav",
            r"C:\Users\Admin\Desktop\CallBuddy-chat\friends\kazuha-1.0\aux_ref_audios\ref_audio2.wav",
            r"C:\Users\Admin\Desktop\CallBuddy-chat\friends\kazuha-1.0\aux_ref_audios\ref_audio3.wav"
        ],
        'seed': -1,      # Seed (-1为随机)
        'model':{
            'gpt':{     
                'enabled':False,    # 是否使用你训练的GPT模型
                'path':''           # GPT模型路径 (abs)
            },
            'sovits':{
                'enabled':False,    # 是否使用你训练的SoVITS模型
                'path':''           # SoVITS模型路径 (abs)
            }
        }
    },
    "wanderer": {    
        'lang': 'zh',  
        'ref_audio_path': r"E:\wanderer\vo_friendship\vo_wanderer\vo_wanderer_Dialog_annoyed.wav",    
        'ref_audio_text': '在想怎么才能把你甩掉，去胡作非为一番。开玩笑的，你信了？',
        'aux_ref_audio_list':[
            r"E:\wanderer\vo_friendship\vo_wanderer\vo_wanderer_pref_hobby.wav",
            r"E:\wanderer\vo_friendship\vo_wanderer\vo_wanderer_spice_dislike_01.wav",
            r"E:\wanderer\vo_friendship\vo_wanderer\vo_wanderer_teammate_dottore_01.wav"
        ],
        'seed': -1,      
        'model':{
            'gpt':{     
                'enabled':False,    
                'path':''           
            },
            'sovits':{
                'enabled':False,    
                'path':''           
            }
        }
    },
    "heizou": {    
        'lang': 'zh',  
        'ref_audio_path': r"E:\heizou\vo_friendship\vo_heizou\vo_heizou_Dialog_idle.wav",    
        'ref_audio_text': '侦探，就该用脑力摧毁那些犯人企图逃脱的侥幸，所以说，真正的侦探，根本犯不着使用武力嘛。',
        'aux_ref_audio_list':[
            r"E:\heizou\vo_friendship\vo_heizou\vo_heizou_weather_snowy_01.wav",
            r"E:\heizou\vo_friendship\vo_heizou\vo_heizou_character_idle_01.wav",
            r"E:\heizou\vo_friendship\vo_heizou\vo_heizou_character_idle_03.wav"
        ],
        'seed': -1,      
        'model':{
            'gpt':{     
                'enabled':False,    
                'path':''           
            },
            'sovits':{
                'enabled':False,    
                'path':''           
            }
        }
    },
    "venti": {    
        'lang': 'zh',  
        'ref_audio_path': r"E:\venti\vo_friendship\vo_venti\vo_venti_Dialog_pendant.wav",    
        'ref_audio_text': '欸？好奇我的神之眼？喔，诺，给你。喜欢的话，要我给你做一个一样的么？嘿嘿嘿。',
        'aux_ref_audio_list':[
            r"E:\venti\vo_friendship\vo_venti\vo_venti_explore_idle_02.wav",
            r"E:\venti\vo_friendship\vo_venti\vo_venti_Dialog_idle.wav",
            r"E:\venti\vo_friendship\vo_venti\vo_venti_pref_hobby.wav"
        ],
        'seed': -1,      
        'model':{
            'gpt':{     
                'enabled':False,    
                'path':''           
            },
            'sovits':{
                'enabled':False,    
                'path':''           
            }
        }
    },
    "xiao": {    
        'lang': 'zh',  
        'ref_audio_path': r"E:\xiao\vo_friendship\vo_xiao\vo_xiao_Dialog_annoyed.wav",    
        'ref_audio_text': '烦恼？呵，这个问题对仙人毫无意义，没有什么烦恼能够存在千年。',
        'aux_ref_audio_list':[
            r"E:\xiao\vo_friendship\vo_xiao\vo_xiao_Dialog_idle_02.wav",
            r"E:\xiao\vo_friendship\vo_xiao\vo_xiao_Dialog_share.wav",
            r"E:\xiao\vo_friendship\vo_xiao\vo_xiao_Dialog_greetingnight.wav"
        ],
        'seed': -1,      
        'model':{
            'gpt':{     
                'enabled':False,    
                'path':''           
            },
            'sovits':{
                'enabled':False,    
                'path':''           
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
    'data.rpy', 'gui.rpy',
    'options.rpy', 'screens.rpy',
    's.rpy_voiced.rpy'
]