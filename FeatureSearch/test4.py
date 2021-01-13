import json
from collections import defaultdict

f = open("../DataCollection/syllabus_2020.json")
d = json.load(f)
subject_codes = []
for i in range(len(d)):
    if d[i]["開講元"] == "情報工学系":
        subject_codes.append(d[i]["科目コード"])
        #nums = list(range(len(d)))#出力するdのindex
index_dict = defaultdict(int)#各科目コードとindexの対応表
for i in range(len(d)):
    index_dict[d[i]["科目コード"]]=i

initnums = []
for x in subject_codes:
    initnums.append(index_dict[x])
    nums = initnums
print("init")
print(nums)