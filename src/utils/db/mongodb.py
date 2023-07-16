import pymongo

# 주소를 쓰지 않을 경우 무조건 27017로 접속 aws를 쓸 경우 ('mongodb://ip주소')
connection = pymongo.MongoClient()

# db = connection["test"] 데이터베이스 없으면 만들어 짐
db = connection.test

# Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=False, connect=True), 'test')
print(db)

login_collection = db.login
login_info = {
    'access_token': ''
    , 'expires_in': 48430
}
login_collection.insert_one(login_info)
