"""
            InBlock = parseInfield(trCode)
            OutBlock = parseOutfield(trCode)
            InBlockValue = [upcode, gubun]
            receiver.query(trCode, InBlock, OutBlock, InBlockValue, log)
"""


class CommonTxnApi:
    """
    예상지수
    gubun     : string, 1 :   조회구분(1: 장전, 2: 장후)
    """
    tr_code = None
    field_info = {}

    in_block_values = []
    receiver = None

    def __init__(self, tr_code):
        self.tr_code = tr_code
        self.field_info['in'] = ['upcode', 'gubun']
        self.field_info['out'] = [
            ['pricejisu', 'sign', 'change', 'volume',
             'yhighjo', 'yupjo', 'yunchgjo', 'ylowjo', 'ydownjo', 'ytrajo'],
            ['chetime', 'jisu', 'sign', 'change', 'volume', 'volcha']
        ]
        # self.receiver = XAQueryResultHandler.get_instance()

    def set_in_block_values(self, parameter_array):
        for i in parameter_array:
            self.in_block_values.append(parameter_array[i])

    def get_result_from_query(self):
        self.receiver.query(self.tr_code
                            , self.field_info.get('in')
                            , self.field_info.get('out')
                            , self.in_block_values)
