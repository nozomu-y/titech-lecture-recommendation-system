import getscore
from getname import GetNameJ
import numpy
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import matplotlib.pyplot as plt
import hierarchy_cluster
import getname
from sklearn import model_selection
from sklearn.model_selection import GridSearchCV
import pandas as pd
from sklearn import mixture, cluster
import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
docs = []
path_open = open('path_clustering.json', 'r')
paths = json.load(path_open)
for path in paths.values():
    df = pd.read_csv(path)
    words = " ".join(df['原型'].dropna(how='all'))
    docs.append(words)
vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
vecs = vectorizer.fit_transform(docs)
print('start')
df = pd.DataFrame(vecs.toarray(), columns=vectorizer.get_feature_names())
df["subject"] = list(paths.keys())
df = df.set_index("subject")
gmm = hierarchy_cluster.hierarchy_cluster(df)

print('end')
for i in [1.2,1.7]:
    lis = []
    #  plt.figure(num=None, figsize=(16, 9), dpi=200, facecolor='w', edgecolor='k')
    #  dendrogram(gmm, labels=df.index)
    #  plt.show()
    clusters = fcluster(gmm, i * numpy.average(gmm[:, 2]), criterion='distance')
    pd.to_pickle(clusters, "pkl/clusters"+str(i)+".pkl")
#     for doc, cls in zip(paths.keys(), clusters):
#         lis.append((cls, GetNameJ(doc)))
#     lis.sort()

#     f = open("cluster"+str(i)+".txt","w")
#     for i,sub in lis:
#         f.write(str(i)+" "+sub+"\n")
#     f.close()

    print(max(clusters))
    print(type(clusters))

# pd.to_pickle(,"pkl/train_codes.pkl")
#pd.to_pickle(train_docs, "pkl/train_docs.pkl")
pd.to_pickle(vecs, "pkl/vec.pkl")
# pd.to_pickle(clusters, "pkl/clusters.pkl")
pd.to_pickle(gmm, "pkl/gmm.pkl")
pd.to_pickle(vectorizer, "pkl/vectorizer.pkl")
