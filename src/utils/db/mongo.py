from pymongo import MongoClient
from config import mongodb
# from src.utils.log import log


# 방법1 - URI
# mongodb_URI = "mongodb://localhost:27017/"
# client = MongoClient(mongodb_URI)

class MongoDB:
    mongo_host = mongodb.config['local']['host']
    mongo_port = mongodb.config['local']['port']

    def __init__(self):
        # 방법2 - HOST, PORT
        self.client = MongoClient(host=self.mongo_host, port=self.mongo_port)
        # log.debug(self.client.list_database_names())

# ebest = client.ebest
# t8410 = ebest.t8410
