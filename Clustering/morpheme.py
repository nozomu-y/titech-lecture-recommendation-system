import json
import pandas as pd
from natto import MeCab
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # DEBUG を INFOに変えるとlogging.debugが出力されなくなる


# sysdicの初期値は環境によって書き換えること
# 辞書のパス(適用されている辞書のパス）はコマンドラインで　`medab -D`で調べられる
def parse2df(text, sysdic="/usr/local/lib/mecab/dic/naist-jdic"):
    """文毎に形態素解析を行い、結果をdataframeに格納して返す
    Args:
      text:形態素解析対象のテキスト
    Returns:
      形態素解析結果を格納したdataframe
      カラムは['文番号','表層', '品詞1','品詞2','品詞3','品詞4','原型','posID']
    """
    # 結果格納用の空のDataFrame
    df = pd.DataFrame(index=[], columns=['文番号', '表層', '品詞1', '品詞2', '品詞3', '品詞4', '原型', 'posID'])

    text = text.split("\n")  # 改行で分割して配列にする
    while '' in text:  # 空行は削除
        text.remove('')

    parser = MeCab("-d " + sysdic)

    for index, sentence in enumerate(text):
        logging.debug(sentence)
        nodes = parser.parse(sentence, as_nodes=True)
        for node in nodes:
            if not node.is_eos():
                # 品詞情報を分割
                feature = node.feature.split(',')
                # dataframeに追加
                series = pd.Series([
                    index,  # 文番号
                    node.surface,  # 表層
                    feature[0],  # 品詞1
                    feature[1],  # 品詞2
                    feature[2],  # 品詞3
                    feature[3],  # 品詞4
                    feature[6],  # 原型
                    node.posid  # 品詞番号
                ], index=df.columns)
                df = df.append(series, ignore_index=True)
    logging.debug("End : parse2df")
    return df


text = ''
output = {}

# syllabus_path = '../DataCollection/output.json'
syllabus_path = 'chunk.json'
import os
with open(syllabus_path) as f:
    lectures = json.load(f)
for leckey in lectures.keys():
    output[leckey] = "data/" + leckey + ".csv"
    '''
    os.mkdir("DetData/" + leckey)
    output[leckey] = "DetData/" + leckey + ".csv"
    text=lectures[leckey]['講義の概要とねらい']
    df = parse2df(text,sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    #df = parse2df(text)
    df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
    stop_words = ["する", "課題", "授業", "*", "."]
    df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
    df2.to_csv("DetData/" + leckey + "/sum.csv")
    
    text=lectures[leckey]['到達目標']
    df = parse2df(text,sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
    stop_words = ["する", "課題", "授業", "*", "."]
    df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
    df2.to_csv("DetData/" + leckey + "/goal.csv")
    
    text=lectures[leckey]['キーワード']
    df = parse2df(text,sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    #df = parse2df(text)
    df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
    stop_words = ["する", "課題", "授業", "*", "."]
    df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
    df2.to_csv("DetData/" + leckey + "/key.csv")
    
    text=lectures[leckey]['関連する科目']
    df = parse2df(text,sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    #df = parse2df(text)
    df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
    stop_words = ["する", "課題", "授業", "*", "."]
    df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
    df2.to_csv("DetData/" + leckey + "/rela.csv")
    
    text=lectures[leckey]['授業計画・課題']
    df = parse2df(text,sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
    #df = parse2df(text)
    df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
    stop_words = ["する", "課題", "授業", "*", "."]
    df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
    df2.to_csv("DetData/" + leckey + "/task.csv")
    '''

f = open('path_clustering.json', 'w')
json.dump(output, f, ensure_ascii=False, indent=4)
f.close()
"""
f = open('chunk.json') #青空文庫の文字コードはshiftjis
text = f.read()  #ファイル終端まで全て読んだデータを返す
f.close()
"""
