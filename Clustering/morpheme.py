import json
import pandas as pd
from natto import MeCab
import logging
import re


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
    text = re.sub(r"．", "。\n", text)
    text = re.sub(r"。", "。\n", text)
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


if __name__ == '__main__':
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # DEBUG を INFOに変えるとlogging.debugが出力されなくなる
    # logger.setLevel(logging.INFO)

    text = ''
    output = {}

    syllabus_path = 'chunk.json'
    import os
    with open(syllabus_path) as f:
        lectures = json.load(f)
    for leckey in lectures.keys():
        print('DEBAG:START:' + leckey)
        output[leckey] = "data/" + leckey + ".csv"
        if not os.path.isdir('DetData/' + leckey):
            print('DEBAG:CREATE:' + leckey)
            os.mkdir('DetData/' + leckey)
            output[leckey] = "DetData/" + leckey + ".csv"
            if '講義の概要とねらい' in lectures[leckey].keys():
                text = lectures[leckey]['講義の概要とねらい']
            else:
                text = ''
            df = parse2df(text, sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
            df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
            stop_words = ["する", "課題", "授業", "*", "."]
            df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
            df2.to_csv("DetData/" + leckey + "/sum.csv")
            if '到達目標' in lectures[leckey].keys():
                text = lectures[leckey]['到達目標']
            else:
                text = ''
            # text=lectures[leckey]['到達目標']
            df = parse2df(text, sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
            df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
            stop_words = ["する", "課題", "授業", "*", "."]
            df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
            df2.to_csv("DetData/" + leckey + "/goal.csv")
            if 'キーワード' in lectures[leckey].keys():
                text = lectures[leckey]['キーワード']
            else:
                text = ''
            # text=lectures[leckey]['キーワード']
            df = parse2df(text, sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
            df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
            stop_words = ["する", "課題", "授業", "*", "."]
            df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
            df2.to_csv("DetData/" + leckey + "/key.csv")
            if '関連する科目' in lectures[leckey].keys():
                text = lectures[leckey]['関連する科目']
            else:
                text = ''
            # text=lectures[leckey]['関連する科目']
            df = parse2df(text, sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")

            df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
            stop_words = ["する", "課題", "授業", "*", "."]
            df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
            df2.to_csv("DetData/" + leckey + "/rela.csv")
            if '授業計画・課題' in lectures[leckey].keys():
                text = lectures[leckey]['授業計画・課題']
            else:
                text = ''
            # text=lectures[leckey]['授業計画・課題']
            df = parse2df(text, sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
            df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
            stop_words = ["する", "課題", "授業", "*", "."]
            df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
            df2.to_csv("DetData/" + leckey + "/task.csv")
        else:
            if not os.path.isfile("DetData/" + leckey + "/sum.csv"):
                print('DEBAG:CREATE:FILE:' + leckey + 'sum')
                if '講義の概要とねらい' in leckey.keys():
                    text = lectures[leckey]['講義の概要とねらい']
                else:
                    text = ''
                text = lectures[leckey]['講義の概要とねらい']
                df = parse2df(text, sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
                df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
                stop_words = ["する", "課題", "授業", "*", ".", "・"]
                df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
                df2.to_csv("DetData/" + leckey + "/sum.csv")
            if not os.path.isfile("DetData/" + leckey + "/goal.csv"):
                print('DEBAG:CREATE:FILE:' + leckey + 'goal')
                if '到達目標' in lectures[leckey].keys():
                    text = lectures[leckey]['到達目標']
                else:
                    text = ''
                # text=lectures[leckey]['到達目標']
                df = parse2df(text, sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
                #df = parse2df(text)
                df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
                stop_words = ["する", "課題", "授業", "*", "."]
                df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
                df2.to_csv("DetData/" + leckey + "/goal.csv")
            if not os.path.isfile("DetData/" + leckey + "/key.csv"):
                print('DEBAG:CREATE:FILE:' + leckey + 'key')
                if 'キーワード' in lectures[leckey].keys():
                    text = lectures[leckey]['キーワード']
                else:
                    text = ''
                # text=lectures[leckey]['キーワード']
                df = parse2df(text, sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
                # df = parse2df(text)
                df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
                stop_words = ["する", "課題", "授業", "*", "."]
                df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
                df2.to_csv("DetData/" + leckey + "/key.csv")
            if not os.path.isfile("DetData/" + leckey + "/rela.csv"):
                print('DEBAG:CREATE:FILE:' + leckey + 'rela')
                if '関連する科目' in lectures[leckey].keys():
                    text = lectures[leckey]['関連する科目']
                else:
                    text = ''
                # text=lectures[leckey]['関連する科目']
                df = parse2df(text, sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
                df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
                stop_words = ["する", "課題", "授業", "*", "."]
                df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
                df2.to_csv("DetData/" + leckey + "/rela.csv")
            if not os.path.isfile("DetData/" + leckey + "/task.csv"):
                print('DEBAG:CREATE:FILE:' + leckey + 'task')
                if '授業計画・課題' in lectures[leckey].keys():
                    text = lectures[leckey]['授業計画・課題']
                else:
                    text = ''
                # text=lectures[leckey]['授業計画・課題']
                df = parse2df(text, sysdic="/usr/local/lib/mecab/dic/mecab-ipadic-neologd")
                df2 = df[df["posID"].isin([36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 50, 51, 52, 66, 67, 2, 31, 10, 34])]
                stop_words = ["する", "課題", "授業", "*", "."]
                df2 = df2[~df2["原型"].isin(stop_words)]  # ~df.isin(list) で listに含まれないもの となる
                df2.to_csv("DetData/" + leckey + "/task.csv")
            print(text)

        '''
        os.mkdir('DetData/' + leckey)
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
    f = open('chunk.json') # 青空文庫の文字コードはshiftjis
    text = f.read()  # ファイル終端まで全て読んだデータを返す
    f.close()
    """
