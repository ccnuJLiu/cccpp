from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.LinkedinData
DataSet = db.newName
a= DataSet.find().count()
print(a)
# for url in DataSet.distinct("name"):
#     num = DataSet.count({"name":url})
#     for i in range(1,num):
#         DataSet.remove({"name":url})
# print(DataSet.count())


# dict_all = DataSet.find()
# for dict_name in dict_all:
#     print(dict_name["name"])

