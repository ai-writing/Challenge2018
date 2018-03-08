# -*- coding: utf-8 -*-

from papersmith.editor.issue import Issue

def check(content):
    '样例：检查内容中的语法错误'

    # do something with the content, which is a string

    issue = Issue(1, 1, [15], [19], 'replacement', 3)
        # Issue(category, itype, start(list), end(list), replacement, exp_id), 参见 ../issue.py

    issues = [issue]

    return issues # List of issues
