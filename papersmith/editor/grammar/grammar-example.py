# -*- coding: utf-8 -*-

from papersmith.editor.issue import Issue
from papersmith.editor.coref.coref import coref
def check(content):
    '样例：检查内容中的语法错误'

    # do something with the content, which is a string
    cordinates=coref(content)
    startlist=[]
    endlist=[]
    issues=[]
    for lists in cordinates:
        for cor in lists:
            startlist.append(cor[0])
            endlist.append(cor[1])
        issue = Issue(3, 2, startlist,endlist, '', 3)
        startlist=endlist=[]
        # Issue(category, itype, start(list), end(list), replacement, exp_id), 参见 ../issue.py

    print(issues)
    return issues # List of issues
