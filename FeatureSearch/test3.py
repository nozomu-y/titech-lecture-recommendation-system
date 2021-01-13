import feature_search

subject_codes = []

fs = feature_search()
fs.make_init_index_list()
fs.get_features()
index_list = fs.get_index_list()
print("----------該当講義一覧----------")
for x in index_list:
    print(fs.d[x]["講義名"]["日本語"])
    # print(fs.d[x]["科目コード"])
print("--------------------------------")
