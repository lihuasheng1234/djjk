import json
import os
import ctypes
import subprocess

import joblib
import requests
from bson import ObjectId
from gevent import monkey
import pandas as pd

monkey.patch_all()

import logging
from functools import wraps
import threading
import time
import datetime
import numpy as np
from math import *
import pymongo
import pymysql
from datetime import timedelta
import settings

"""

"""


class ProcessData(threading.Thread):
    def __init__(self):
        super().__init__()
        self.changeTool = False
        self.pre_total = None
        self.cal_data = []
        self.machineData_origin_cache = []
        self.cycle_changeTool_start_time_str = None
        self.cycle_changeTool_end_time_str = None
        self.vibration_originData_cache = []
        self.dic = {}

        self.exist_list = []
        self.processed_raw_vibData = []
        self.load_cache = []
        self.user_settings = {}
        self.set_feed = 0
        self.set_speed = 0
        self.tool_num = 0
        self.load = 0
        self.tool_hp = 0
        self.tool_hp_pre = 1
        self.companyNo = settings.company_no
        self.deviceNo = settings.device_no
        self.logger = logging.getLogger()
        self.val = 30
        self.vib_start_id = None
        self.machine_start_id = None
        self.vib_end_id = None

    def is_time_space(self, t_str1, t_str2, diff):
        """
        判断两个时间是否超过指定距离
        :param t1:
        :param t2:
        :param diff:
        :return:
        """
        pass

    @property
    def now(self):
        return datetime.datetime.now()

    def now_str(self,formats=settings.DATETIME_PATTERN):
        return self.now.strftime(formats)

    def clothes(blanking_time, flag=False):
        """
        限制函数的执行间隔
        参数 blanking_time: 间隔时间
            flag: 如果为True 将在指定时间后执行 否则立马执行
        """

        def decorate(func):

            @wraps(func)
            def ware(self, *args, **kwargs):
                # print(id(self))
                last_time = self.dic.get(func)
                if not last_time:
                    ret = None
                    if not flag:
                        ret = func(self, *args, **kwargs)
                    self.dic[func] = self.now
                    return ret
                elif (self.now - last_time) >= timedelta(milliseconds=blanking_time):
                    self.dic[func] = self.now
                    return func(self, *args, **kwargs)

            return ware

        return decorate

    def setup(self):
        print("正在准备中。。。")
        self.check_or_create_necessary_file()
        try:
            self.rf = joblib.load('rfr.pkl')
            self.get_mysql_connect()
            self.get_mangodb_connect()
            self.set_machineinfo_from_file()
            self.set_logger()
            self.vib_start_id = next(self.get_last_data_MongoDB(type=1))["_id"]
            self.machine_start_id = next(self.get_last_data_MongoDB(type=2))["_id"]
            self.ready = True
            self.last_transform_time =datetime.datetime.strptime(self.last_machineData["time"], "%Y-%m-%d-%H-%M-%S-%f")
        except Exception as e:
            print(e)
            self.ready = False

    def set_logger(self):
        print(self.logger.handlers)
        if not self.logger.handlers:
            fh = logging.FileHandler(filename=settings.kwargs['filename'], mode=settings.kwargs['mode'],
                                     encoding="utf-8")
            formatter = logging.Formatter(settings.kwargs['format'])
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)
            self.logger.setLevel(logging.WARNING)

    def get_mangodb_connect(self):
        """
        获取mongodb连接
        """
        self.vibdata_mangodb_connect = pymongo.MongoClient(settings.vibdata_mangodb_info['host'],
                                                           serverSelectionTimeoutMS=settings.vibdata_mangodb_info[
                                                               'connect_timeoutMS'])
        self.machineinfo_mangodb_connect = pymongo.MongoClient(settings.machineInfo_mangodb_info['host'],
                                                               serverSelectionTimeoutMS=settings.vibdata_mangodb_info[
                                                                   'connect_timeoutMS'])
        self.vibdata_mangodb_connect.list_database_names()
        self.machineinfo_mangodb_connect.list_database_names()

    def get_mysql_connect(self):
        """
        获取上传刀具健康度的mysql连接
        """
        self.mysql_connect = pymysql.connect(**settings.mysql_info)
        self.cursor = self.mysql_connect.cursor()

    @property
    def last_vibData(self):
        return next(self.get_last_data_MongoDB())

    @clothes(settings.VIBDATA_DB_GET_BLANKING_TIME)
    def prepare_vibrationData(self):
        """
        准备好需要的振动数据
        """

        origin_data = self.get_origin_vibrationData()
        #print("origin_data", origin_data)
        self.process_vibrationData(origin_data)


    def get_last_data_MongoDB(self, type=1):
        """
        获取MongoDB中最后一条数据
        :return:
        """
        if type == 1:
            # 获得振动数据最后一条
            databse = settings.vibdata_mangodb_info["db_name"]
            collection = settings.vibdata_mangodb_info["tb_name"]

        else:
            # 获得机台信息数据最后一条
            databse = settings.machineInfo_mangodb_info["db_name"]
            collection = settings.machineInfo_mangodb_info["tb_name"]
        col = self.vibdata_mangodb_connect[databse][collection].find({},sort=[('_id',pymongo.DESCENDING)],limit=1)
        return col


    def get_origin_vibrationData(self):
        """
        从数据库中获得原始数据
        """
        last_vibData = self.get_last_data_MongoDB()
        last_id = next(last_vibData)["_id"]
        start_id = self.vib_start_id
        origin_data = self.findArangeWithID(start_id, last_id)
        self.vib_start_id = last_id
        # 去除重复的第一条数据 第一条为上一次获取的最后一条数据
        next(origin_data)
        origin_data = list(origin_data)
        return origin_data if origin_data else [self.last_vibData]

    def findArangeWithID(self, start_id: str, end_id: str, type=1):
        """
        在mongodb中根据id查询范围内数据
        :param start_id:
        :param end_id:
        :return:
        """
        if type == 1:
            database = settings.vibdata_mangodb_info["db_name"]
            collection = settings.vibdata_mangodb_info["tb_name"]
        else:
            database = settings.machineInfo_mangodb_info["db_name"]
            collection = settings.machineInfo_mangodb_info["tb_name"]
        client = self.vibdata_mangodb_connect
        mydb = client[database][collection].find(
            {"_id": {"$gte": ObjectId(start_id), "$lte": ObjectId(end_id)}},
        )
        return mydb
    def process_vibrationData(self, db_data):
        """
        把数据库请求得到的数据处理成对应结果
        通过self.pre_data存放
        """
        data = []
        for item in db_data:
            data.extend(item['zdata'])
        
        if self.load <= 0.5:
            self.val = sum(data)/len(data)
            data = [x - self.val for x in data]
        self.pre_data = data

    @property
    def last_machineData(self):
        return next(self.get_last_data_MongoDB(type=2))

    @clothes(settings.LOADDATA_DB_GET_BLANKING_TIME)
    def prepare_machineInfo(self):
        origin_machineinfo = self.get_origin_machineinfo()

        self.set_machineinfo()
        if origin_machineinfo:
            self.analysisMachineData(origin_machineinfo)
        self.make_machineData_cache()

    def findArangeWithTime(self, start_time, end_time, type=1):
        client = self.machineinfo_mangodb_connect
        if type == 1:
            database = settings.vibdata_mangodb_info["db_name"]
            collection = settings.vibdata_mangodb_info["tb_name"]
        else:
            database = settings.machineInfo_mangodb_info["db_name"]
            collection = settings.machineInfo_mangodb_info["tb_name"]
        mydb = client[database][collection].find(
            {"time": {"$gte": start_time, "$lte": end_time}},
        )
        return mydb


    def get_tool_num(self, tool_num):
        if tool_num < 10:
            tool_num = "T0" + str(tool_num)
        else:
            tool_num = "T" + str(tool_num)
        return tool_num
    def analysisMachineData(self, machine_data):
        """
        根据获取到的机台信息分析当前运行状况
        :return:
        """
        for item in machine_data:
            print("tool:%s"%item['tool'])
            if not self.cycle_changeTool_start_time_str:
                self.cycle_changeTool_start_time_str = item["time"]
                self.cycle_changeTool_start_id = item["_id"]
            #print(item)
            # 判断换刀
            tool_list = item["tool"]
            self.tool_num_pre = self.tool_num
            self.tool_num = self.get_tool_num(tool_list[-1])
            print(self.tool_num_pre,self.tool_num)
            A = self.tool_num_pre != 0
            B = tool_list[0] != tool_list[-1] or self.tool_num_pre != self.tool_num
            if A and B:
                # 更换了刀具
                print("更换刀具")
                self.cycle_changeTool_start_time_str = self.cycle_changeTool_end_time_str
                self.cycle_changeTool_end_time_str = item["time"]
                self.changeTool = True
                print("%s->%s" % (self.cycle_changeTool_start_time_str, self.cycle_changeTool_end_time_str))



    def make_machineData_cache(self):
        self.load_cache.append(self.load)

    @clothes(settings.LOADDATA_UPLOAD_BLANKING_TIME, flag=True)
    def 发送负载数据到云端(self):
        device_num = int(self.deviceNo)
        self.更新数据(device_num, self.load_cache[:5], tb_name="load_data")
        if len(self.load_cache) >=10:
            self.load_cache = self.load_cache[-5:]

    def get_origin_machineinfo(self):
        """
        获取至上次获取的数据后开始到最新数据为止的数据
        :return:
        """
        last_id = self.last_machineData["_id"]
        start_id = self.machine_start_id
        origin_data = self.findArangeWithID(start_id, last_id, type=2)
        self.machine_start_id = last_id
        # 去除重复的第一条数据 第一条为上一次获取的最后一条数据
        next(origin_data)
        origin_data = list(origin_data)
        # print(origin_data[0]["_id"])
        # print(origin_data[-1]["_id"])
        return origin_data
    @property
    def machine_time_str(self):
        return self.last_machineData["time"]

    def set_machineinfo(self):
        """
        根据最新机台信息设定算法所需的机台状态信息
        :param origin_machineinfo:
        :return:
        """
        origin_machineinfo = self.last_machineData
        # self.set_feed = origin_machineinfo["setFeed"][0]
        # self.act_feed = origin_machineinfo["actFeed"][0]
        # self.set_speed = origin_machineinfo["setSpeed"][0]
        # self.act_speed = origin_machineinfo["actSpeed"][0]\

        self.load = origin_machineinfo["load"][0]
        if self.tool_num and self.tool_num not in self.user_settings.keys():
            self.user_settings[self.tool_num] = {
                "feed": float(5000),
                "speed": float(5000),
                "model": "AAAAA",
                "var1": float(0.2),
                "var2": float(0.6),
            }
            print("用户还未设定当前刀具信息")


    def read_user_settings(self):
        """
        通过本地表格文件读取用户设定,
        读取出来的数据均为字符串
        :return:
        """
        user_settings = {}
        # 迭代所有的行
        for key in settings.json_data["damage"]:
            if key.startswith("T"):
                temp = settings.json_data["damage"][key].split(',')
                tool_num = key
                s = 0
                f = 0
                model = temp[0]
                val1 = temp[1]
                val2 = temp[2]
                user_settings[tool_num] = {
                    "feed": float(f),
                    "speed": float(s),
                    "model": model,
                    "var1": float(val1),
                    "var2": float(val2),
                }
        return user_settings

    def set_machineinfo_from_file(self):
        """
        获取并设定用户提供的机台刀具信息
        """
        self.user_settings = self.read_user_settings()


    @clothes(settings.RAWVIBDATA_UPLOAD_BLANKING_TIME, flag=True)
    def 发送振动数据到云端(self):
        """
        降维原始振动数据
        发送降维后数据到云端
        清空本地缓存
        :return:
        """
        data = self.处理振动数据()
        device_num = int(self.deviceNo)
        self.更新数据(device_num, data, tb_name="vib_data")

    def 判断数据存在(self, machine_num):
        if machine_num in self.exist_list:
            return True
        with self.mysql_connect.cursor() as cursor:
            cursor.execute('''SELECT * from {0} WHERE machine_num={1};'''.format("vib_data", machine_num))
            self.mysql_connect.commit()
            ret1 = cursor.fetchone()

            cursor.execute('''SELECT * from {0} WHERE machine_num={1};'''.format("load_data", machine_num))
            self.mysql_connect.commit()
            ret2 = cursor.fetchone()
            if not ret1:
                cursor.execute('''INSERT INTO vib_data(data, time, machine_num) VALUES("{0}",NOW(),{1});'''.format("[0]", machine_num))
                self.mysql_connect.commit()
            if not ret2:
                cursor.execute('''INSERT INTO load_data(data, time, machine_num) VALUES("{0}",NOW(),{1});'''.format("[0]", machine_num))
                self.mysql_connect.commit()
            self.exist_list.append(machine_num)

    def 更新数据(self, machine_num, data, tb_name):

        data = str(data)
        now_time = self.now_str(formats="%Y-%m-%d %H:%M:%S")
        with self.mysql_connect.cursor() as cursor:

            cursor.execute(
                '''UPDATE %s SET data="%s",time="%s" WHERE machine_num=%s;''' % (tb_name, data, now_time, machine_num))
            self.mysql_connect.commit()
            return True



    def 处理振动数据(self):
        """
        把振动数据降频处理
        :return:
        """

        data = self.last_vibData['zdata']
        if self.load <= 0.5:
            self.val = sum(data) / len(data)
            data = [x - self.val for x in data]
        data = data[:60]
        val = 600
        max_abs_val = max(abs(min(data)), abs(max(data)))
        if 600 < max_abs_val < 1000:
            val = 1000
        elif 1000 < max_abs_val < 1500:
            val = 1500
        elif max_abs_val >= 1500:
            val = 2000
        data.insert(0, val)
        data = ",".join([str(i) for i in data])
        return data

    def 处理健康度(self):
        """
        通过算法把缓存的振动数据处理成刀具健康度然后发送到指定端口
        :return:
        """
        if settings.ANALYSIS_MODEL == 1:
            if self.changeTool:
                start_time = self.cycle_changeTool_start_time_str
                end_time = self.cycle_changeTool_end_time_str
                self.machineData_origin_cache = self.findArangeWithTime(start_time, end_time, type=2)
                self.vibration_originData_cache = self.findArangeWithTime(start_time, end_time, type=1)
                self.filter_data()
                self.changeTool = False
                if self.is_available:
                    H, flag_wear = self.运行对应算法计算健康度()
                    if H:
                        H = H[0]
                        print(H, flag_wear)
                    self.tool_hp_pre = self.tool_hp
                    self.tool_hp = H

                    self.发送健康度到云端()
                    self.刀具报警判断(flag_wear)


        else:
            # 根据时长来计算
            blanking_time = 5

            now = datetime.datetime.strptime(self.machine_time_str, "%Y-%m-%d-%H-%M-%S-%f")
            if self.changeTool or (now - self.last_transform_time) > timedelta(seconds=blanking_time):
                print(now, self.last_transform_time, (now - self.last_transform_time))
                start_time = self.last_transform_time.strftime(settings.SAVEDDATA_FILENAME_FORMAT)[:-3]
                end_time = now.strftime(settings.SAVEDDATA_FILENAME_FORMAT)[:-3]
                self.last_transform_time = now
                self.machineData_origin_cache = self.findArangeWithTime(start_time, end_time, type=2)
                self.vibration_originData_cache = self.findArangeWithTime(start_time, end_time, type=1)
                self.filter_data()
                self.changeTool = False
                if self.is_available:
                    H, flag_wear = self.运行对应算法计算健康度()
                    if H:
                        H = H[0]
                        print(H, flag_wear)
                    self.tool_hp_pre = self.tool_hp
                    self.tool_hp = H

                    self.发送健康度到云端()
                    self.刀具报警判断(flag_wear)


    def 刀具报警判断(self, flag_wear):
        """
        根据刀具健康度与前一个计算的健康度差值进行报警处理
        :return:
        """
        # 如果前一个健康度小于后一个健康度则不判断
        if self.tool_hp_pre < self.tool_hp:
            return False
        hp_abs_val = self.tool_hp_pre - self.tool_hp
        alpha = self.user_settings[self.tool_num_pre]["var1"]
        beta = self.user_settings[self.tool_num_pre]["var2"]
        flag = 0
        if flag_wear:
            print("磨损报警")
            self.写入日志("刀具%s-->出现磨损报警" % self.tool_num_pre)
            flag = 1
        #print(alpha)
        if alpha <= hp_abs_val < alpha + 0.2:
            print("崩缺报警")
            self.写入日志("刀具%s-->出现崩缺报警" % self.tool_num_pre)
            flag = 2
        elif alpha + 0.2 <= hp_abs_val:
            self.写入日志("刀具%s-->出现断刀报警" % self.tool_num_pre)
            print("断刀报警")
            flag = 3
        if self.load > settings.MAX_LOAD_WARMING:
            #self.进行机台报警()
            self.写入日志("机台%s-->负载过高报警" % self.deviceNo)
        if flag:
            self.进行机台报警()
            self.进行UI报警(type=flag)

    def 写入日志(self, msg):
        self.logger.warning(msg)

    def 进行UI报警(self, type):
        print("ui报警")
        with self.mysql_connect.cursor() as cursor:
            tool_num = int(self.tool_num_pre[1:])
            cursor.execute('''insert into warming(type,time,machine_num,tool_num,djgg) values('dd1',NOW(),%s,%s,'MX8-08');'''%(self.deviceNo, tool_num))
            self.mysql_connect.commit()
            return True

    def 进行机台报警(self):
        return
        machine_ip = settings.MACHINE1_IP
        alarm_flag = 511
        alarm_No = 3
        base_path = settings.BASE_PATH
        os.chdir(os.path.join(base_path, 'Alarm_API'))
        lib = ctypes.cdll.LoadLibrary('API.dll')
        lib.setAlarm.restype = ctypes.c_int
        ret = lib.setAlarm(machine_ip, len(machine_ip), alarm_flag, alarm_No)
        os.chdir(base_path)
        

    def 运行对应算法计算健康度(self):
        model = self.user_settings[self.tool_num_pre]["model"]
        alpha = self.user_settings[self.tool_num_pre]["var1"]
        beta = self.user_settings[self.tool_num_pre]["var2"]
        data = []
        ret = self.alarm(self.cal_data, float(beta))
        self.cal_data = []
        return ret

    '''
    输入：数据raw_data、崩缺调整系数alpha、磨损调整系数beta
    输出：健康度H、崩缺报警标志flag_notch、磨损报警标志flag_wear
    '''

    def alarm(self, raw_data, beta=0.60):

        flag_wear = 0
        feature = []
        feature_all = []
        data = []
        for i in range(len(raw_data)):
            data += raw_data[i]
        print(len(data))
        # 计算rms
        tem = np.array(data)
        rms = sqrt(np.sum(np.int64(tem ** 2)) / len(data))
        feature.append(rms)
        data = pd.Series(data)
        # 计算std、kurt
        std = data.rolling(5000).std()
        feature.append(std[6000])
        kurt = data.rolling(5000).kurt()
        feature.append(kurt[6000])
        feature_all.append(feature)

        # 预测健康度
        H = self.rf.predict(feature_all)
        # 磨损报警
        if H < beta:
            flag_wear = 1
        return H, flag_wear

    def 发送健康度到云端(self):
        #self.put_hpdata_to_cloud(self.tool_hp)
        tool_num = int(self.tool_num_pre[1:])
        device_num = int(self.deviceNo)
        self.更新健康度(device_num,tool_num,self.tool_hp)
        print("发送到云端:健康度->%s,刀具->%s" % (self.tool_hp, self.tool_num_pre))

    def 更新健康度(self, machine_num, tool_num, tool_hp):
        now_time = self.now_str(formats="%Y-%m-%d %H:%M:%S")
        sql = '''INSERT INTO tool_hp(hp, machine_num, tool_num,time) VALUES(%s,%s,%s,"%s");'''%(tool_hp, machine_num, tool_num, now_time)
        with self.mysql_connect.cursor() as cursor:
            cursor.execute(sql)
            self.mysql_connect.commit()
            return True

    @clothes(1000)
    def show_info(self):
        """
        显示当前算法运行状况
        """
        print("振动数据:%s;机台信息:%s;"%(len(self.vibration_originData_cache), len(self.machineData_origin_cache)))

    @property
    def is_available(self):
        data = []
        for i in range(len(self.cal_data)):
            data += self.cal_data[i]

        return True if len(data) >6000 else False


    def run(self) -> None:
        """
        每1秒获取一次数据 每次10条 间隔100毫秒
        """
        while 1:
            self.setup()
            while self.ready:
                try:
                    self.判断数据存在(int(self.deviceNo))
                    self.prepare_machineInfo()
                    #self.prepare_vibrationData()
                    self.处理健康度()
                    self.发送振动数据到云端()
                    self.发送负载数据到云端()
                    #self.show_info()
                except Exception as e:
                    print("错误信息：%s"%e)
                    print("错误行号：%s"% e.__traceback__.tb_lineno)
                    self.ready = False
                time.sleep(0.001)
            if not self.ready:
                print("五秒后重试")
                time.sleep(5)

    def check_or_create_necessary_file(self):
        """
        检查项目运行所需文件完整性
        :return:
        """
        # 检查用户设定文件
        pass

    def filter_data(self):
        """
        根据缓存数据筛分
        :return:
        """
       # print("开始筛分")
        time = 0
        count = 0
        for machinedata_line in self.machineData_origin_cache:
            try:
                _id = machinedata_line["_id"]
                actFeed = float(machinedata_line["actFeed"][0])
                actSpeed = float(machinedata_line["actSpeed"][0])
                load = machinedata_line["load"][0]
                setFeed = float(machinedata_line["setFeed"][0])
                setSpeed = float(machinedata_line["setSpeed"][0])
                last_time = time if time else machinedata_line["time"]
                time = machinedata_line["time"]
                tool = machinedata_line["tool"][0]
            except Exception as e:
                print(e)
                print(machinedata_line)
            if setFeed - 100 < actFeed < setFeed + 100 and setSpeed - 100 < actSpeed < setSpeed + 100:
                if count % 2 == 0:
                    start_time = datetime.datetime.strptime(time, "%Y-%m-%d-%H-%M-%S-%f")
                    count += 1
            else:
                if count % 2 == 1:
                    end_time = datetime.datetime.strptime(last_time, "%Y-%m-%d-%H-%M-%S-%f")
                    for sensor_line in self.vibration_originData_cache:
                        sensor_time = datetime.datetime.strptime(sensor_line["time"], "%Y-%m-%d-%H-%M-%S-%f")
                        if sensor_time > end_time:
                            break
                        if sensor_time > start_time:
                            self.cal_data.append(sensor_line["xdata"])
                    count += 1
        if count % 2 == 1:
            end_time = datetime.datetime.strptime(last_time, "%Y-%m-%d-%H-%M-%S-%f")
            for sensor_line in self.vibration_originData_cache:
                sensor_time = datetime.datetime.strptime(sensor_line["time"], "%Y-%m-%d-%H-%M-%S-%f")
                if sensor_time > end_time:
                    break
                if sensor_time > start_time:
                    self.cal_data.append(sensor_line["xdata"])
            count += 1

        self.vibration_originData_cache = []
        self.machineData_origin_cache = []
        #print("结束")

if __name__ == '__main__':

    print("检查更新中。。。")
    #p = subprocess.Popen(os.path.join(settings.BASE_PATH, "update.exe"))
    t = []



    t.append(ProcessData())
    # t.append(ProcessData())


    for t1 in t:
        t1.start()
    for t1 in t:
        t1.join()
