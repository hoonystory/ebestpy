from src.api.txn.txn import CommonTxnApi
from src.api.txn.t9943 import T9943
from src.api.txn.t9944 import T9944


tr_list = {
    'common': CommonTxnApi
    , 't9943': T9943()
    , 't9944': T9944()
}


def parse_transaction(tr_code):
    return tr_list[tr_code] if tr_code in tr_list else ''
