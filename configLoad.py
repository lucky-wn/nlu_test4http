# -*- coding: utf-8 -*-
import configparser
import os

PWD = os.getcwd()
CONFIG_FILE = os.path.join(PWD, 'config.ini')


class ConfigParser(object):
    conf = configparser.ConfigParser()
    conf.read(CONFIG_FILE, encoding='utf-8')

    """ 读取配置文件信息 """
    envir = conf.get("CONFIG", "ENVIRONMENT")
    car_type = conf.get("CONFIG", "CAR_TYPE")
    excle = conf.get("CONFIG", "EXCLE")
    sheet = conf.get("CONFIG", "SHEET").split(',')
    qa_test = conf.get("CONFIG", "QA_TEST")
    nlu_test = conf.get("CONFIG", "NLU_TEST")

    """ 读取常量内容 """
    qa_test_url = conf.get("CONSTANT", "QA_TEST_URL")
    qa_pre_url = conf.get("CONSTANT", "QA_PRE_URL")
    qa_body = conf.get("CONSTANT", "QA_BODY")
    nlu_test_url = conf.get("CONSTANT", "NLU_TEST_URL")
    nlu_pre_url = conf.get("CONSTANT", "NLU_PRE_URL")
    nlu_body = conf.get("CONSTANT", "NLU_BODY")

    """ 测试结果路径 """
    cases = os.path.join(PWD, "Cases")
    result = os.path.join(PWD, 'Result')

    path_set = os.path.join(cases, excle)
