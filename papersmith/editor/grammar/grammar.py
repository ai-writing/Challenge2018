# -*- coding: utf-8 -*-

from papersmith.editor.issue import Issue
from papersmith.editor.grammar.articleCheck.src.test.articleCheck import *
from papersmith.editor.grammar import single_three
from papersmith.editor.grammar import tense


#djl
def checkTense(content):
    suggests=tense.tensecheck(verse)
    issuesOfArticle = []
    for i in suggests:
        issue = Issue(2, 2, [i[0]], [i[1]], i[2], 1)
        issuesOfArticle.append(issue)
    return issuesOfArticle
    

# ht
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


# gjy
def checkThirdPersonSingular(content):
    res = single_three.check(content)
    issues = []
    for sentence_entries in res:
        for entry in sentence_entries:
            le = entry[0]
            ri = entry[1]
            rep = entry[2]
            issue = Issue(1, 1, [le], [ri], rep, 4)
            issues.append(issue)
    return issues


def check(content):
    '检查内容中的语法错误'

    issues = []
    issues += checkArticle(content)
    issues += checkThirdPersonSingular(content)
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
