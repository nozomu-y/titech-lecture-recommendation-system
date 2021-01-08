import json
path_open = open('path_clustering.json', 'r')
paths = json.load(path_open)

from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd 
docs=[]

for path in paths.values():
    df = pd.read_csv(path)
#     print(df.columns)
    words = " ".join(df['原型'])
    docs.append(words)
#     print(path)



vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
vecs = vectorizer.fit_transform(docs)

"""
df1 = pd.DataFrame(vecs.toarray(),columns=vectorizer.get_feature_names())
df1["book"]=list(paths.keys())
df1 = df1.set_index("book")
print(df1)
"""


"""
from sklearn.metrics.pairwise import cosine_similarity
print(cosine_similarity(vecs))

#行/列に書籍名をラベリングしたDataFrameに変換
df2 = pd.DataFrame(cosine_similarity(vecs),columns = list(paths.keys()))
df2["book"]=list(paths.keys())
df2 = df2.set_index("book")

print(df2)
"""

from sklearn import mixture, cluster
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn import model_selection
from sklearn.cluster import AffinityPropagation

from getname import GetNameJ

# gmm = mixture.BayesianGaussianMixture(n_components=10).fit_predict(vecs.toarray())
gmm = AffinityPropagation(random_state=0).fit_predict(vecs.toarray())  #最初の４文書をクラスタリング
lis = []
for doc, cls in zip(paths.keys(), gmm):
#     print(cls, GetNameJ(doc))
    if GetNameJ(doc) is None:
        continue
    lis.append((cls, GetNameJ(doc)))

lis.sort()
print(lis)
    