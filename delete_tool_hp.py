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

def test_put_hp_to_mysql(snap, val):
    cursor, mysql_connect = get_mysql_connect()
    cursor.execute('''truncate table tool_hp''')
    ret = cursor.fetchone()
    mysql_connect.commit()
    print(ret)
') if '\n' in x else x for x in sql_list]
        print(sql_list)
import time
if __name__ == '__main__':
    test_put_hp_to_mysql("vib_data", 2)