import json
from morpheme import parse2df
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
#  from sklearn import mixture, cluster
#  from sklearn.model_selection import GridSearchCV
#  from sklearn import model_selection
from sklearn.cluster import AffinityPropagation
from getname import GetNameJ
from wordnet import SearchSimilarWords

keyword = input('キーワード: ')

#########ワードネット#############
# split_words = keyword.split()
# similar_words = split_words.copy()
# for word in split_words:
# #     print(word)
#     tmp = SearchSimilarWords(word)
#     if tmp == None:
#         continue
#     for tmp_word in tmp:
#         similar_words.append(tmp_word)
# #     print(similar_words)
# # print(similar_words)
# for word in similar_words:
#     keyword += word+" "
# # print(keyword)
################################

# vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')

# path_open = open('path_clustering.json', 'r')
# paths = json.load(path_open)
# train_docs = []
# train_codes = []
# for lec_code, path in paths.items():
#     train_df = pd.read_csv(path)
#     train_words = " ".join(train_df['原型'].dropna(how='all'))
#     train_docs.append(train_words)
#     train_codes.append(lec_code)
# train_vecs = vectorizer.fit_transform(train_docs)

vec = pd.read_pickle('pkl/vec.pkl')
vectorizer = pd.read_pickle('pkl/vectorizer.pkl')
train_vecs = vec

test_df = parse2df(keyword)
test_docs = [" ".join(test_df['原型'].dropna(how='all'))]
test_vecs = vectorizer.transform(test_docs)

# gmm = AffinityPropagation(random_state=0).fit(train_vecs.toarray())
# train_predict = gmm.predict(train_vecs.toarray())
# test_predict = gmm.predict(test_vecs.toarray())

clusters = pd.read_pickle('pkl/clusters.pkl')
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
# clf = make_pipeline(StandardScaler(), SGDClassifier(max_iter=1000, tol=1e-3))
clf = SGDClassifier(max_iter=1000, tol=1e-3, random_state=1)
clf.fit(train_vecs, clusters)
test_predict = clf.predict(test_vecs)
train_predict = clf.predict(train_vecs)
print(test_predict)
print(train_predict)
print(clusters)
import json
path_open = open('path_clustering.json', 'r')
paths = json.load(path_open)

simlec = []
# for index, cluster in enumerate(clusters):
#     if test_predict[0] == cluster:
#         simlec.append(list(paths.keys())[index])

# similar_lectures = []
for doc, cls in zip(paths.keys(), clusters):
    if test_predict[0] == cls:
        print(doc)
        simlec.append(GetNameJ(doc))
    

# for index, lecture in enumerate(train_predict):
#     if lecture == test_predict:
#         similar_lectures.append(train_codes[index])

for lecture in simlec:
    print(lecture)
