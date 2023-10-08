header = {
    'content-type': 'application/json',
    'tr_cd': '',
    'Authorization': '',
    'tr_cont': 'N',
    'tr_cont_key': '0'
}
hostname = 'https://openapi.ebestsec.co.kr:8080'
websocket_domain = 'wss://openapi.ebestsec.co.kr:9443'
login = '/oauth2/token'
stock = {
    't8412': {
        'pathname': '/stock/chart',
        'inblock': {
            'shcode': '101T9000',
            'ncnt': 0,
            'qrycnt': 500,
            'nday': '0',
            'sdate': '20230727',
            'stime': '084500',
            'edate': '20230727',
            'etime': '154500',
            'cts_date': '20230727',
            'cts_time': '112530',
            'comp_yn': 'N'
        },
        'limit': 1
    },
    'code_list': []
}
future_option = {
    't8415': {
        'pathname': '/futureoption/chart',
        'inblock': {
            'shcode': '101T9000',
            'ncnt': 0,
            'qrycnt': 500,
            'nday': '0',
            'sdate': '20230727',
            'stime': '084500',
            'edate': '20230727',
            'etime': '154500',
            'cts_date': '20230727',
            'cts_time': '112530',
            'comp_yn': 'N'
        },
        'limit': 1,
        'code_list': [1, 2, 3]
    },
    't9943': {
        'pathname': '/futureoption/market-data',
        'inblock': {
            'gubun': ''
        },
        'limit': 2,
        'code_list': [1, 2, 3, 4]
    },

}
real_time = {
    'nws': {
        'pathname': '/websocket',
        'header': {
            'token': '',
            'tr_type': '3'
        },
        'body': {
            "tr_cd": "NWS",
            "tr_key": "NWS001"
        }
    }
}
