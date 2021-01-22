import json
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer
docs=[]
path_open = open('path_clustering.json', 'r')
paths = json.load(path_open)
for path in paths.values():
    df = pd.read_csv(path)
    #print(df.columns)
    #print(df['原型'])
    words = " ".join(str(df['原型']))
    docs.append(words)
vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')
vecs = vectorizer.fit_transform(docs)
from sklearn import mixture, cluster
import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn import model_selection
#from sklearn.cluster import AffinityPropagation
#from sklearn.mixture import BayesianGaussianMixture 
import getname
#from sklearn.cluster import MeanShift
import hierarchy_cluster
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
print('start')
#bgm=BayesianGaussianMixture(n_components=10).fit_predict(vecs.toarray())
#gmm=mixture.bgm
#gmm = mixture.BayesianGaussianMixture(n_components=30).fit_predict(vecs.toarray())
#gmm = AffinityPropagation(random_state=0).fit_predict(vecs.toarray())  #最初の４文書をクラスタリング
#clustering = MeanShift().fit(vecs.toarray())
#gmm=clustering.labels_

df = pd.DataFrame(vecs.toarray(),columns=vectorizer.get_feature_names())
df["subject"]=list(paths.keys())
df = df.set_index("subject")
gmm=hierarchy_cluster.hierarchy_cluster(df)

print('end')
lis = []
plt.figure(num=None, figsize=(16, 9), dpi=200, facecolor='w', edgecolor='k')
dendrogram(gmm,labels=df.index)
plt.show()
'''
for doc, cls in zip(paths.keys(), gmm):
    sub=getname.GetNameJ(doc)
    print(cls, sub)
    
    if getname.GetNameJ(doc) is None:
        continue
    
    lis.append((cls, sub))
    
lis.sort()
print(lis)
'''
#print(gmm)
import numpy
clusters = fcluster(gmm,1.2*numpy.average(gmm[:,2]), criterion='distance')
from getname import GetNameJ
for doc, cls in zip(paths.keys(), clusters):
    lis.append((cls, GetNameJ(doc)))
    #print(cls, GetNameJ(doc))
lis.sort()
#print(lis)
print(max(clusters))
print(type(clusters))
import getscore
#print(getscore.GetScoreClus(paths.keys(),clusters))

'''
import getscore
print(clusters)
print(len(paths.keys()))
print(len(clusters))
print(clusters.tolist())
'''