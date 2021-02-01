#  from sklearn.pipeline import make_pipeline
#  from sklearn.preprocessing import StandardScaler
import sys
import os
sysFile = os.path.dirname(os.path.abspath(__file__))
sys.path.append(sysFile + '/..')
from Clustering.wordnet import SearchSimilarWords
from Clustering.getname import GetNameJ
from Clustering.morpheme import parse2df

from sklearn.linear_model import SGDClassifier
import json
import pandas as pd
#  from sklearn import mixture, cluster
#  from sklearn.model_selection import GridSearchCV
#  from sklearn import model_selection
#  from sklearn.cluster import AffinityPropagation
#  from sklearn.feature_extraction.text import TfidfVectorizer


def search_lectures(keyword):
    if keyword == '':
        path_open = open(sysFile + '/path_clustering.json', 'r')
        paths = json.load(path_open)

        simlec = []
        for doc in paths.keys():
            simlec.append(doc)
        return simlec

    #########ワードネット#############
    split_words = keyword.split()
    similar_words = split_words.copy()
    for word in split_words:
        tmp = SearchSimilarWords(word)
        if tmp is None:
            continue
        if split_words.index(word)==0:
            for i in range(3):
                #print(split_words.index(word))
                for tmp_word in tmp:
                    similar_words.append(tmp_word)
        elif split_words.index(word)==1:
            for i in range(2):
                #print(split_words.index(word))
                for tmp_word in tmp:
                    similar_words.append(tmp_word)
        else:
            #print(split_words.index(word))
            for tmp_word in tmp:
                similar_words.append(tmp_word)
    #     print(similar_words)
    # print(similar_words)
    for word in similar_words:
        keyword += word + " "
    #  print(keyword)
    ################################

    #  vectorizer = TfidfVectorizer(use_idf=True, token_pattern=u'(?u)\\b\\w+\\b')

    #  path_open = open('path_clustering.json', 'r')
    #  paths = json.load(path_open)
    #  train_docs = []
    #  train_codes = []
    #  for lec_code, path in paths.items():
    #  train_df = pd.read_csv(path)
    #  train_words = " ".join(train_df['原型'].dropna(how='all'))
    #  train_docs.append(train_words)
    #  train_codes.append(lec_code)
    #  train_vecs = vectorizer.fit_transform(train_docs)

    vec = pd.read_pickle(sysFile + '/pkl/vec.pkl')
    vectorizer = pd.read_pickle(sysFile + '/pkl/vectorizer.pkl')
    train_vecs = vec

    test_df = parse2df(keyword, sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    test_df = test_df[test_df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
    test_docs = [" ".join(test_df['原型'].dropna(how='all'))]
    test_vecs = vectorizer.transform(test_docs)

    # gmm = AffinityPropagation(random_state=0).fit(train_vecs.toarray())
    # train_predict = gmm.predict(train_vecs.toarray())
    # test_predict = gmm.predict(test_vecs.toarray())

    clusters2 = pd.read_pickle(sysFile + '/pkl/clusters1.2.pkl')
    clusters7 = pd.read_pickle(sysFile + '/pkl/clusters1.7.pkl')
    # clf = make_pipeline(StandardScaler(), SGDClassifier(max_iter=1000, tol=1e-3))
    clf2 = SGDClassifier(max_iter=1000, tol=1e-3, random_state=1)
    clf7 = SGDClassifier(max_iter=1000, tol=1e-3, random_state=1)
    clf2.fit(train_vecs, clusters2)
    clf7.fit(train_vecs, clusters7)
    test_predict2 = clf2.predict(test_vecs)
    train_predict2 = clf2.predict(train_vecs)
    test_predict7 = clf7.predict(test_vecs)
    train_predict7 = clf7.predict(train_vecs)
    #  print(test_predict)
    #  print(train_predict)
    #  print(clusters)
    path_open = open(sysFile + '/path_clustering.json', 'r')
    paths = json.load(path_open)

    simlec1 = []
    simlec2 = []
    simlec = []
    for doc, cls in zip(paths.keys(), clusters2):
        if test_predict2[0] == cls:
            #  print(doc)
            simlec1.append(doc)
    for doc, cls in zip(paths.keys(), clusters7):
        if test_predict7[0] == cls:
            #  print(doc)
            if doc not in simlec1:
                simlec2.append(doc)
    simlec.append(simlec1)
    simlec.append(simlec2)


    return simlec


if __name__ == '__main__':
    keyword = input('キーワード: ')
    result = search_lectures(keyword)

    print()
    print("類似科目")
    for lecture in result:
        for lec in lecture:
            print(" *", GetNameJ(lec))
        print()
