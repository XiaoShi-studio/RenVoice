import os
import shutil
import requests
from config import *
from tkinter.filedialog import askdirectory
from pathlib import Path
import json
import re
import time

def send_tts(s:str, char:str):
    data = roles[char]
    resp = requests.post(url+'/tts',json={
        "text": s,
        "text_lang": data['lang'],
        "ref_audio_path": data["ref_audio_path"],
        "aux_ref_audio_paths": data['aux_ref_audio_list'],
        "prompt_text": data['ref_audio_text'],
        "prompt_lang": data['lang'],
        "seed": data['seed']
    })
    if resp.status_code == 200:
        return True, resp.content
    else:
        return False, resp.content

def process_tts(folder: Path):
    say_re_dict = {}
    voice_re = re.compile(r'^\s*voice\s+["\'].*["\'].*$')
    for name in roles.keys():
        say_re_dict[name] = re.compile(
            r'^(?P<indent>\s*)'
            rf'(?P<who>{re.escape(name)})'
            r'(?:\s+(?P<middle>[^"\']+?))?'   # 可选：引号前的其他内容
            r'\s+'
            r'(?P<quote>"|\')'
            r'(?P<content>.*?)'
            r'(?P=quote)'
            r'(?:\s+(?P<extra>\S.*?))?'
            r'\s*$'
        )
        voice_folder_path = folder / f'audio/voice/{name}'
        os.makedirs(voice_folder_path, exist_ok=True)   #建文件夹
    while True:
        try:
            requests.get(url)
            break
        except requests.exceptions.ConnectionError: # 服务还未启动
            time.sleep(2)
            print("等待TTS服务启动...")
    t1 = time.perf_counter()
    # 如果存在映射
    map_path = folder / 'VoiceMap.json'
    if map_path.exists():
        try:
            full_voice_map = json.loads(map_path.read_text(encoding='utf-8'))
        except Exception:
            full_voice_map = {}
    else:
        full_voice_map = {}
    var_map = full_voice_map.setdefault('$var_map',{})
    failed = full_voice_map.setdefault('$failed', [])
    for name in roles.keys():
        if name not in full_voice_map:
            full_voice_map[name] = {'last_index': 0, 'data': {}}
        full_voice_map[name].setdefault('last_index', 0)
        full_voice_map[name].setdefault('data', {})
        full_voice_map[name].setdefault('manual', {})

    source_files = list(folder.rglob("*.rpy"))
    for name in roles.keys():
        name_script_suc = 0
        name_script_fail = 0
        name_script_skip = 0
        print(f'处理中: {name}')
        # 看看用没用模型
        model_config = roles[name]['model']
        if model_config['gpt'].get('enabled'):
            resp = requests.get(url+'/set_gpt_weights',params={'weights_path':model_config['gpt'].get('path')})
            if resp.status_code == 200:
                print('  GPT模型切换成功')
            else:
                print('  GPT模型切换失败',resp.content)
        else:
            print('  未使用GPT模型, 使用默认预训练模型')
            resp = requests.get(url+'/set_gpt_weights',params={'weights_path':default_gpt_weights})
            print(f'  切换成功状态: {resp.status_code == 200}')
        if model_config['sovits'].get('enabled'):
            resp = requests.get(url+'/set_sovits_weights',params={'weights_path':model_config['sovits'].get('path')})
            if resp.status_code == 200:
                print('  SoVITS模型切换成功')
            else:
                print('  SoVITS模型切换失败',resp.content)
        else:
            print('  未使用SoVITS模型, 使用默认预训练模型')
            resp = requests.get(url+'/set_sovits_weights',params={'weights_path':default_sovits_weights})
            print(f'  切换成功状态: {resp.status_code == 200}')
        for rpy in source_files:
            file_script_suc = 0
            file_script_fail = 0
            file_script_skip = 0
            if rpy.name in rpy_white_list:  #简易小过滤
                print(f"  跳过: {rpy.name}")
                continue

            print(f'  正在处理: {rpy.name}')
            
            with open(rpy, 'r', encoding='utf-8') as rpy_file:
                # 行读
                for line in rpy_file:
                    voice_match = voice_re.match(line)
                    if voice_match:
                        continue

                    say_match = say_re_dict[name].match(line)
                    if say_match:
                        
                        ori_content = say_match.group('content')
                        ori_content = re.sub(r'\{.*?\}', '', ori_content).strip()   # 把像{w}之类的文本标签去了
                        
                        if '[' in ori_content and ']' in ori_content:
                            key = ori_content+'|'+name
                            if key not in var_map:
                                print(f"    在\n{ori_content}\n中检测到变量，您希望把它读成什么？")
                                goal = input('    >>>')
                                var_map[ori_content+'|'+name] = goal
                                content = re.sub(r'\[.*?\]', goal, ori_content).strip()
                                if isCleanText:
                                    content = cleanText(content)
                            else:
                                content = re.sub(r'\[.*?\]', var_map[key], ori_content).strip()
                                print('使用预存的变量读音:', ori_content, var_map[key])
                        elif isCleanText:
                            content = cleanText(ori_content)        # 这行可选，按需选择
                        else:
                            content = ori_content       # 反正不管怎样最后用content发tts，写脚本展示ori_
                    
                        voice = full_voice_map[name]['manual'].get(content) or full_voice_map[name]['data'].get(content)
                        # 先查用户指定再查data
                        if voice == None or not (folder / "audio" / voice).exists():      # 缓存没存/文件不在了
                            if ori_content+'|'+name not in failed:
                                status, voice = send_tts(content, name)
                                if status:
                                    file_script_suc += 1
                                    name_script_suc += 1
                                    new_voice_name = f"voice/{name}/{full_voice_map[name]['last_index']}.wav"
                                    with open(folder / f"audio/{new_voice_name}",'wb') as f:
                                        f.write(voice)

                                    full_voice_map[name]['last_index'] += 1        # 序号自增
                                    full_voice_map[name]['data'][content] = new_voice_name # 映射，内容(清洗后) -> 音频
                                else:
                                    file_script_fail += 1
                                    name_script_fail += 1                         
                                    print("      ===未成功处理的内容===")
                                    print(f"        源: {ori_content}")
                                    if isCleanText:
                                        print(f"        处理后: {content}")
                                    try:
                                        errorData = json.loads(voice)
                                        print(f"        错误: {errorData['message']}")
                                        print(f"        异常: {errorData['Exception'].encode('utf-8').decode('unicode_escape').encode('latin1').decode('utf-8')}")
                      
                                    except:
                                        print(f'        错误: {voice}')
                                    failed.append(ori_content+'|'+name)
                            else:
                                print('      跳过一个TTS已经失败的内容')
                                name_script_skip += 1
                                file_script_skip += 1
                        else:
                            name_script_skip += 1
                            file_script_skip += 1
            print(f'      总计: {file_script_fail + file_script_suc + file_script_skip}, 成功: {file_script_suc}, 失败: {file_script_fail}, 跳过: {file_script_skip}')
        print(f'  总计: {name_script_fail + name_script_suc + name_script_skip}, 成功: {name_script_suc}, 失败: {name_script_fail}, 跳过: {name_script_skip}')
    full_voice_map['$var_map'] = var_map
    full_voice_map['$failed'] = failed
    with open((folder / 'VoiceMap.json'), 'w', encoding='utf-8') as f:
        json.dump(full_voice_map, f, indent=4, ensure_ascii=False)
    t2 = time.perf_counter()
    print("用时:",t2 - t1)   

def process_file(folder: Path):
    say_re_dict = {}
    voice_re = re.compile(r'^\s*voice\s+["\'].*["\'].*$')
    print('写入文件...')    
    for name in roles.keys():
        say_re_dict[name] = re.compile(
            r'^(?P<indent>\s*)'
            rf'(?P<who>{re.escape(name)})'
            r'(?:\s+(?P<middle>[^"\']+?))?'   # 可选：引号前的其他内容
            r'\s+'
            r'(?P<quote>"|\')'
            r'(?P<content>.*?)'
            r'(?P=quote)'
            r'(?:\s+(?P<extra>\S.*?))?'
            r'\s*$'
        )  

    map_path = folder / 'VoiceMap.json'
    if map_path.exists():
        full_voice_map = json.loads(map_path.read_text(encoding='utf-8'))
    source_files = list(folder.rglob("*.rpy"))
    var_map = full_voice_map.get('$var_map', {})
    failed = full_voice_map.get('$failed', [])
    for rpy in source_files:
        if rpy.name in rpy_white_list:  #简易小过滤
            print(f"  跳过: {rpy.name}")
            continue

        print(f'  正在处理: {rpy.name}')
        tmp = rpy.with_name(rpy.name + '.tmp')  # 临时文件
        #===挪一个备份1
        bak_dir = folder.parent / 'baks'
        rel = rpy.relative_to(folder)
        bak = bak_dir / rel
        bak.parent.mkdir(parents=True, exist_ok=True)
        if not bak.exists():
            shutil.copy2(rpy, bak)
        #===

        with open(tmp, 'w', encoding='utf-8') as voiced_rpy_file:
            with open(rpy, 'r', encoding='utf-8') as rpy_file:
                for line in rpy_file:
                    voice_match = voice_re.match(line)
                    if voice_match:
                        #print(f"{rpy.name}: 剥除一行已有 voice，如需指定请写 VoiceMap.json 的 manual")
                        continue

                    normal_line = True
                    for name in roles.keys():
                        say_match = say_re_dict[name].match(line)

                        if say_match:
                            indent = len(say_match.group('indent'))
                            ori_content = say_match.group('content')
                            ori_content = re.sub(r'\{.*?\}', '', ori_content).strip()   # 把像{w}之类的文本标签去了
                            if '[' in ori_content and ']' in ori_content:
                                
                                key = ori_content+'|'+name
                                if var_map.get(key) != None:
                                    content = re.sub(r'\[.*?\]', var_map[key], ori_content).strip()
                                else:
                                    print(f"    在\n{ori_content}\n中检测到变量，您希望把它读成什么？")
                                    goal = input('  >>>')
                                    content = re.sub(r'\[.*?\]', goal, ori_content).strip()
                                    var_map[key] = goal
                                if isCleanText:
                                    content = cleanText(content)
                            elif isCleanText:
                                content = cleanText(ori_content)        # 这行可选，按需选择
                            else:
                                content = ori_content       # 反正不管怎样最后用content发tts，写脚本展示ori_
                        
                            voice = full_voice_map[name]['manual'].get(content) or full_voice_map[name]['data'].get(content)
                            # 先查用户指定再查data
                            if voice and (folder / "audio" / voice).exists():      # 缓存存了
                                voiced_rpy_file.write(f"{' '*indent}voice \"audio/{voice}\"\n")
                                voiced_rpy_file.write(line)
                                normal_line = False
                                break
                            elif ori_content+"|"+name in failed:
                                print('    跳过一句TTS处理失败的文本：',ori_content+'|'+name)
                            else:
                                print('    未经处理的文本？',ori_content)
                    if normal_line:
                        voiced_rpy_file.write(line)
        try:
            tmp.replace(rpy)
        except Exception as e:
            print("替换原文件失败，",e)
    full_voice_map['$var_map'] = var_map
    with open((folder / 'VoiceMap.json'), 'w', encoding='utf-8') as f:
        json.dump(full_voice_map, f, indent=4, ensure_ascii=False)      # 如果var_map变了的话
if __name__ == '__main__':
    # 选择带.rpy的文件夹
    folder_path = askdirectory(title="选择game文件夹")
    folder = Path(folder_path)
    #var_map = {}
    process_tts(folder)
    process_file(folder)

# RenVoice
# Ver: 1.2
# 作者: 小石
# github: XiaoShi-studio

    