import pymongo.mongo_client
class Manager():
    def __init__(self):
        db=pymongo.mongo_client.MongoClient('127.0.0.1',27017).ipmph
        self.collection=db.sections
    def init(self):
        a = {'status': 1}
        while True:
            flag=self.collection.update({'status': 0}, {'$set': a})
            if not flag['updatedExisting']:
                break
    def save(self,data):
        self.collection.remove()
        for sectionDic in data:
            self.collection.insert({'chapterName':sectionDic[0],'_id':sectionDic[1],'sectionName':sectionDic[2],'sectionSum':sectionDic[3],'status':1})
    def getSection(self):
        sectionDic=self.collection.find_and_modify(query={'status': 1}, update={'$set': {'status': 0}})
        return sectionDic