import datetime
import os

import pymysql
import settings




def get_mysql_connect():
    """
    获取上传刀具健康度的mysql连接
    """
    mysql_connect = pymysql.connect(**settings.mysql_info)
    cursor = mysql_connect.cursor()
    return cursor, mysql_connect

print("1")

import time
if __name__ == '__main__':
    print("hello")
    print(sys.argv[0])
    
    #test_put_hp_to_mysql("vib_data", 2)