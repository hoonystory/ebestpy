

class T9943:
    """
    # 지수선물마스터조회 API용
    # gubun     : 구분(V: 변동성지수선물, S: 섹터지수선물, 그 외 코스피200지수선물)
    """
    in_field = None
    out_field = None

    def __init__(self):
        self.in_field = ['gubun']
        self.out_field = ['hname', 'shcode', 'expcode']
