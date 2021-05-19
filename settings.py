import os
import json

import pymysql

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

if not os.path.exists(os.path.join(BASE_PATH, "config.json")):
    with open(os.path.join(BASE_PATH, "config.json"), 'w') as f:
        data = '''{
    "company_no": "CMP20210119001",
    "device_no": "0001",
    "damage":{
    "signalr_url": "http://202.104.118.59:8070/signalr/",
    "signalr_hubname": "dashBoardHub",
    "load_send_funcname": "broadcastDJJK_FZ",
    "raw_send_funcname": "broadcastDJJK_Working",
    "rws_send_funcname": "broadcastDJJK_Health",
    "alarm_send_funcname": "BroadcastDJJK_Alarm",
    "data_post_params": "http://202.104.118.59:8054/api/TblDeviceFanuc/InsertToolDetect",
    "T00":"AAAA,0.2,0.6",
    "T01":"AAAA,0.2,0.6",
    "T02":"AAAA,0.2,0.6",
    "T03":"AAAA,0.2,0.6",
    "T04":"AAAA,0.2,0.6",
    "T05":"AAAA,0.2,0.6",
    "T06":"AAAA,0.2,0.6",
    "T07":"AAAA,0.2,0.6",
    "T08":"AAAA,0.2,0.6",
    "T10":"AAAA,0.2,0.6",
    "T11":"AAAA,0.2,0.6",
    "T12":"AAAA,0.2,0.6",
    "T13":"AAAA,0.2,0.6",
    "T14":"AAAA,0.2,0.6",
    "T15":"AAAA,0.2,0.6",
    "T16":"AAAA,0.2,0.6",
    "T17":"AAAA,0.2,0.6",
    "T18":"AAAA,0.2,0.6",   
    "T19":"AAAA,0.2,0.6",
    "T20":"AAAA,0.2,0.6"
    }
    }'''
        json.dump(json.loads(data), f)
SETTINGS_PATH = os.path.join(BASE_PATH, "config.json")


with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
    #print(list(f.readlines()))
    json_data = json.load(f)
TOTAL_SETTINGS = json_data

# 时间字符串格式
DATETIME_PATTERN = "%Y-%m-%d %H:%M:%S"
# 训练数据保存格式
SAVEDDATA_FILENAME_FORMAT = "%Y-%m-%d-%H-%M-%S-%f"

# 负载报警阈值
MAX_LOAD_WARMING = 100

#是否为本地模式
IS_LOCAL = False

# 保存数据开关
LEARNNING_MODEL = False

# 计算健康度时间间隔 毫秒
TOOLHEALTH_COMPUTE_BLANKING_TIME = 60*1000

# 负载上传时间 毫秒
LOADDATA_UPLOAD_BLANKING_TIME = 1*1000

# 原始振动数据上传时间 毫秒
RAWVIBDATA_UPLOAD_BLANKING_TIME = 1*1000

# 数据库中振动数据每条数据间隔 毫秒
VIBDATA_DB_TIME = 100

# 每隔多少时间间隔获取一次机台信息 毫秒
LOADDATA_DB_GET_BLANKING_TIME = 100

# 从数据库获取振动数据间隔 毫秒
VIBDATA_DB_GET_BLANKING_TIME = 1000

# 每个间隔内从数据库中获取的数据条数
VIBDATA_COUNT = VIBDATA_DB_GET_BLANKING_TIME//VIBDATA_DB_TIME

# 从数据库获取振动数据间隔 毫秒
LEARNNING_MODEL_BLANKING_TIME = 2*1000

#mangodb settings
vibdata_mangodb_info = {
    "host" : "mongodb://localhost:27017/",
    "db_name" : "VibrationData",
    "tb_name" : "Sensor",
    "connect_timeoutMS" : "10000",
}

machineInfo_mangodb_info = {
    "host" : "mongodb://localhost:27017/",
    "db_name" : "MachineData",
    "tb_name" : "machineData",
    "connect_timeoutMS" : "10000",
}

mysql_info = {
    "host" : "localhost",  # mysql服务端ip
    "port" : 3306,  # mysql端口
    "user" : "root",  # mysql 账号
    "password" : "rootroot",
    "db" : "djjk",
    "charset" : "utf8",
    "cursorclass" : pymysql.cursors.DictCursor
}

#websocket 发送配置
signalr_hub_info = {
    "url": TOTAL_SETTINGS["damage"]["signalr_url"] if not IS_LOCAL else "http://localhost:8070/signalr/",
    "name": TOTAL_SETTINGS["damage"]["signalr_hubname"],
}

# 读取用户设定文件配置

SHEET_PATH = os.path.join(BASE_PATH, "sheets.csv")


# 刀具健康度缓存数据接口
TOOL_HP_CACHE_POST_URL = TOTAL_SETTINGS["damage"]["data_post_params"] if not IS_LOCAL else "http://localhost:8054/api/TblDeviceFanuc/InsertToolDetect"
TOOL_HP_CACHE_POST_PARRM = {
        "company_no": "CMP20210119001",
        "device_no": "0001",
        "tool_position": "",
        "collect_data": "",
        "collect_date": "2021-02-24 14:13:00"
    }

MACHINE1_IP = "192.168.1.1"

# 报警接口dll文件路径
DLL_PATH = BASE_PATH
DLL_NAME = os.path.join(DLL_PATH, "API.dll")

# 日志配置参数
kwargs = {
    "filename": "logs.txt",
    "format": "%(asctime)s - %(message)s",
    "mode": "a",
}

company_no = TOTAL_SETTINGS["company_no"]
device_no = TOTAL_SETTINGS["device_no"]

WORKING_HUB_NAME = TOTAL_SETTINGS["damage"]["raw_send_funcname"]
FZ_HUB_NAME = TOTAL_SETTINGS["damage"]["load_send_funcname"]
HEALTH_HUB_NAME = TOTAL_SETTINGS["damage"]["rws_send_funcname"]
ALARM_HUB_NAME = TOTAL_SETTINGS["damage"]["alarm_send_funcname"]
