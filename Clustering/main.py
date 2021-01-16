import json
from morpheme import parse2df
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
#  from sklearn import mixture, cluster
#  from sklearn.model_selection import GridSearchCV
#  from sklearn import model_selection
from sklearn.cluster import AffinityPropagation
from getname import GetNameJ

keyword = input('キーワード: ')

#########ワードネット#############
split_words = keyword.split()
similar_words = split_words.copy()
for word in split_words:
#     print(word)
    tmp = SearchSimilarWords(word)
    for tmp_word in tmp:
        similar_words.append(tmp_word)
#     print(similar_words)
# print(similar_words)
for word in similar_words:
    keyword += word+" "
# print(keyword)
################################

vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')

path_open = open('path_clustering.json', 'r')
paths = json.load(path_open)
train_docs = []
train_codes = []
for lec_code, path in paths.items():
    train_df = pd.read_csv(path)
    train_words = " ".join(train_df['原型'].dropna(how='all'))
    train_docs.append(train_words)
    train_codes.append(lec_code)
train_vecs = vectorizer.fit_transform(train_docs)

test_df = parse2df(keyword)
test_docs = [" ".join(test_df['原型'].dropna(how='all'))]
test_vecs = vectorizer.transform(test_docs)

gmm = AffinityPropagation(random_state=0).fit(train_vecs.toarray())
train_predict = gmm.predict(train_vecs.toarray())
test_predict = gmm.predict(test_vecs.toarray())

similar_lectures = []
for index, lecture in enumerate(train_predict):
    if lecture == test_predict[0]:
        similar_lectures.append(train_codes[index])

for lecture in similar_lectures:
    print(GetNameJ(lecture))
