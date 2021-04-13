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
    cursor.execute("insert into test01(snap, hp) values('{0}', {1})".format(snap, val))
    ret = cursor.fetchone()
    mysql_connect.commit()
    print(ret)

def 更新负载(machine_num, data):
    data = str(data)
    cursor, conn = get_mysql_connect()
    cursor.execute("UPDATE djjk.`load` SET data='{0}' WHERE machine_num={1};".format(data, machine_num))
    conn.commit()
    ret = cursor.fetchone()
    print(ret)

def 更新加工状态(machine_num, data, type):
    data = str(data)

    cursor, conn = get_mysql_connect()
    cursor.execute("UPDATE djjk.vib_data SET data=%s WHERE machine_num=%s;", (data, machine_num))
    conn.commit()
    ret = cursor.fetchone()
    print(ret)


def 更新数据(machine_num, data, tb_name="vib_data"):
    data = str(data)
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor, conn = get_mysql_connect()

    with conn.cursor() as cursor:
        cursor.execute('''UPDATE %s SET data="%s",time="%s" WHERE machine_num=%s;'''%(tb_name, data, now_time, machine_num))
        conn.commit()
        return True

def 更新健康度(machine_num, tool_num, tool_hp):
    now_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor, conn = get_mysql_connect()
    with conn.cursor() as cursor:
        cursor.execute('''INSERT INTO tool_hp(hp, machine_num, tool_num,time) VALUES(%s,%s,%s,"%s");;'''%(tool_hp, machine_num, tool_num, now_time))
        conn.commit()
        return True

def 执行系列sql语句():
    cursor, conn = get_mysql_connect()
    execute_sql_list = []
    file_lists = ["machine_info.sql", "tool_info.sql", "load_data.sql", "tool_hp.sql", "vib_data.sql", "warming.sql", ]

    for file in file_lists:
        file_path = os.path.join(settings.BASE_PATH, "mysql_struct", file)
        with open(file_path, 'r+', encoding="utf-8") as f:
            sql_list = f.read().split(';')[:-1]  # sql文件最后一行加上;
            sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]
            execute_sql_list.append(sql_list)

    with conn.cursor() as cursor:

        print(conn.host_info)
        for sqls in execute_sql_list:
            for item in sqls:
                cursor.execute(item)
                print(item)
        conn.commit()
        ret = cursor.fetchall()
        print(ret)
        return True

def test():
    file_lists = ["machine_info.sql", "tool_info.sql", "load_data.sql", "tool_hp.sql", "vib_data.sql", "warming.sql", ]
    with open(u'load_data.sql', 'r+') as f:
        sql_list = f.read().split(';')[:-1]  # sql文件最后一行加上;
        sql_list = [x.replace('\n', ' ') if '\n' in x else x for x in sql_list]
        print(sql_list)
import time
if __name__ == '__main__':
    执行系列sql语句()