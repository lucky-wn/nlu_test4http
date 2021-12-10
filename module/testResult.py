# -*- coding: utf-8 -*-
import sys
import re


class TestResult(object):

    """ 取得实际domain """
    def _get_tr_nlu_domain(self, nlu_result):
        try:
            domain = nlu_result['domainName'].strip().replace(" ", "")
        except:
            domain = 'NA'
        # print("domain, ", domain)
        return domain

    """ 取得实际intent """
    def _get_tr_nlu_intent(self, nlu_result):
        try:
            if "intents" not in nlu_result.keys():
                intent = 'NA'
            else:
                nlu_result = sorted(nlu_result.get("intents"), key=lambda x: x["intentConfidence"], reverse=True)
                intent = nlu_result[0]['intentName'].strip().replace(" ", "")
        except:
            intent = "NA"
        # print("intent, ", intent)
        return intent

    """ 取得实际slot """
    def _get_tr_nlu_slot(self, nlu_result):
        res_slot = {}
        try:
            if "intents" not in nlu_result.keys():
                return res_slot
            else:
                nlu_result = sorted(nlu_result.get("intents"), key=lambda x: x["intentConfidence"], reverse=True)

            for slot in nlu_result[0]['slots']:
                key = slot['name'].strip().replace(" ", "")

                """ tpl的情况下, 需要比较pageUrl和packageName """
                if key == 'tpl_name':
                    value = re.findall(r"('pageUrl.*packageName.*')}", slot['value'])[0].replace("'", "")
                else:
                    value = slot['rawvalue']
                    if not value:
                        value = slot['value']

                res_slot[key] = value.strip().replace(" ", "")
        except:
            print("Get Slot Error!!!!!!!!")

        return res_slot

    def get_nlu_results(self, raw_json):
        try:
            nlu_result = raw_json['data']['domains']
            if nlu_result[0]:
                domain = self._get_tr_nlu_domain(nlu_result[0])
                intent = self._get_tr_nlu_intent(nlu_result[0])
                slot = self._get_tr_nlu_slot(nlu_result[0])
        except:
            domain = 'NA'
            intent = 'NA'
            slot = raw_json

        return domain, intent, slot

    def get_tr_qa_results(self, raw_json):
        text = 'NA'
        domain = 'NA'
        intent = 'NA'

        try:
            answer = raw_json['data']['data']['answer']
            text = self.get_tr_text(answer)
        except (KeyError, IndexError):
            print("{0}执行失败：".format(TestResult.__name__), raw_json)

        try:
            semantic = raw_json['data']['data']['semantic']
            domain = self.get_tr_domain(semantic)
            intent = self.get_tr_intent(semantic)

        except (KeyError, IndexError):
            print("{0}执行失败：".format(TestResult.__name__), raw_json)

        return domain, intent, text

    def get_tr_domain(self, seman):
        if "domain" in seman:
            return seman['domain']

    def get_tr_intent(self, seman):
        if "intent" in seman:
            return seman['intent']

    def get_tr_text(self, answer):
        if len(answer[0]) > 0:
            return answer[0]['text'].replace(u'\xa0', u' ')
        else:
            return "NA"
