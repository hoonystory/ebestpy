market_data = {
    'pathname': '/stock/market-data',
    't9945': {
        # 주식마스터조회API용
        # 구분(KSP:1KSD:2)
        'inblock': {
            'gubun': '1'
        },
        'limit': 2,
        # 'code_list': [1]
    }

}

chart = {
    'pathname': '/stock/chart',
    't8410': {
        # API전용주식챠트(일주월년)
        # 주기구분(2:일3:주4:월5:년)
        'inblock': {
            'shcode': '005930',
            'gubun': '4',
            'qrycnt': 500,
            'sdate': '20230101',
            'edate': '20240121',
            'cts_date': '',
            'comp_yn': 'N',
            'sujung': ''
        },
        'limit': 1
    },
    # 't8412': {
    #     # 주식챠트(N분)
    #     'inblock': {
    #         'shcode': '005930',
    #         'ncnt': 1,
    #         'qrycnt': 500,
    #         'nday': '0',
    #         'sdate': '20230727',
    #         'stime': '084500',
    #         'edate': '20230727',
    #         'etime': '154500',
    #         'cts_date': '',
    #         'cts_time': '',
    #         'comp_yn': 'N'
    #     },
    #     'limit': 1
    # },
    # 'code_list': []
}