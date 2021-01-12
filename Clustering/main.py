from morpheme import parse2df
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
from sklearn import mixture, cluster
from sklearn.model_selection import GridSearchCV
from sklearn import model_selection
from sklearn.cluster import AffinityPropagation
from getname import GetNameJ

keyword = input('キーワード: ')
df = parse2df(keyword)
doc = [" ".join(df['原型'])]
vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
vec = vectorizer.fit_transform(doc)

import json
path_open = open('path_clustering.json', 'r')
paths = json.load(path_open) 
docs=[]
for path in paths.values():
    df = pd.read_csv(path)
#     print(df.columns)
    words = " ".join(df['原型'])
    docs.append(words)
#     print(path)
vecs = vectorizer.fit_transform(docs)

gmm = AffinityPropagation(random_state=0).fit_predict(vecs.toarray())  #最初の４文書をクラスタリング
lis = []
for doc, cls in zip(paths.keys(), gmm):
#     print(cls, GetNameJ(doc))
    if GetNameJ(doc) is None:
        continue
    lis.append((cls, GetNameJ(doc)))

lis.sort()
print(lis)