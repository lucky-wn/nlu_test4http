# -*- coding: utf-8 -*-
import datetime
import json
import time
import requests
from .judge import JudgeDir


class SendRequest(object):
    def __init__(self, envir, data, car_type):
        self.jd = JudgeDir()
        self._url = self.jd.judge_which_url(envir)
        print("当前测试环境是：", self._url)
        self._data = data
        self._car_type = car_type

    def request(self, query):
        re_headers = {"carType": self._car_type}
        raw_json = ""
        # status_code = -1
        """ 若未取到response结果, 尝试10次进行结果请求 """
        for i in range(0, 10):
            if raw_json:
                #if status_code == 200:
                break
            try:
                raw_json = requests.post(self._url, json=self._get_nlu_json_data(query), timeout=10).json()
            except Exception as e:
                print("\n\n\n" + str(e) + "\n\n\n")
                raw_json = ""

        return raw_json

    """ 拼凑请求参数的json数据 """
    def _get_qa_json_data(self, query):
        time_stamp = str(int(time.mktime(datetime.datetime.now().timetuple()) * 1000))
        json_data = json.loads(self._data)
        json_data['q'] = query
        json_data['timestamp'] = time_stamp
        return json_data

    def _get_nlu_json_data(self, query):
        json_data = json.loads(self._data)
        json_data['query'] = query
        json_data['carType'] = self._car_type
        return json_data

