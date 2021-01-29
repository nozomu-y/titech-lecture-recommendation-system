import json
import feature_search as fsearch

f = open("../DataCollection/syllabus_2020.json")
d = json.load(f)
subject_codes = []
for i in range(len(d)):
    if d[i]["開講元"] == "情報工学系":
        subject_codes.append(d[i]["科目コード"])
    
######feature_searchクラスは以下のように使う#######
fs = fsearch.feature_search(subject_codes)  #科目コードのリストを渡してインスタンス作成
fs.get_features()                   #検索条件（特徴量を取得)
fs.print_result()                   #結果を出力
###############################################