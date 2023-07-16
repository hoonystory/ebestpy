from src.model.model import model


class Transaction:
    """
    common transaction request class
    tr_code:
    field_info:
    in_block_values:
    receiver:
    """
    tr_code = None
    receiver = None
    field_info = None
    in_block_values = []

    def __init__(self, tr_code):
        self.set_field_info(tr_code)
        pass

    def set_field_info(self, tr_code):
        self.tr_code = tr_code
        self.field_info = model.get(tr_code)
        # tr_code_field_list = model.get(tr_code)
        # if tr_code_field_list is not None:
        #     self.field_info = tr_code_field_list
            # self.field_info['in'] = tr_code_field_list.get('in')
            # self.field_info['out'] = [
            #     tr_code_field_list.get('out1'),
            #     tr_code_field_list.get('out2')
            # ]
        # else:
        #     pass

    def set_in_block_values(self, parameter_array):
        for i in parameter_array:
            self.in_block_values.append(parameter_array[i])

    def get_result_from_query(self):
        self.receiver.query(self.tr_code
                            , self.field_info.get('in')
                            , self.field_info.get('out')
                            , self.in_block_values)
