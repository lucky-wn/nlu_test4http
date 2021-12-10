# -*- coding: utf-8 -*-


class CountResult(object):
    def category_assort(self, category, res={}, *args):
        if category in res.keys():
            [res[category][index].append(v) for index, v in enumerate(args)]
        else:
            res.setdefault(category, [])
            [res[category].append([v]) for v in args]

        return res

    def statistics(self, assort_dict):
        count_result = []

        col = 0
        for k, result in assort_dict.items():
            count_result.append([k])
            """ FAIL, PASS, SUM, PASS_RATE"""
            for index, single in enumerate(result):
                fail_num = single.count("FAIL")
                pass_num = single.count("PASS")
                #if index == 0:
                length = len(single)
                # else:
                #     length = count_result[col][index * 4 - 2]
                pass_rate = '%.2f%%' % (float(pass_num) / float(length) * 100)

                count_result[col].extend([fail_num, pass_num, length, pass_rate])
            col += 1

        # count_result.append(["总计", ])
        print(1111, count_result)
        return count_result











