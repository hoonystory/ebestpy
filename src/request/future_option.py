market_data = {
    'pathname': '/futureoption/market-data',
    't9943': {
        # 지수선물마스터조회API용
        # V:변동성지수선물 S:섹터지수선물 그 이외의 값은 코스피200지수선물
        'inblock': {
            'gubun': ''
        },
        'limit': 2,
        # 'code_list': [1]
    },
    't9944': {
        # 지수옵션마스터조회API용
        'inblock': {
            'gubun': ''
        },
        'limit': 2,
        # 'code_list': [1, 2, 3]
    },
}

chart = {
    'pathname': '/futureoption/chart',
    't8414': {
        # 선물옵션차트(틱/n틱)
    },
    't8416': {
        # 선물/옵션챠트(일주월)
    },
    't8429': {
        # EUREX야간옵션선물틱분별체결조회챠트
    },
    't8415': {
        # 선물/옵션챠트(N분)
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
        # 'code_list': []
    }
}