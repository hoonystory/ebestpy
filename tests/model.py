from src.constant.model import model
from src.constant import request


# print(model.get('t1484').get('out3'))
for i in request.future_option['market_data']:
    # print(i)
    if i in ['t9943', 't9944']:
        print(i)