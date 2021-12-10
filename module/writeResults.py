# -*- coding: utf-8 -*-
import os

import pandas as pd


class SaveExcle(object):
    def __init__(self, file):
        self._result_file = file
       # self._pass_style =

    def save_excle(self, data_list, titles, sheet_name):
        """ 将测试结果写入excle文件 """
        if not os.path.isfile(self._result_file):
            pd.DataFrame(data=data_list, columns=titles).to_excel(self._result_file, index=False, sheet_name=sheet_name)
        else:
            with pd.ExcelWriter(self._result_file, mode='a', engine='openpyxl') as writer:
                pd.DataFrame(data=data_list, columns=titles).to_excel(writer, sheet_name=sheet_name, index=False)
