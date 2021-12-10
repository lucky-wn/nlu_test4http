import datetime
import os
from configparser import ConfigParser
import time
import requests
import threading
import pandas as pd
import json

PWD = os.getcwd()

headers = {
    "carType": "D55"
    }


def get_qa_json(text):
    test_json = {
        "q": "帐号管理在哪里",
        "bid": "1",
        "hid": "REV08",
        "lat": 23.159605,
        "lon": 113.38507,
        "vid": "XPENGD55408094130EA0EB2D",
        "vin": "zhangy2",
        "city": "广州",
        "sign": "afb45b8adc38aaf321313a4c8d5b6344",
        "app_v": "V1.1.5.229",
        "model": "8",
        "msgId": "1558420630080 ",
        "app_id": "xmart:appid:002",
        "pre_ts": 1550316751937,
        "status": "start",
        "msgType": "req",
        "pre_cmd": "",
        "speech_v": "2.8.0",
        "timestamp": 1550316755442,
        "active_app": "speech",
        "pre_intent": "navigation_search",
        "active_page": "main",
        "switch_data": "{\"sound_location\":\"1\"}"
        }

    test_json['q'] = text
    tt = str(int(time.mktime(datetime.datetime.now().timetuple()) * 1000))
    test_json['timestamp'] = tt
    return test_json

class NluTester:
    THREAD_NUM = 4

    def __init__(self, domain, car_type, version):
        self._config(car_type, version)
        self.domain = domain
        self.case_sets = self._init_case_set()

    def _config(self, car_type='E28', version='2.7.0'):
        cf = ConfigParser()
        config_file = os.path.join(PWD, 'config.ini')
        cf.read(config_file, encoding='utf-8')
        self._car_type = car_type

        self._version = version
        self._sets = eval(cf.get('NLU', 'SETS'))
        if car_type in {'E28', 'D22', 'D55'}:
            self._url = cf.get('NLU', 'URL_P7')
            self._body = cf.get('NLU', 'BODY_P7').replace('\n', '').replace('version', version).replace('E28', car_type)
        elif car_type in {'D21B'}:
            self._url = cf.get('NLU', 'URL_G3')
            self._body = cf.get('NLU', 'BODY_G3').replace('\n', ''). \
                replace('type', car_type).replace('version', version)

    def _init_case_set(self):
        res = []
        return [pd.read_excel(f'./{s}.xlsx', sheet_name=self.domain, engine='openpyxl') for s in self._sets]

    def _process_query(self, i, q):
        j = 1
        while j < 4:
            tt = str(int(time.mktime(datetime.datetime.now().timetuple()) * 1000))
            # print(11111, self._url, self._body.replace('query', q).replace("TIME_STAMP", tt).encode('utf-8') )
            #raw_json = requests.post(self._url, json=self._body.replace('query', q).replace("TIME_STAMP", tt).encode('utf-8')).json()
            raw_json = requests.post(self._url, json=get_qa_json(q), headers=headers).json()
            print(raw_json)
            try:
                nlu_result = raw_json['data']['data']['answer']
                domain_res = 'None'
                intent_res = 'None'
                if nlu_result:
                    if len(nlu_result[0]) > 0:
                        tts_res = nlu_result[0]['text']
                    if 'semantic' in raw_json['data']['data']:
                        if 'domain' in raw_json['data']['data']['semantic']:
                            domain_res = raw_json['data']['data']['semantic']['domain']
                        if 'intent' in raw_json['data']['data']['semantic']:
                            intent_res = raw_json['data']['data']['semantic']['intent']

                    return int(i), domain_res, intent_res, tts_res, raw_json
            except (KeyError, IndexError):
                print(f'执行失败 {q} {raw_json}')
            return int(i), '', '', '', raw_json
        return int(i), '', '', '', {}

    def _run_batch(self, i, suite, s, e, suite_result, case):
        suite_result.extend(list(suite[s:e]['query'].map(lambda q: self._process_query(i, q))))

    def _run_each_suite(self, case, suite, result):
        print(f'processing {case}...')
        size = suite.shape[0]
        gap = size // self.THREAD_NUM
        suite_result = []
        thread_pool = []
        for i in range(self.THREAD_NUM):
            s, e = gap * i, gap * (i + 1) if i < (self.THREAD_NUM - 1) else size
            thread_pool.append(threading.Thread(target=self._run_batch, args=(i, suite, s, e, suite_result, case)))
        for task in thread_pool:
            task.start()
        for task in thread_pool:
            task.join()
        print(f'process done, reducing...')
        suite_result.sort(key=lambda x: x[0])
        suite.insert(suite.shape[1], 'new_domain', list(map(lambda x: x[1], suite_result)))
        suite.insert(suite.shape[1], 'new_intent', list(map(lambda x: x[2], suite_result)))
        suite.insert(suite.shape[1], 'new_tts', list(map(lambda x: x[3], suite_result)))
        suite.insert(suite.shape[1], 'result', list(map(lambda x: json.dumps(x[-1], ensure_ascii=False), suite_result)))
        # suite.insert(suite.shape[1], 'pass', [s[0] == s[2] and s[1] == s[3] for s in suite[['domain', 'intent', 'new_domain', 'new_intent']].values])
        suite.insert(suite.shape[1], 'pass', [str(s[0]).replace(" ", "") == str(s[1]).replace(" ", "") for s in suite[['tts', 'new_tts']].values])
        # suite = suite[suite['pass'] == False]
        suite.to_excel(result, sheet_name=case, index=False)
        print(f'{case} done!\n')

    def run(self):
        result = pd.ExcelWriter(
            f'./nlu_{self._car_type}_{self._version}_{self.domain}_{time.strftime("%Y-%m-%d", time.localtime())}.xlsx')
        for i, s in enumerate(self.case_sets):
            case_name = self._sets[i].lower().replace('suite', '')
            self._run_each_suite(case_name, s, result)
        result.close()
        self.get_report()

    def get_report(self):
        f = open(f'./report_nlu_{self._car_type}_{self._version}_{self.domain}_{time.strftime("%Y-%m-%d", time.localtime())}.txt', 'w', encoding='UTF-8')
        print('Report:')
        msg = f'\t{"数据集":<15}{"Domain":<15}通过率\t\t未通过数量\t\t用例数'
        f.write(msg + '\n')
        total_pass, total_num = 0, 0
        print(msg)
        for i, s in enumerate(self._sets):
            df = self.case_sets[i]
            num_pass, num_total = df[df['pass']].shape[0], df.shape[0]
            total_pass, total_num = total_pass + num_pass, total_num + num_total
            msg = f'{s:<15}{self.domain:<15}{num_pass / num_total * 100:.2f}%\t\t{num_total - num_pass}\t\t\t{num_total}'
            f.write(msg + '\n')
            print('\t' + msg)
        print()
        conclusion = f'综合通过率: {100 * total_pass / total_num:.2f}%\n综合通过数: {total_pass} / {total_num}'
        print(conclusion)
        f.write(conclusion)
        f.close()


if __name__ == '__main__':
    # car_type = 'E28' / 'D21B' / 'D22'
    # for domain in ['ac', 'control', 'camera', 'charge', 'music', 'gui', 'navigation', 'chat', 'system']:
    #     tester = NluTester(domain=domain, car_type='D22', version='2.8.0')
    #     tester.run()
    """domain可以指定需要测试的sheet, 若为空则依次遍历excle中的每个sheet"""
    tester = NluTester(domain='Sheet1', car_type='D55', version='2.8.0')
    #tester = NluTester(domain='句式一', car_type='D55', version='2.8.0')
    tester.run()
    # tester = NluTester(domain='vui', car_type='E28', version='2.7.0')
    # tester.run()
