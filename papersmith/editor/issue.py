# -*- coding: utf-8 -*-

class Issue:
    '用于后端内部的数据通信'
    
    def __init__(self, category, itype, start, end, replacement, exp_id):
        '''
        category:       1拼写/2语法/3语义/4句式
        itype:          issue 类型：1错误/2建议/3普通；
        start:          起始下标，列表
        end:            终止下标，列表
        replacement:    替换成的字符串
        exp_id:         解释的编号
        '''
        self.category = category
        self.itype = itype
        self.start = start
        self.end = end
        self.replacement = replacement
        self.exp_id = exp_id

    def print(self):
        '用于调试打印'
        if self.category == 1:      print('spelling', end = ', ')
        elif self.category == 2:    print('grammar', end = ', ')
        elif self.category == 3:    print('semantic', end = ', ')
        elif self.category == 4:    print('sentence', end = ', ')
        else:                       print('unknown category', end = ', ')

        if self.itype == 1:      print('error', end = ', ')
        elif self.itype == 2:    print('suggestion', end = ', ')
        elif self.itype == 3:    print('info', end = ', ')
        else:                    print('unknown type', end = ', ')

        print(str(self.start) + ' to ' + str(self.end), end = ', ')
        print(self.replacement, end = ', ')
        print(self.exp_id)

    def export(self, index=None):
        '生成字典，用于输出 JSON'
        obj = {
            'cat': self.category,
            'type': self.itype,
            'start': self.start,
            'end': self.end,
            'rep': self.replacement,
            'eid': self.exp_id
        }
        if index is not None:
            obj['id'] = index
        return obj
