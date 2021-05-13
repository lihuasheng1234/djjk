import os

def get_files_on_dir(dir_path):
    dir_path = "D:\MyWorkSpace\PythonProcess\djjk"
    pathnames = []
    for (dirpath, dirnames, filenames) in os.walk(dir_path):
        for filename in filenames:
            pathnames += [os.path.join(dirpath, filename)]
    print(pathnames)
    print(len(pathnames))
if __name__ == '__main__':
    get_files_on_dir('/')