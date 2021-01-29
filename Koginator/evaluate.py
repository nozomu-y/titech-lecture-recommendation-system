# -*- coding: utf-8 -*-
import sys
import os
import numpy as np
rootFile = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(rootFile)
from Koginator import koginator
from collections import defaultdict

sysFile = os.path.dirname(__file__)
data_file = os.path.normpath(os.path.join(sysFile, './data/testdata.tsv'))
label_file = os.path.normpath(os.path.join(sysFile, './data/testlabel_nm.txt'))
feature_file = os.path.normpath(os.path.join(sysFile, './data/feature_nm.txt'))

testdata = np.loadtxt(data_file, delimiter='\t')   #tsvは'\t'で区切られている
testlabel = open(label_file, 'r', encoding='utf-8').readlines()
for i in range(len(testlabel)):
    testlabel[i] = testlabel[i].rstrip("\n")  #rstrip()文字列の右側から指定した文字列を削除
feature = open(feature_file, 'r', encoding='utf-8').readlines()
for i in range(len(feature)):
    feature[i] = feature[i].rstrip("\n")  #rstrip()文字列の右側から指定した文字列を削除
f_map = defaultdict(str)
for i in range(len(feature)):
    f_map[feature[i]] = i
'''
question = kg.getQuestion()
quest_index = f_map[question]
testans = testdata[4][quest_index]
print(str(int(testans)))
'''
score = 0
N = 0
for i in range(len(testlabel)):
    kg = koginator.koginator()
    while True:
        question = kg.getQuestion()
        quest_index = f_map[question]
        testans = testdata[i][quest_index]
        if(kg.getAnswer(str(int(testans)))):
            break
    
    if testlabel[i] in kg.answer:
        score = score+1
    N = N+1
print('N = ' + str(N) + '\n' + 'score = ' + str(score) + '\n' + 'precision = ' + str(score/N *100.0))
