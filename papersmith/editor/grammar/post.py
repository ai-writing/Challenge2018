#encoding:utf-8
#注意!没做nounflag.需要的去reader.py取

import numpy as np
import word2vec
import re
import time
import os
import pickle
import random
import requests
import json
from queue import Queue
#bug:shorten和shorten_front不一样的话,每一遍都得重新计算而不是直接从队列里拿出来!

a="Designing cooling channels for the thermoplastic injection process is a very important step in mold design."
url = 'http://166.111.139.15:9000'
params = {'properties' : r"{'annotators': 'tokenize,ssplit,pos,depparse', 'outputFormat': 'json'}"}
while True:
    try:
        #print('0')
        resp = requests.post(url,a,params=params).text
        content=json.loads(resp)
        #print('1')
        break
    except Exception as e:
        if e!=KeyboardInterrupt:
            print('error...')
        else:
            raise KeyboardInterrupt
for sentence in content['sentences']:
    for i in sentence['enhancedPlusPlusDependencies']:
            print('out',i)
#                for j in i:
                #print(i)
                #input()
#                        print(posdict)
#                           print(':\n',a,posdict[i['governor']]+1)
