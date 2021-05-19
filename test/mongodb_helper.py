import pymongo
from bson import ObjectId

import settings

myclient = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000)

# dblist = myclient.list_database_names()
# print(dblist)
# mydb = myclient["VibrationData"]["Sensor"].find({"_id": {"$gte": ObjectId("60a3180785d2d9814c071113"),"$lte": ObjectId("60a3180885d2d9814c071115")}}, sort=[('_id', pymongo.DESCENDING)], limit=100)
#
# # for doc in mycol.find({},{ "_id": 1}, sort=[('_id', pymongo.DESCENDING)], limit=1000):
# #  doc in mycol.find({},{ "_id": 1}, sort=[('_id', pymongo.DESCENDING)], limit=1000)   print(doc)
# doc = list(mydb)[::-1]
# xdata = []
# ydata = []
# zdata = []
# for i in doc:
#     print(i)
#     xdata.extend(i['xdata'])
#     ydata.extend(i['ydata'])
#     zdata.extend(i['zdata'])
# # print(len(xdata))
# myclient.close()

def findArangeWithID(start_id: str, end_id: str, database="VibrationData", collection="Sensor"):
    """
    在mongodb中根据id查询范围内数据
    :param start_id:
    :param end_id:
    :return:
    """
    client = myclient
    mydb = client[database][collection].find(
        {"_id": {"$gte": "ObjectId(start_id)", "$lte": ObjectId(end_id)}},
        )
    return mydb

def get_last_data_MongoDB(type=1):
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
    col = myclient[databse][collection].find({},sort=[('_id',pymongo.DESCENDING)],limit=1)
    return col

def findArangeWithTime(start_time, end_time, database="VibrationData", collection="Sensor"):
    client = myclient
    mydb = client[database][collection].find(
        {"time": {"$gte": start_time, "$lte": end_time}},
        )
    return mydb
if __name__ == '__main__':
    ret_iter = findArangeWithTime()
    print(next(ret_iter)["_id"])
