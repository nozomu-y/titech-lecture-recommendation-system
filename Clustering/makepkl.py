import json
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
docs=[]
path_open = open('path_clustering.json', 'r')
paths = json.load(path_open)
for path in paths.values():
    df = pd.read_csv(path)
    words = " ".join(str(df['原型']))
    docs.append(words)
vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
vecs = vectorizer.fit_transform(docs)
from sklearn import mixture, cluster
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn import model_selection
import getname
import hierarchy_cluster
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
print('start')
df = pd.DataFrame(vecs.toarray(),columns=vectorizer.get_feature_names())
df["subject"]=list(paths.keys())
df = df.set_index("subject")
gmm=hierarchy_cluster.hierarchy_cluster(df)

print('end')
lis = []
plt.figure(num=None, figsize=(16, 9), dpi=200, facecolor='w', edgecolor='k')
dendrogram(gmm,labels=df.index)
plt.show()
import numpy
clusters = fcluster(gmm,1.2*numpy.average(gmm[:,2]), criterion='distance')
from getname import GetNameJ
for doc, cls in zip(paths.keys(), clusters):
    lis.append((cls, GetNameJ(doc)))
lis.sort()

print(max(clusters))
print(type(clusters))
import getscore

#pd.to_pickle(,"pkl/train_codes.pkl")
#pd.to_pickle(train_docs, "pkl/train_docs.pkl")
pd.to_pickle(vecs,"pkl/vec.pkl")
pd.to_pickle(clusters,"pkl/clusters.pkl")
pd.to_pickle(gmm,"pkl/gmm.pkl")
