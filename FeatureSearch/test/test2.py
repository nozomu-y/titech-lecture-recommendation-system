import feature_search
'''

fs = feature_search.feature_search() 
fs.get_features() #標準入力から特徴量を取得

subject_codes = fs.get_subject_codes() #取得した特徴量をもとに検索を行い、科目コードを取得

for i in range(len(subject_codes)):
    print(str(i) + ":" + subject_codes[i])
'''
fs = feature_search.feature_search()
for i in range(len(fs.course)):
    print('"' + fs.course[i] + '",')