from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.LinkedinData
DataSet = db.oldName
dict_all = DataSet.find()
for dict_name in dict_all:
    print(dict_name["name"])

