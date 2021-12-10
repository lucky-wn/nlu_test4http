# -*- coding: utf-8 -*-
import json
import pandas as pd
PASS_TAG = "PASS"
FAIL_TAG = "FAIL"


class CompareResult(object):
    def get_result_tag(self, res):
        if res:
            return PASS_TAG
        else:
            return FAIL_TAG

    """ 比较domain的值 """
    def cmp_domain(self, tr_domain, er_domain):
        er_domain = "" if pd.isnull(er_domain) else er_domain
        return str(tr_domain).lower().replace(" ", "") == str(er_domain).lower().replace(" ", "")

    """ 比较intent的值 """
    def cmp_intent(self, tr_intent, er_intent):
        er_intent = "" if pd.isnull(er_intent) else er_intent
        """ music的校正规则 """
        music_corr_play = ["music_control_play", "music_random_play"]
        music_cor_close = ["music_control_pause", "music_control_close"]
        music_cor_unclear = ["music_control_resume", "music_control_unclear"]

        intent_cmp = str(tr_intent).strip().lower().replace(" ", "") == str(er_intent).strip().lower().replace(" ", "")
        if not intent_cmp:
            tr_intent = tr_intent.lower().replace(" ", "")
            if any([tr_intent in music_corr_play, tr_intent in music_cor_close, tr_intent in music_cor_unclear]):
                return True

        return intent_cmp

    def cmp_tts(self, tr_tts, er_tts):
        return str(tr_tts).strip().lower().replace(" ", "").replace("\n", "") == str(er_tts).strip().lower().replace(" ", "").replace("\n", "")

    def cmp_slot(self, tr_slot, er_slot):
        """ 1.比较slot的时候, 实际可以比预期多, 但不能比预期的slot内容少 """

        er_slot = {} if pd.isnull(er_slot) else json.loads(er_slot)
        if len(tr_slot) < len(er_slot):
            return False

        for ek, ev in er_slot.items():
            """ 2.实际中不包含预期的key内容 """
            if isinstance(tr_slot, str):
                tr_slot = eval(tr_slot)
            if ek.lower().strip().replace(" ", "") not in [tk.lower().strip().replace(" ", "") for tk in tr_slot.keys()]:
                return False
            else:
                """ 3. 实际value不在预期中, slot判定失败 """
                if tr_slot[ek].lower().strip().replace(" ", "") not in [va.strip().replace(" ", "").lower() for va in ev.split("|")]:
                    return False
        return True