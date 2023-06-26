def t9943():
    trCode = 't9943'
    pass


tr_list = {
    't9943': t9943
}


def parse_transaction(tr_code):
    return tr_list[tr_code] if tr_code in tr_list else ''
