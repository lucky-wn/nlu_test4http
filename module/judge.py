# -*- coding: utf-8 -*-
import os
import sys
from configLoad import ConfigParser

conf = ConfigParser()
TRUE_TAG = "true"
FALSE_TAG = "false"


class JudgeDir(object):
    def __init__(self):
        self.test_url, self.pre_url, self.body, self.test_type = self.judge_test_type()

    """ 判定文件夹是否存在, 不存在需要创建 """
    def judge_dir_exists(self, *args):
        [os.mkdir(path) for path in args if not os.path.exists(path)]

    """ 通过测试类型, 判断当前是QA还是NLU测试 """
    def judge_test_type(self):
        if conf.qa_test.lower() == TRUE_TAG:
            test_url = conf.qa_test_url
            pre_url = conf.qa_pre_url
            body = conf.qa_body
            test_type = 'qa'
        elif conf.nlu_test.lower() == TRUE_TAG:
            test_url = conf.nlu_test_url
            pre_url = conf.nlu_pre_url
            body = conf.nlu_body
            test_type = 'nlu'
        else:
            print("请查看测试类型")
            sys.exit()

        return test_url, pre_url, body, test_type

    """ 判定是测试环境还是预发布环境 """
    def judge_which_url(self, envir):
        if envir.lower() == 'test':
            return self.test_url
        elif envir.lower() == 'pre':
            return self.pre_url
        else:
            print("您输入有误,请检查配置文件<ENVIRONMENT>")
            sys.exit()


if __name__ == "__main__":
    jd = JudgeDir()

