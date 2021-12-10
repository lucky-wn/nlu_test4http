# -*- coding: utf-8 -*-
import os
import time
import threading
from constant import process
from .expectResult import ExpectResult
from .sendRequest import SendRequest
from .cmpResult import CompareResult
from .testResult import TestResult
from .writeResults import SaveExcle
from .countResult import CountResult
from multiprocessing import Process, Queue, Pool

TIME_STAMP = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime(time.time()))
QA_RES_TITLE = ["Feature", "Query", "实际Domain", "实际Intent", "预期TTS", "实际TTS", "TTS结果", "Response"]
NLU_RES_TITLE = ["Feature", "Query", "预期Domain", "实际Domain", "Domain结果", "预期Intent", "实际Intent", "Intent结果",
                 "预期Slot", "实际Slot", "Slot结果", "Result", "Response"]
NLU_COUNT_TITLE = ["Feature", "DomainFAIL", "DomainPASS", "DomainSUM", "DomainPassRate", "Inten_FAIL", "IntentPASS",
                   "IntentSUM", "IntentPassRate", "SlotFAIL", "SlotPASS", "SlotSUM", "SlotPassRate"]


def query(sr, tr, query_list, filename):
    query_length = len(query_list)
    count = 0
    file = open(process + filename, "w", encoding="utf8")
    # query: [1, '字体设为精致']
    for idx, ql in enumerate(query_list):
        print("> 当前进程: %s, Query:%s, Index：%s, 测试进度：%.2f%%" % (filename, ql, idx, idx/query_length * 100))
        response = sr.request(ql[1])
        tr_domain, tr_intent, tr_slot = tr.get_nlu_results(response)
        file.write(str(ql[0]) + "##" + ql[1] + "##" + tr_domain + "##" + tr_intent + "##" + str(tr_slot) + "##" + str(response) + "\n")
    file.close()


class Parser(object):
    def __init__(self, conf, body):
        result_file = os.path.join(conf.result, "Result_{0}_{1}_{2}.xlsx".format(conf.excle.replace(".xlsx", ""), conf.sheet, TIME_STAMP))
        self.sheet = conf.sheet
        self.er = ExpectResult(conf.path_set, conf.sheet)
        self.sr1 = SendRequest(conf.envir, body, conf.car_type)
        self.sr2 = SendRequest(conf.envir, body, conf.car_type)
        self.sr3 = SendRequest(conf.envir, body, conf.car_type)
        self.cmp = CompareResult()
        self.tr1 = TestResult()
        self.tr2 = TestResult()
        self.tr3 = TestResult()
        self.wr = SaveExcle(result_file)
        self.cr = CountResult()
        self.all_querys = []
        for sheet in self.sheet:
            for index, query in enumerate(self.er.get_query_lists(sheet)):
                self.all_querys.append([index, query])

    def run_process(self):
        pool = Pool(processes=3)
        for i in range(3):
            a = self.all_querys[len(self.all_querys) // 3 * i: len(self.all_querys) // 3 * (i + 1)]
            pool.apply_async(query, (eval("self.sr%s"%(i+1)), eval("self.tr%s"%(i+1)), a, str(i) + ".txt",))
        pool.close()
        pool.join()

    def get_final_result(self):
        res = []
        assort_lists = {}
        q_result = []
        with open(process + "0.txt", "r", encoding="utf8") as file:
            for line in file.readlines():
                q_result.append(line.replace("\n", "").split("##"))
        with open(process + "1.txt", "r", encoding="utf8") as file:
            for line in file.readlines():
                q_result.append(line.replace("\n", "").split("##"))
        with open(process + "2.txt", "r", encoding="utf8") as file:
            for line in file.readlines():
                q_result.append(line.replace("\n", "").split("##"))

        sheet = self.sheet[0]
        for qq in q_result:
            index = int(qq[0])
            query = qq[1]
            tr_domain, tr_intent, tr_slot = qq[2], qq[3], qq[4]
            print("{0} 当前QUERY : {1}, 实际: {2} - {3} - {4}".format(index, qq[1], tr_domain, tr_intent, tr_slot))
            er_domain = self.er.get_er_domain_lists(sheet)[index]
            er_intent = self.er.get_er_intent_lists(sheet)[index]
            er_slot = self.er.get_er_slot_lists(sheet)[index]
            er_feature = self.er.get_er_feature_lists(sheet)[index]

            domain_res = self.cmp.get_result_tag(self.cmp.cmp_domain(tr_domain, er_domain))
            intent_res = self.cmp.get_result_tag(self.cmp.cmp_intent(tr_intent, er_intent))
            slot_res = self.cmp.get_result_tag(self.cmp.cmp_slot(tr_slot, er_slot))
            result = self.cmp.get_result_tag(domain_res == intent_res == slot_res == "PASS")
            res.append([er_feature, query, er_domain, tr_domain, domain_res, er_intent, tr_intent, intent_res,
                        er_slot, tr_slot, slot_res, result, qq[5]])

            self.cr.category_assort(er_feature, assort_lists, domain_res, intent_res, slot_res)

        self.wr.save_excle(res, NLU_RES_TITLE, sheet)
        self.wr.save_excle(self.cr.statistics(assort_lists), NLU_COUNT_TITLE, "统计结果")




