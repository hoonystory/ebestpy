# -*- coding: utf-8 -*-
import funcs

"""
    shcode: 종목코드
    upcode: 업종코드
    focode: 종목코드
    ncnt: 틱/분
    qrycnt: 요청건수
    gubun: 구분
    sdate: 시작일자
    edate: 종료일자
    comp_yn: 압축여부

    cts_time: 연속조회
    cts_date: 연속조회

    ***********
    중요: mysql 오늘 날짜 디폴트 값으로 넣어야함...!
    ***********

    t1102 : 주식 현재가(시세) 조회 (단일데이터)     비정기       x
    t1485 : 예상지수                               정기       o
    t1511 : 업종현재가 (상승하락종목수 조회)        정기        o
    t1603 : 시간대별 투자자 매매추이 상세           정기       o
    t1662 : 시간대별 프로그램 매매추이(차트)        정기        o

    t1921 : 신용거래동향                           비정기      
    t1926 : 종목별 신용/대주 현황                  정기        
    t1927 : 공매도일별추이                         정기      
    t2201 : 선물옵션 시간대별 체결조회              정기
    t2203 : 선물옵션 기간별 주가                    비정기      x
    t2301 : 옵션 전광판                            정기        x
    t2405 : 선물옵션 호가잔량 비율 차트             정기      x

    t2804 : CME야간선물 시간대별 체결조회           정기
    t2805 : CME 기간별 주가                        비정기       x
    t2813 : CME야간선물 시간대별투자자매매추이      정기     x
    t2814 : CME야간선물 기간별투자자매매추이(차트)   비정기        x
    t2832 : EUREX 야간옵션 시간대별체결 조회        정기
    t2833 : EUREX 야간옵션 기간별 추이              비정기      x
    t2835 : EUREX 야간옵션 전광판                  정기      x
    
    t3102 : 뉴스본문									(보류)정기
	t3202 : 종목별 증시일정							정기
	t3320 : FNG_요약									비정기
	t3518 : 해외실시간지수							정기

    t8408 : CME야간선물 틱분별조회   << 30초 조회   정기      x   <<< 연속조회 되지 않음, 보류
    t8409 : CME야간선물 미결제약정추이              정기       
    t8412 : 주식차트(n분)                          정기        1분 단위
    t8413 : 주식차트(일주월)                       비정기     일 단위 
    t8414 : 선물옵션차트(틱/n틱)                   정기       1틱 단위
    t8415 : 선물옵션차트(n분)                                  30초 단위
    t8416 : 선물옵션차트(일/주/월)                 비정기        일 단위
    t8417 : 업종차트(틱/n틱)                       정기     1틱 단위
    t8418 : 업종차트(n분)                          정기     30초 단위
    t8418 : 업종차트(일주월)                         비정기     일 단위
    t8424 : 업종전체조회                           정기     x
    t8427 : 선물옵션 과거데이터시간대별조회          비정기   x
    t8428 : 증시주변자금추이							정기
    t8429 : EUREX 야간옵션 틱분별체결조회  << 30초 조회   정기 
    t8430 : 주식종목조회                            정기    x
    t9943 : 지수선물마스터조회 API용                 정기   x
    t9944 : 지수옵션마스터조회 API용                 정기   x

    NWS   : 실시간 뉴스 제목 패킷

    t1102 : 주식 현재가(시세) 조회 (단일데이터)     비정기
    t1921 : 신용거래동향                           비정기
    t2203 : 선물옵션 기간별 주가                    비정기
    t2805 : CME 기간별 주가                        비정기
    t2814 : CME야간선물 기간별투자자매매추이(차트)   비정기
    t2833 : EUREX 야간옵션 기간별 추이              비정기
    t3320 : FNG_요약									비정기
    t8427 : 선물옵션 과거데이터시간대별조회          비정기
"""


db_name = 'eBestDB'

strtLogin = ', Start on eBest Login---'
strtFunction = ', Start on Function---'
strtDatabase = ', Start on Database Login---'

trList = [ "t1485", "t1511", "t1603", "t1662", "t1921", "t1926", "t1927"
    , "t2201", "t2301", "t2405", "t2804", "t2813", "t2814", "t2832", "t2835"
    , "t3202", "t3320", "t3518"
    , "t8409", "t8412", "t8414", "t8415", "t8417", "t8428"]

# t8408, t8429(모두 CME)는 장 중에 처리해줘야 하는 이슈로 현재 리스트에서 제거
# >> 1분봉 처리로 변경


def parseInfield(trCode):
    """요청 TR 코드 Infield 파싱
        :param trCode: TR 코드
        :type trCode: str
        :return: TR코드 Infield 반환
    """
    ht = {
        # t1102     : 주식 현재가(시세) 조회 (단일데이터)
        "t1102":    ['shcode'],

        # t1485     : 예상지수
        "t1485":    ['upcode', 'gubun'],
        # gubun     : string, 1 :   조회구분(1: 장전, 2: 장후)

        # t1511     : 업종현재가 (상승하락종목수 조회)
        "t1511":    ['upcode'],

        # t1603     : 시간대별 투자자 매매추이 상세
        "t1603":    ['market', 'gubun1', 'gubun2', 'cnt', 'upcode'],
        # market    : string, 1 :   시장구분(1: 코스피, 2: 코스닥, 3: 선물, ...)
        # gubun1    : string, 1 :   투자자구분(1: 개인, 2: 외인, 3: 기관계, ...)
        # gubun2    : string, 1 :   전일분구분(0: 당일, 1: 전일)

        # t1662     : 시간대별 프로그램 매매추이(차트)
        "t1662":    ['gubun', 'gubun1', 'gubun3'],
        # gubun     : string, 1 :   구분(0: 코스피, 1: 코스닥)
        # gubun1    : string, 1 :   금액수량구분(0: 금액, 1: 수량)
        # gubun3    : string, 1 :   전일구분(0: 당일, 1: 전일)

        # t1921     : 신용거래동향
        "t1921":    ['shcode', 'gubun', 'date'],
        # gubun     : string, 1 : 융자/대주 구분(1: 융자, 2: 대주)

        # t1926     : 종목별 신용/대주 현황
        "t1926":    ['shcode'],

        # t1927     : 공매도일별추이
        "t1927":    ['shcode', 'date', 'sdate', 'edate'],
        # date      : 다음 조회 시, 사용(outfield에 date 입력)

        # t2201     : 선물옵션 시간대별 체결조회
        "t2201":    ['focode', 'cvolume', 'stime', 'etime'],
        # cvolume   : long, 12  :   특이거래량(체결수량 >= cvolume)
        # stime     : string, 4 :   시작시간
        # etime     : string, 4 :   종료시간

        # t2203     : 선물옵션 기간별 주가
        "t2203":    ['shcode', 'futcheck', 'date', 'cts_code', 'lastdate', 'cnt'],
        # futcheck  : 선물최근월물(0: default, 1: 최근월물만 연결)
        # date      : space
        # cts_code  : space
        # lastdate  : space
        # cnt       : 조회요청건수

        # t2301     : 옵션 전광판
        "t2301":    ['yyyymm', 'gubun'],
        # yyyymm    : 월물
        # gubun     : 미니구분(M: 미니, G: 정규)

        # t2405     : 선물옵션 호가잔량 비율 차트
        "t2405":    ['focode', 'bgubun', 'nmin', 'etime', 'hgubun', 'cnt'],
        # focode    : 단축코드
        # bgubun    : 분구분(0: 30초, 1: 분)
        # nmin      : N분
        # etime     : 종료시간
        # hgubun    : 호가구분(0: 총 호가잔량, 1: 1차 호가잔량, ... 5: 5차 호가잔량)

        # t2804     : CME 시간대별 체결조회
        "t2804":    ["focode", "cvolume", "stime", "etime", "cts_time"],

        # t2805     : CME 기간별 주가
        "t2805":    ['shcode', 'futcheck', 'date', 'cts_code', 'lastdate', 'cnt'],

        # t2813     : CME 야간선물 시간대별투자자매매추이
        "t2813":    ['gubun1', 'gubun2', 'cts_time', 'cts_idx', 'cnt', 'gubun3'],
        # gubun1    : string, 1 :   수량구분(1: 수량, 2: 금액)
        # gubun2    : string, 1 :   전일분구분(0: 금일, 1: 전일)
        # gubun3    : string, 1 :   직전대비(C: 직전대비, null: 누적)

        # t2814     : CME 야간선물 기간별투자자매매추이(차트)
        "t2814":    ['gubun1', 'gubun2', 'from_date', 'to_date'],
        # gubun1    : string, 1 :   수치구분(1: 수치, 2: 누적)
        # gubun2    : string, 1 :   단위구분(1: 일, 2: 주, 3: 월)
        # from_date : string, 8 :   시작날짜
        # to_date   : string, 8 :   종료날짜

        # t2832     : EUREX 야간옵션 시간대별체결조회
        "t2832":    ['focode', 'cvolume', 'stime', 'etime'],

        # t2833     : EUREX 야간옵션 기간별 추이
        "t2833":    ['shcode', 'futcheck', 'date', 'cts_code', 'lastdate', 'cnt'],

        # t2835     : EUREX 야간옵션 전광판
        "t2835":    ['yyyymm'],

        # t3102     : 뉴스본문
        "t3102":    ['sNewsno'],

        # t3202     : 종목별 증시일정
        "t3202":    ['shcode', 'date'],

        # t3320     : FNG_요약
        "t3320":    ['gicode'],

        # t3518     : 해외실시간지수
        "t3518":    ['kind', 'symbol', 'cnt', 'jgbn', 'nmin', 'cts_date', 'cts_time'],

        # t8408     : CME 야간선물 틱분별조회
        "t8408":    ['focode', 'cgubun', 'bgubun', 'cnt'],
        # cgubun    : string, 1 :   차트구분(T: 틱차트, B: 분차트)
        # bgubun    : string, 3 :   분구분
        # cnt       : string, 3 :   조회건수

        # t8409     : CME 야간선물 미결제약정추이
        "t8409":    ['focode', 'bdgubun', 'nmin', 'tcgubun', 'cnt'],
        # bdgubun   : string, 1 :   분일구분(0: 30초, 1: 분, 2: 일)
        # nmin      : string, 3 :   N분
        # tcgubun   : string, 1 :   당일연결구분(0: 전체, 1: 당일)
        # cnt       : string, 4 :   조회건수

        # t8412     : 주식차트(n분)
        "t8412":    ['shcode', 'ncnt', 'qrycnt', 'sdate', 'edate', 'comp_yn'],
        # ncnt      : string, 4 :   단위(n틱)
        # qrycnt    : string, 4 :   요청건수
        # sdate     : string, 8 :   시작일자
        # edate     : string, 8 :   종료일자

        # t8413     : 주식차트(일주월)
        "t8413":    ['shcode', 'gubun', 'sdate', 'edate', 'comp_yn'],
        # gubun     : 주기구분(2: 일, 3: 주, 4: 월)
        # sdate     : string, 8 :   시작일자
        # edate     : string, 8 :   종료일자

        # t8414     : 선물옵션차트(틱/n틱)
        "t8414":    ['shcode', 'ncnt', 'qrycnt', 'sdate', 'edate', 'comp_yn'],
        # ncnt      : string, 4 :   단위(n틱)
        # qrycnt    : string, 4 :   요청건수
        # sdate     : string, 8 :   시작일자
        # edate     : string, 8 :   종료일자

        # t8414     : 선물옵션차트(n분)
        "t8415":    ['shcode', 'ncnt', 'qrycnt', 'sdate', 'edate', 'comp_yn'],

        # t8416     : 선물옵션차트(일/주/월)
        "t8416":    ['shcode', 'gubun', 'sdate', 'edate', 'comp_yn'],
        # gubun     : 주기구분(2: 일, 3: 주, 4: 월)
        # sdate     : string, 8 :   시작일자
        # edate     : string, 8 :   종료일자

        # t8417     : 업종차트(틱/n틱)
        "t8417":    ['shcode', 'ncnt', 'qrycnt', 'sdate', 'edate', 'comp_yn'],

        # t8418     : 업종차트(n분)
        "t8418":    ['shcode', 'ncnt', 'qrycnt', 'sdate', 'edate', 'comp_yn'],

        # t8419     : 업종차트(일주월)
        "t8419":    ['shcode', 'gubun', 'sdate', 'edate', 'comp_yn'],

        # t8424     : 업종전체조회
        "t8424":    ['gubun1'],
        # gubun1    : null

        # t8427     : 선물옵션 과거데이터시간대별조회
        "t8427":    ['fo_gbn', 'yyyy', 'mm', 'cp_gbn', 'actprice',
                     'focode', 'dt_gbn', 'min_term', 'date', 'time'],
        # fo_gbn    : 선물옵션구분(F: 선물, O: 옵션)
        # cp_gbn    : 옵션콜풋구분(2: 콜, 3: 풋)
        # actprice  : 옵션행사가
        # focode    : 선물옵션코드
        # dt_gbn    : 일분구분(D: 일, M: 분)
        # min_term  : 분간격

        # t8428     : 증시주변자금추이
        "t8428":    ['fdate', 'tdate', 'gubun', 'key_date', 'upcode', 'cnt'],

        # t8429     : EUREX 야간옵션 틱분별체결조회
        "t8429":    ['focode', 'cgubun', 'bgubun', 'cnt'],
        # cgubun    : string, 1 :   차트구분(T: 틱차트, B: 분차트)
        # bgubun    : string, 3 :   분구분(0: 30초, 0초과: n분)
        # cnt       : string, 3 :   cnt

        # t8430     : 주식종목조회
        "t8430":    ['gubun'],
        # gubun     : 구분(0: 전체, 1: 코스피, 2: 코스닥)

        # t9943     : 지수선물마스터조회 API용
        "t9943":    ['gubun'],
        # gubun     : 구분(V: 변동성지수선물, S: 섹터지수선물, 그 외 코스피200지수선물)

        # t9944     : 지수옵션마스터조회 API용
        "t9944":    ['dummy'],
        # dummy     : null

        # NWS       : 실시간 뉴스 제목 패킷
        "nws":      ['nwcode'],
        # nwcode    : NWS001

        "CSPAT00600": ['AcntNo', 'InptPwd', 'IsuNo',
                       'OrdQty', 'OrdPrc', 'BnsTpCode',
                       'OrdprcPtnCode', 'MgntrnCode', 'LoanDt', 'OrdCndiTpCode']
        # AcntNo        : 계좌번호
        # InptPwd       : 입력비밀번호
        # IsuNo         : 종목번호
        # OrdQty        : 주문수량
        # OrdPrc        : 주문가
        # BnsTpCode     : 매매구분
        # OrdprcPtnCode : 호가유형코드
        # MgnTrnCode    : 신용거래코드
        # LoanDt        : 대출일
        # OrdCndiTpCode : 주문조건구분
    }
    return ht[trCode] if trCode in ht else ""


def parseOutfield(trCode):
    """요청 TR 코드 Outfield 파싱
        :param trCode: TR 코드
        :type trCode: str
        :return: TR코드 Outfield 반환
    """
    ht = {
        "t1102":    [
            ['hname', 'price']
        ],
        "t1485":    [
            ['pricejisu', 'sign', 'change', 'volume',
             'yhighjo', 'yupjo', 'yunchgjo', 'ylowjo', 'ydownjo', 'ytrajo'],
            ['chetime', 'jisu', 'sign', 'change', 'volume', 'volcha']
        ],
        "t1511":    [
            ['gubun', 'hname', 'pricejisu', 'jniljisu', 'sign',
             'change', 'diffjisu', 'jnilvolume', 'volume', 'volumechange',
             'volumerate', 'jnilvalue', 'value', 'valuechange', 'valuerate',
             'openjisu', 'opendiff', 'opentime',
             'highjisu', 'highdiff', 'hightime',
             'lowjisu', 'lowdiff', 'lowtime',
             'whjisu', 'whchange', 'whjday',
             'wljisu', 'wlchange', 'wljday',
             'yhjisu', 'yhchange', 'yhjday',
             'yljisu', 'ylchange', 'yljday',
             'highjo', 'upjo', 'unchgjo', 'lowjo', 'downjo']
        ],
        "t1603":    [
            ['cts_idx'],
            ['time', 'tjjcode',
             'msvolume', 'mdvolume', 'msvalue', 'mdvalue',
             'svolume', 'svalue']
        ],
        "t1662":    [
            ['time', 'k200jisu', 'sign', 'change', 'k200basis',
             'tot3', 'tot1', 'tot2',
             'cha3', 'cha1', 'cha2',
             'bcha3', 'bcha1', 'bcha2',
             'volume']
        ],
        "t1921":    [
            ['cnt', 'date', 'idx'],
            ['mmdate', 'close', 'sign', 'jchange', 'diff',
             'nvolume', 'svolume', 'jvolume', 'price', 'change',
             'gyrate', 'jkrate', 'shcode']
        ],
        "t1926":    [
            ['ynvolume', 'ysvolume', 'yjvolume', 'yychange', 'ygrate',
             'yjrate', 'ynprice', 'ysprice', 'yjprice', 'yachange',
             'dnvolume', 'dsvolume', 'djvolume', 'dvchange', 'dgrate',
             'djrate', 'dnprice', 'dsprice', 'djprice', 'dachanage',
             'mmdate', 'close', 'volume', 'value', 'pr5days', 'pr20days',
             'yj5days', 'yj20days', 'dj5days', 'dj20days']
        ],
        "t1927":    [
            ['date'],
            ['date', 'price', 'sign', 'change', 'diff',
             'volume', 'value', 'gm_vo', 'gm_va', 'gm_per',
             'gm_avg', 'gm_vo_sum']
        ],
        "t2201":    [
            ['cts_time'],
            ['chetime', 'price', 'sign', 'change', 'cvolume',
             'chdegree', 'offerho', 'bidho', 'volume', 'openyak',
             'jnilopenupdn', 'ibasis', 'sbasis', 'kasis', 'value',
             'j_openupdn', 'n_msvolume', 'n_mdvolume',
             's_msvolume', 'n_mschecnt', 'n_mdchecnt', 's_mschecnt']
        ],
        "t2203":    [
            ['date', 'cts_code', 'lastdate', 'nowfutyn'],
            ['date', 'open', 'high', 'low', 'close',
             'sign', 'change', 'diff', 'volume', 'diff_vol',
             'openyak', 'openyakupdn', 'value']
        ],
        "t2301":    [
            ['histimpv',
             'jandatecnt',
             'cimpv', 'pimpv',
             'gmprice', 'gmsign', 'gmchange',
             'gmdiff', 'gmvolume', 'gmshcode'],
            ['actprice', 'optcode',
             'price', 'sign', 'change',
             'diff', 'volume', 'iv', 'mgjv', 'mgjvupdn',
             'delt', 'gama', 'vega', 'ceta', 'rhox',
             'theoryprice', 'impv', 'timevl',
             'open', 'high', 'low',
             'atmgubun', 'jisuconv', 'value'],
            ['actprice', 'optcode',
             'price', 'sign', 'change',
             'diff', 'volume', 'iv', 'mgjv', 'mgjvupdn',
             'delt', 'gama', 'vega', 'ceta', 'rhox',
             'theoryprice', 'impv', 'timevl',
             'open', 'high', 'low',
             'atmgubun', 'jisuconv', 'value']
        ],
        "t2405":    [
            ['mdvolume', 'mdchecnt', 'msvolume', 'mschecnt',
             'cts_time'],
            ['time', 'price', 'sign', 'change', 'volume', 'cvolume',
             'offerho1', 'bidho1', 'offerrem', 'bidrem',
             'offercnt', 'bidcnt', 'c_offerrem', 'c_bidrem',
             'c_offercnt', 'c_bidcnt',
             'r_bidrem', 'r_bidcnt', 'r_sign',
             'date']
        ],
        "t2804":    [
            ['cts_time'],
            ['chetime', 'chetime24', 'price', 'sign', 'change',
             'cvolume', 'chdegree', 'offerho', 'bidho', 'volume',
             'openyak', 'jnilopenupdn', 'ibasis', 'sbasis', 'kasis',
             'value', 'j_openupdn', 'n_msvolume', 'n_mdvolume', 's_msvolume',
             'n_mschecnt', 'n_mdchecnt', 's_mschecnt']
        ],
        "t2805":    [
            ['date', 'cts_code', 'lastdate', 'nowfutyn'],
            ['date', 'open', 'high', 'low', 'close',
             'sign', 'change', 'diff', 'volume', 'diff_vol',
             'openyak', 'openyakupdn', 'value']
        ],
        "t2813":    [
            ['date',
             'tjjcode_08', 'ms_08', 'md_08', 'rate_08', 'svolume_08',
             'tjjcode_17', 'ms_17', 'md_17', 'rate_17', 'svolume_17',
             'tjjcode_18', 'ms_18', 'md_18', 'rate_18', 'svolume_18',
             'tjjcode_01', 'ms_01', 'md_01', 'rate_01', 'svolume_01',
             'tjjcode_03', 'ms_03', 'md_03', 'rate_03', 'svolume_03',
             'tjjcode_04', 'ms_04', 'md_04', 'rate_04', 'svolume_04',
             'tjjcode_02', 'ms_02', 'md_02', 'rate_02', 'svolume_02',
             'tjjcode_05', 'ms_05', 'md_05', 'rate_05', 'svolume_05',
             'tjjcode_06', 'ms_06', 'md_06', 'rate_06', 'svolume_06',
             'tjjcode_07', 'ms_07', 'md_07', 'rate_07', 'svolume_07',
             'tjjcode_11', 'ms_11', 'md_11', 'rate_11', 'svolume_11',
             'tjjcode_00', 'ms_00', 'md_00', 'rate_00', 'svolume_00'],
            ['time',
             'sv_08', 'sv_17', 'sv_18', 'sv_01', 'sv_03', 'sv_04',
             'sv_02', 'sv_05', 'sv_06', 'sv_07', 'sv_11', 'sv_00']
        ],
        "t2814":    [
            ['mcode', 'mname'],
            ['date',
             'sv_08', 'sv_17', 'sv_18', 'sv_01', 'sv_03', 'sv_04', 'sv_02',
             'sv_05', 'sv_06', 'sv_07', 'sv_00', 'sv_09', 'sv_10', 'sv_11', 'sv_99',
             'sa_08', 'sa_17', 'sa_18', 'sa_01', 'sa_03', 'sa_04', 'sa_02',
             'sa_05', 'sa_06', 'sa_07', 'sa_00', 'sa_09', 'sa_10', 'sa_11', 'sa_99',
             'jisu']
        ],
        "t2832":    [
            ['cts_time'],
            ['chetime', 'price', 'sign', 'change', 'cvolume', 'chdegree',
             'offerho', 'bidho', 'volume', 'n_msvolume', 'n_mdvolume', 's_msvolume',
             'n_mschecnt', 'n_mdchecnt', 's_mschecnt']
        ],
        "t2833":    [
            ['date', 'cts_code', 'lastdate', 'nowfutyn'],
            ['date', 'open', 'high', 'low', 'close',
             'sign', 'change', 'diff', 'volume', 'diff_vol']
        ],
        "t2835":    [
            ['gmprice', 'gmsign', 'gmdiff', 'gmvolume', 'gmshcode'],
            ['actprice', 'optcode',
             'price', 'sign', 'change',
             'diff', 'volume', 'cvolume', 'impv', 'timevl',
             'open', 'high', 'low',
             'atmgubun', 'jisuconv'],
            ['actprice', 'optcode',
             'price', 'sign', 'change',
             'diff', 'volume', 'cvolume', 'impv', 'timevl',
             'open', 'high', 'low',
             'atmgubun', 'jisuconv'],
        ],
        "t3102":    [
            ['sJongcode'],
            ['sBody']
        ],
        "t3202":    [
            ['recdt', 'tableid', 'upgu',
             'custono', 'custnm', 'shcode', 'upnm']
        ],
        "t3320":    [
            ['upgubunnm', 'sijangcd', 'marketnm',
             'company', 'baddress', 'btelno',
             'gsyyyy', 'gsmm', 'lstprice',
             'gstock', 'homeurl', 'grdnm',
             'foreignratio', 'irtel', 'capital',
             'sigavalue', 'cashsis', 'cashrate',
             'price', 'jnilclose'],
            ['gicode', 'gsym', 'gsgb',
             'per', 'eps', 'pbr', 'roa', 'roe',
             'ebitda', 'evebitda', 'par', 'sps',
             'cps', 'bps', 't_per', 't_eps',
             'peg', 't_peg', 't_gsym']
        ],
        "t3518":    [
            ['cts_date', 'cts_time'],
            ['date', 'time', 'open', 'high', 'low',
             'price', 'sign', 'change', 'uprate',
             'volume', 'bidho', 'offerho', 'bidrem', 'offerrem',
             'kind', 'symbol', 'exid', 'kodate', 'kotime']
        ],
        "t8408":    [
            [],
            ['chetime', 'price', 'sign', 'change', 'open', 'high', 'low',
             'volume', 'value', 'openyak', 'openupdn', 'cvolume',
             's_mschecnt', 's_mdchecnt', 'ss_mschecnt',
             's_mschevol', 's_mdchevol', 'ss_mschevol',
             'chdegvol', 'chdegcnt']
        ],
        "t8409":    [
            ['price', 'sign', 'change', 'diff', 'cvolume', 'volume', 'openyak'],
            ['dt', 'open', 'high', 'low', 'close',
             'openopenyak', 'highopenyak', 'lowopenyak', 'closeopenyak', 'openupdn']
        ],
        "t8412":    [
            ['shcode',
             'jisiga', 'jihigh', 'jilow', 'jiclose', 'jivolume',
             'disiga', 'dihigh', 'dilow', 'diclose',
             'highend', 'lowend'],
            ['date', 'time',
             'open', 'high', 'low', 'close',
             'jdiff_vol', 'value',
             'jongchk', 'rate', 'sign']
        ],
        "t8413":    [
            ['shcode',
             'jisiga', 'jihigh', 'jilow', 'jiclose', 'jivolume',
             'disiga', 'dihigh', 'dilow', 'diclose',
             'highend', 'lowend'],
            ['date',
             'open', 'high', 'low', 'close',
             'jdiff_vol', 'value',
             'jongchk', 'rate', 'pricechk', 'ratevalue',
             'sign']
        ],
        "t8414":    [
            ['shcode',
             'jisiga', 'jihigh', 'jilow', 'jiclose', 'jivolume',
             'disiga', 'dihigh', 'dilow', 'diclose',
             'highend', 'lowend'],
            ['date', 'time',
             'open', 'high', 'low', 'close',
             'jdiff_vol', 'openyak']
        ],
        "t8415":    [
            ['shcode',
             'jisiga', 'jihigh', 'jilow', 'jiclose', 'jivolume',
             'disiga', 'dihigh', 'dilow', 'diclose',
             'highend', 'lowend'],
            ['date', 'time',
             'open', 'high', 'low', 'close',
             'jdiff_vol', 'value', 'openyak']
        ],
        "t8416":    [
            ['shcode',
             'jisiga', 'jihigh', 'jilow', 'jiclose', 'jivolume',
             'disiga', 'dihigh', 'dilow', 'diclose',
             'highend', 'lowend'],
            ['date',
             'open', 'high', 'low', 'close',
             'jdiff_vol', 'value', 'openyak']
        ],
        "t8417":    [
            ['shcode',
             'jisiga', 'jihigh', 'jilow', 'jiclose', 'jivolume',
             'disiga', 'dihigh', 'dilow', 'diclose'],
            ['date', 'time',
             'open', 'high', 'low', 'close',
             'jdiff_vol']
        ],
        "t8418":    [
            ['shcode',
             'jisiga', 'jihigh', 'jilow', 'jiclose', 'jivolume',
             'disiga', 'dihigh', 'dilow', 'diclose', 'disvalue'],
            ['date', 'time',
             'open', 'high', 'low', 'close',
             'jdiff_vol', 'value']
        ],
        "t8419":    [
            ['shcode',
             'jisiga', 'jihigh', 'jilow', 'jiclose', 'jivolume',
             'disiga', 'dihigh', 'dilow', 'diclose', 'disvalue'],
            ['date',
             'open', 'high', 'low', 'close',
             'jdiff_vol', 'value']
        ],
        "t8424":    [
            ['hname', 'upcode']
        ],
        "t8427":    [
            ['focode', 'date', 'time'],
            ['date', 'time',
             'open', 'high', 'low', 'close',

             'change', 'diff', 'volume',
             'diff_vol', 'openyak', 'openyakupdn', 'value']
        ],
        "t8428":    [
            ['date', 'idx'],
            ['date', 'jisu', 'sign', 'change', 'diff',
             'volume', 'customoney', 'yecha',
             'vol', 'outmoney', 'trjango',
             'futymoney', 'stkmoney', 'mstkmoney',
             'mbndmoney', 'bndmoney', 'bndsmoney',
             'mmfmoney']
        ],
        "t8429":    [
            [],
            ['chetime', 'price', 'sign', 'change', 'open', 'high', 'low',
             'volume', 'cvolume',
             's_mschecnt', 's_mdchecnt', 'ss_mschecnt',
             's_mschevol', 's_mdchevol', 'ss_mschevol',
             'chdegvol', 'chdegcnt']
        ],
        "t8430":    [
            ['hname', 'shcode', 'expcode', 'etfgubun',
             'uplmtprice', 'dnlmtprice', 'jnilclose', 'memedan',
             'recprice', 'gubun']
        ],
        "t9943":    [
            ['hname', 'shcode', 'expcode']
        ],
        "t9944":    [
            ['hname', 'shcode', 'expcode']
        ],

        "nws":      ['date', 'time', 'id', 'realkey', 'title', 'code'],

        "CSPAT00600":   [
            [],
            ['RecCnt', 'AcntNo', 'InptPwd',
             'IsuNo', 'OrdQty', 'OrdPrc',
             'BnsTpCode', 'OrdPrcPtnCode', 'PrgmOrdprcPtnCode',
             'StslAbleYn', 'StslOrdprcTpCode',
             'CommdaCode', 'MgntrnCode', 'LoanDt',
             'MbrNo', 'OrdCndiTpCode', 'StrtgCode',
             'GrpId', 'OrdSeqNo', 'PtflNo',
             'BskNo', 'TrchNo', 'ItemNo',
             'OpDrtnNo', 'LpYn', 'CvrgTpCode'],
            ['RecCnt', 'OrdNo', 'OrdTime',
             'OrdMktCode', 'OrdPtnCode', 'ShtnlsuNo',
             'MgempNo', 'OrdAmt', 'SpareOrdNo',
             'CvrgSeqno', 'RsvOrdNo', 'SpotOrdQty',
             'RuseOrdQty', 'MnyOrdAmt', 'SubstOrdAmt',
             'RuseOrdAmt', 'AcntNm', 'IsuNm']
        ]

    }
    return ht[trCode] if trCode in ht else ""


def parseTrFunction(trCode):

    ht = {
        "t1485":  funcs.t1485
        , "t1511":  funcs.t1511
        , "t1603":  funcs.t1603
        , "t1662":  funcs.t1662
        , "t1921":  funcs.t1921
        , "t1926":  funcs.t1926
        , "t1927":  funcs.t1927
        , "t2201":  funcs.t2201
        , "t2203":  funcs.t2203
        , "t2301":  funcs.t2301
        , "t2405":  funcs.t2405
        , "t2804":  funcs.t2804
        , "t2805":  funcs.t2805
        , "t2813":  funcs.t2813
        , "t2814":  funcs.t2814
        , "t2832":  funcs.t2832
        , "t2833":  funcs.t2833
        , "t2835":  funcs.t2835
        , "t3102":  funcs.t3102
        , "t3202":  funcs.t3202
        , "t3320":  funcs.t3320
        , "t3518":  funcs.t3518
        , "t8408":  funcs.t8408
        , "t8409":  funcs.t8409
        , "t8412":  funcs.t8412
        , "t8413":  funcs.t8413
        , "t8414":  funcs.t8414
        , "t8415":  funcs.t8415
        , "t8416":  funcs.t8416
        , "t8417":  funcs.t8417
        , "t8418":  funcs.t8418
        , "t8419":  funcs.t8419
        , "t8424":  funcs.t8424
        , "t8428":  funcs.t8428
        , "t8429":  funcs.t8429
        , "t8430":  funcs.t8430
        , "t9943":  funcs.t9943
        , "t9944":  funcs.t9944
    }
    return ht[trCode] if trCode in ht else ""


def parseTrArgsList(trCode):

    ht = {
        "t1485":  ["tday"]
        , "t1511":  ["tday"]
        , "t1603":  ["tday"]
        , "t1662":  ["tday"]
        , "t1921":  ["shcode"]
        , "t1926":  ["shcode", "tday"]
        , "t1927":  ["shcode", "sdate", "edate"]
        , "t2201":  ["focode", "tday"]
        , "t2203":  ["opcode"]
        , "t2301":  ["yyyymm"]
        , "t2405":  ["focode"]
        , "t2804":  ["cmecode", "tday"]
        , "t2805":  ["cmecode"]
        , "t2813":  ["tday"]
        , "t2814":  ["sdate", "edate"]
        , "t2832":  ["opcode", "tday"]
        , "t2833":  ["opcode"]
        , "t2835":  ["yyyymm"]
        , "t3102":  ["sNewsno"]
        , "t3202":  ["shcode", "tday"]
        , "t3320":  ["shcode"]
        , "t3518":  []
        , "t8408":  ["cmecode", "tday"]
        , "t8409":  ["cmecode", "tday"]
        , "t8412":  ["shcode", "sdate", "edate"]
        , "t8413":  ["shcode", "sdate", "edate"]
        , "t8414":  ["focode", "sdate", "edate"]
        , "t8415":  ["focode", "sdate", "edate"]
        , "t8416":  ["focode", "sdate", "edate"]
        , "t8417":  ["upcode", "sdate", "edate"]
        , "t8418":  ["upcode", "sdate", "edate"]
        , "t8419":  ["upcode", "sdate", "edate"]
        , "t8424":  []
        , "t8427":  ["fo_gbn", "yyyy", "mm", "cp_bgn", "actprice", "focode", "dt_gbn", "min_term"]
        , "t8428":  ["sdate", "edate"]
        , "t8429":  ["opcode", "tday"]
        , "t8430":  []
        , "t9943":  []
        , "t9944":  []
    }
    return ht[trCode] if trCode in ht else ""


def retFutCode(yyyy, mm):
    year = {
        "2020": 'Q'
        , "2021": 'R'
        , "2022": 'S'
        , "2023": 'T'
        , "2024": 'U'
        , "2025": 'V'
        , "2026": 'W'
        , "2027": 'X'
        , "2028": 'Y'
        , "2029": 'Z'
        , "2030": 'A'
    }
    month = {
        "1": '1'
        , "2": '2'
        , "3": '3'
        , "4": '4'
        , "5": '5'
        , "6": '6'
        , "7": '7'
        , "8": '8'
        , "9": '9'
        , "10": 'A'
        , "11": 'B'
        , "12": 'C'
    }
    returnCode = year[yyyy] + month[mm]

    return returnCode


def holidayList(today):
    isHoliday = funcs.isHolidayTrue(today)

    ht = {
        "20200415": 'holiday'
        , "20200430": 'holiday'
        , "20200501": 'holiday'
        , "20200505": 'holiday'
        , "20200817": 'holiday'
        , "20200930": 'holiday'
        , "20201001": 'holiday'
        , "20201002": 'holiday'
        , "20201009": 'holiday'
        , "20201225": 'holiday'
    }
    # 공휴일 리스트에 존재하는 경우
    if today in ht:
        return True
    # 토, 일요일인 경우
    if isHoliday is True:
        return True
        # ht[today] = 'holiday'

    return True if today in ht else False


def expirationList(today):
    ht = {
        "20200910": 'expiration'
        , "20201008": 'expiration'
        , "20201112": 'expiration'
        , "20201210": 'expiration'
        , "20210114": 'expiration'
        , "20210218": 'expiration'
        , "20210311": 'expiration'
        , "20210408": 'expiration'
        , "20210513": 'expiration'
    }
    return True if today in ht else False


def odrParam(isuNo, ordQty, ordPrc, bnsTpCode, ordprcPtnCode):
    """
    정규장 현물 주문 오브젝트
    :param isuNo:
    :param ordQty:
    :param ordPrc:
    :param bnsTpCode:
    :param ordprcPtnCode:
    :return:
    """
    obj = {
        "IsuNo": isuNo
        , "OrdQty": ordQty
        , "OrdPrc": ordPrc
        , "BnsTpCode": bnsTpCode
        , "OrdprcPtnCode": ordprcPtnCode
    }
    return obj

'''
IsuNo = '001510'
OrdQty = '1'
OrdPrc = '0'
BnsTpCode = '2'
OrdprcPtnCode = '03'
'''
'''
t2301OutBlock
histimpv:   역사적 변동성,      long, 4
jandatecnt: 옵션 잔존일,        long, 4
cimpv:      콜옵션대표 IV,      float, 6.3
pimpv:      풋옵션대표 IV,      float, 6.3
gmprice:    근월물현재가,       float, 6.2
gmsign:     근월물전일대비구분,  string, 1
gmchange:   근월물전일대비,     float, 6.2
gmdiff:     근월물등락율,       float, 6.2
gmvolume:   근월물거래량,       long, 12
gmshcode:   근월물선물코드,     string, 8

t2301OutBlock1
t2301OutBlock2
actprice:   행사가,            float, 6.2
optcode:    옵션코드,          string, 8
price:      현재가,            float, 6.2
sign:       전일대비구분,       string, 1 
change:     전일대비,           float, 6.2
diff:       등락율,            float, 6.2
volume:     거래량,            long,  12
iv:         IV,                float, 6.2
mgjv:       미결제약정,         long, 12
mgjvupdn:   미결제약정증감,      long, 12
delt:       델타,              float, 6.4
gama:       감마,              float, 6.4
vega:       베가,              float, 6.4
ceta:       세타,              float, 6.4
rhox:       로우,              float, 6.4
theoryprice: 이론가,           float, 6.2
impv:       내재가치,           float, 6.2
timevl:     시간가치,           float, 6.2
open:       시가,             float, 6.2
high:       고가,             float, 6.2
low:        저가,             float, 6.2
atmgubun:   ATM 구분,         string, 1
jisuconv:   지수환산,           float, 6.2
value:      거래대금,           float, 12
'''
