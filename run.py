# -*- coding: utf-8 -*-
from configLoad import ConfigParser
from module.judge import JudgeDir
from module.parser import Parser


if __name__ == '__main__':
    conf = ConfigParser()
    jd = JudgeDir()
    jd.judge_dir_exists(conf.result, conf.cases)
    parser = Parser(conf, jd.body)

    if conf.nlu_test.lower() == 'true':
        """ NLU接口测试 """
        #parser.run_parser_nlu()
        parser.run_process()
        parser.get_final_result()
    elif conf.qa_test.lower() == "true":
        """ QA接口测试 """
        parser.run_parser_qa()