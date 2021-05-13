import json
import os
import sys
import hashlib
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

def gen_file_MD5(dir_path=""):
    """
    生成路径下所有文件的md5值并且按照格式写入文件
    [[filename, md5, relative_filePath],...]
    文件名, md5值, 文件相对路径
    :param dir_path:
    :return:
    """
    dir_path = "D:\MyWorkSpace\PythonProcess\djjk\dist\processFiles_release"
    files_filter = ['.git', 'docs']
    file_md5_dict = {}
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dir_path)):
        if i == 0:
            for i in files_filter:
                if i in dirnames:
                    dirnames.remove(i)
        for filename in filenames:
            full_filepath = os.path.join(dirpath, filename)
            relative_dirpath = dirpath.replace(dir_path, "")[1:]
            relative_filepath = os.path.join(relative_dirpath, filename)
            with open(full_filepath, 'rb') as f:
                file_md5 = hashlib.md5(f.read()).hexdigest()
            file_md5_dict[relative_filepath] = file_md5
    os.makedirs(os.path.join(dir_path, "docs"), exist_ok=True)
    with open(os.path.join(dir_path, "docs", "file_md5.json"), 'w', encoding="utf-8") as f:
        json.dump(file_md5_dict, f)

def cal_md5(path):
    with open(path, 'rb') as f:
        file_md5 = hashlib.md5(f.read()).hexdigest()
    print(file_md5)

def check_file_change(dir_path=""):
    """
    检查文件夹下所有文件是否修改
    :return:
    """

    dir_path = "D:\MyWorkSpace\PythonProcess\djjk\dist\processFiles_release"
    files_filter = ['.git', 'docs']
    all_filenames = []
    with open(os.path.join(dir_path, "docs", "file_md5.json"), 'r', encoding="utf-8") as f:
        file_md5_dic = json.load(f)
    print(file_md5_dic)
    for i, (dirpath, dirnames, filenames) in enumerate(os.walk(dir_path)):
        if i == 0:
            for i in files_filter:
                if i in dirnames:
                    dirnames.remove(i)
        for filename in filenames:
            all_filenames.append(filename)
            full_filepath = os.path.join(dirpath, filename)
            relative_dirpath = dirpath.replace(dir_path, "")[1:]
            relative_filepath = os.path.join(relative_dirpath, filename)
            with open(full_filepath, 'rb') as f:
                file_md5 = hashlib.md5(f.read()).hexdigest()
            remote_md5 = file_md5_dic.get(relative_filepath, 0)
            if remote_md5 != file_md5:
                print("文件:%s的md5不一致"%relative_filepath)

            file_md5_dic[relative_filepath] = file_md5
    with open(os.path.join(dir_path, "docs", "file_md5.json"), 'w', encoding="utf-8") as f:
        json.dump(file_md5_dic, f)


def download_update_file():
    """
    下载需要更新的文件， 确保远程文件列表中每个文件都下载到本地
    :return:
    """
    locla_dir_path = "D:\MyWorkSpace\PythonProcess\djjk\dist\processFiles"
    remote_url = "https://github.com/lihuasheng1234/djjk/raw/my-test/"
    import requests
    resp = requests.get("https://raw.githubusercontent.com/lihuasheng1234/djjk_release/master/docs/file_md5.json")
    file_md5_dict = json.loads(resp.text)
    file_md5_list = file_md5_dict.keys()
    for item_list in file_md5_list:
        # 对比远程和本地文件 md5值
        remote_file_md5 = file_md5_dict[item_list]
        file_relativePath = item_list
        full_filepath = os.path.join(locla_dir_path, file_relativePath)
        if os.path.exists(full_filepath):
            with open(full_filepath, 'rb') as f:
                file_md5 = hashlib.md5(f.read()).hexdigest()
            if file_md5 == remote_file_md5:
                continue
        print("文件%s有误，重新下载"%full_filepath, file_relativePath)
        url_file_relativePath = file_relativePath.replace('\\', '/')
        url = "https://raw.githubusercontent.com/lihuasheng1234/djjk_release/master/" + url_file_relativePath
        resp1 = requests.get(url)
        with open(os.path.join(locla_dir_path, file_relativePath), 'wb') as f:
            f.write(resp1.content)


def get_remote_md5_dict():
    import requests
    resp = requests.get("https://raw.githubusercontent.com/lihuasheng1234/djjk/my-test/docs/file_md5.json")
    print(resp.text)

if __name__ == '__main__':
    gen_file_MD5()
    check_file_change()
    # download_update_file()
    #get_remote_md5_dict()
    cal_md5(r"D:\MyWorkSpace\PythonProcess\djjk\dist\processFiles_release\update.exe")
    cal_md5(r"D:\MyWorkSpace\PythonProcess\djjk\dist\update.exe")