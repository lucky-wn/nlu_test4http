# -*- coding: utf-8 -*-
import sys
import pandas as pd
import numpy as np


class ExpectResult(object):
    def __init__(self, set, sheets):
        self.set = set

        self._query_tag = 'Query'
        self._er_domain_tag = '预期Domain'
        self._er_intent_tag = '预期Intent'
        self._er_tts_tag = '预期tts'
        self._er_slot_tag = '预期Slot'
        self._er_feature_tag = 'Feature'
        self._er_tts_tag = '预期TTS'

        self.sheets = sheets
        self.cases = self._load_cases()

    """ 加载测试集数据 """
    def _load_cases(self):
        if not isinstance(self.sheets, list):
            print("输入有误：请查看配置文件<SHEET>项, 格式为***或者***,***")
            sys.exit()
        return {sheet: pd.read_excel(self.set, sheet_name=sheet, engine='openpyxl') for sheet in self.sheets}

    """ 取得需要测试的query """
    def get_query_lists(self, sheet_name):
        return self.cases[sheet_name][self._query_tag]

    """ 取得预期domain """
    def get_er_domain_lists(self, sheet_name):
        return self.cases[sheet_name][self._er_domain_tag]

    """ 取得预期intent """
    def get_er_intent_lists(self, sheet_name):
        return self.cases[sheet_name][self._er_intent_tag]

    """ 取得预期tts """
    def get_er_tts_lists(self, sheet_name):
        return self.cases[sheet_name][self._er_tts_tag]

    """ 取得预期slot """
    def get_er_slot_lists(self, sheet_name):
        return self.cases[sheet_name][self._er_slot_tag]

    """ 取得预期feature """
    def get_er_feature_lists(self, sheet_name):
        return self.cases[sheet_name][self._er_feature_tag]



