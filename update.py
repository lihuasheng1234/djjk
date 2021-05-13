import hashlib
import json
import os
import sys
import time

import psutil
import requests

def exit_main():
    print("结束主进程")
    for proc in psutil.process_iter():
        if proc.name() == 'processFiles_0223.exe':
            proc.kill()

BASE_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))
locla_dir_path = BASE_PATH
resp = requests.get("https://raw.githubusercontent.com/lihuasheng1234/djjk_release/master/docs/file_md5.json")
file_md5_dict = json.loads(resp.text)
file_md5_list = file_md5_dict.keys()
is_update = False
for item_list in file_md5_list:
    # 对比远程和本地文件 md5值
    print("进行文件(%s)对比"%item_list)
    remote_file_md5 = file_md5_dict[item_list]
    file_relativePath = item_list
    full_filepath = os.path.join(locla_dir_path, file_relativePath)
    if os.path.exists(full_filepath):
        with open(full_filepath, 'rb') as f:
            file_md5 = hashlib.md5(f.read()).hexdigest()
        if file_md5 == remote_file_md5:
            continue
    print("文件%s有误，重新下载"%full_filepath, file_relativePath)
    if not is_update:
        exit_main()
        is_update = True
    url_file_relativePath = file_relativePath.replace('\\', '/')
    url = "https://raw.githubusercontent.com/lihuasheng1234/djjk_release/master/" + url_file_relativePath
    resp1 = requests.get(url)
    file_full_path = os.path.join(locla_dir_path, file_relativePath)
    file_dir = os.path.dirname(file_full_path)
    os.makedirs(file_dir, exist_ok=True)
    with open(file_full_path, 'wb') as f:
        f.write(resp1.content)
if is_update:
    print("更新结束，5s后退出，请重新运行")
else:
    print("没有更新")
time.sleep(5)
