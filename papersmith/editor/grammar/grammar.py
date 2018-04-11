# -*- coding: utf-8 -*-

from papersmith.editor.issue import Issue
from papersmith.editor.grammar.articleCheck.src.test.articleCheck import *

def checkArticle(content):
    sets = articleCheck(content)
    issuesOfArticle = []
    for each in sets:
        le = int(each[0])
        ri = int(each[1])
        str = each[2]
        #issue = Issue(1, 1, [15], [19], 'replacement', 3)
        issue = Issue(1, 1, [le], [ri], str, 3)
        issuesOfArticle.append(issue)
    return issuesOfArticle
    return []

def check(content):
    '检查内容中的语法错误'


    issues = []
    issues += checkArticle(content)
    # Issue(category, itype, start(list), end(list), replacement, exp_id), 参见 ../issue.py

    #issues = [issue]
    return issues # List of issues'''

'''def check(content):
    '样例：检查内容中的语法错误'

    # do something with the content, which is a string

    issue = Issue(1, 1, [15], [19], 'replacement', 3)
        # Issue(category, itype, start(list), end(list), replacement, exp_id), 参见 ../issue.py

    issues = [issue]

    return issues # List of issues'''


#check("I am a boy.")
