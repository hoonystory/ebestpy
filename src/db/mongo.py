from pymongo import MongoClient
# from config import mongodb
# from src.utils.log import log


# 방법1 - URI
# mongodb_URI = "mongodb://localhost:27017/"
# client = MongoClient(mongodb_URI)

config = {
    'local': {
        'port': 27017,
        'host': 'localhost',

    }
}


class MongoDB:
    db_name = 'mongo'
    # mongo_host = mongodb.config['local']['host']
    # mongo_port = mongodb.config['local']['port']
    mongo_host = config['local']['host']
    mongo_port = config['local']['port']

    def __init__(self):
        # 방법2 - HOST, PORT
        self.client = MongoClient(host=self.mongo_host, port=self.mongo_port)
        try:
            print(self.client.list_database_names())
            # self.database = self.client['realtime']
            # self.collection = self.database['nws']
        except Exception as e:
            raise Exception(
                "The following error occurred: ", e)
        # log.debug(self.client.list_database_names())

    def insert(self, database, collection, json_data):
        try:
            db = self.client[database]
            col = db.database[collection]
            print(db, col)

            result = col.insert_one(json_data)
            print(result.acknowledged)
        except Exception as e:
            raise Exception(
                "The following error occurred: ", e)
# ebest = client.ebest
# t8410 = ebest.t8410
