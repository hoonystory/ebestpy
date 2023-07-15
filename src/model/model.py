"""
트랜잭션 요청 시,
필요한 파라미터 리스트, 결과값을 받아올 때 필요한 파라미터 리스트 나열
"""

model = {
    't1485': {
        'in': ['upcode', 'gubun'],
        'out1': ['pricejisu', 'sign', 'change', 'volume', 'yhighjo'
            , 'yupjo', 'yunchgjo', 'ylowjo', 'ydownjo', 'ytrajo'],
        'out2': ['chetime', 'jisu', 'sign', 'change', 'volume', 'volcha']
    },
    't9943': {
        'in': ['gubun'],
        'out1': ['hname', 'shcode', 'expcode']
    },
    't9944': {
        'in': ['dummy'],
        'out': ['hname', 'shcode', 'expcode']
    }
}