
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
def lemma(self,verb):
    if verb in self.ldict:
        return self.ldict[verb]
    else:
        params = {'properties' : r"{'annotators': 'lemma', 'outputFormat': 'json'}"}
        resp = requests.post(self.url, verb, params=params).text
        content=json.loads(resp)
        word=content['sentences'][0]['tokens'][0]['lemma']
        print('errverb',verb)
        self.ldict[verb]=word
        return word


with open('tense/verbset', 'rb') as f:
    self.verbset = pickle.load(f)
