import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  #DEBUG を INFOに変えるとlogging.debugが出力されなくなる

from natto import MeCab
import pandas as pd 

# sysdicの初期値は環境によって書き換えること
# 辞書のパス(適用されている辞書のパス）はコマンドラインで　`medab -D`で調べられる
def parse2df(text,sysdic="/usr/local/lib/mecab/dic/naist-jdic"):
    """文毎に形態素解析を行い、結果をdataframeに格納して返す
    Args:
      text:形態素解析対象のテキスト
    Returns:
      形態素解析結果を格納したdataframe
      カラムは['文番号','表層', '品詞1','品詞2','品詞3','品詞4','原型','posID']
    """
    #結果格納用の空のDataFrame
    df = pd.DataFrame(index=[], columns=['文番号','表層', '品詞1','品詞2','品詞3','品詞4','原型','posID'])
    
    text = text.split("\n") #改行で分割して配列にする
    while '' in text: #空行は削除
        text.remove('')
    
    parser = MeCab("-d "+sysdic)

    for index,sentence in enumerate(text): 
        logging.debug(sentence)
        nodes = parser.parse(sentence,as_nodes=True)
        for node in nodes:
            if not node.is_eos():
                #品詞情報を分割
                feature = node.feature.split(',')
                #dataframeに追加
                series = pd.Series( [
                    index,          #文番号
                    node.surface,   #表層
                    feature[0],     #品詞1
                    feature[1],     #品詞2     
                    feature[2],     #品詞3
                    feature[3],     #品詞4
                    feature[6],     #原型
                    node.posid      #品詞番号
                ], index=df.columns)
                df = df.append(series, ignore_index = True)
    logging.debug("End : parse2df")            
    return df
   

f = open('chunk.json') #青空文庫の文字コードはshiftjis
text = f.read()  #ファイル終端まで全て読んだデータを返す
f.close()

df = parse2df(text)
df
df2 = df[df["posID"].isin([36,37,38,40,41,42,43,44,45,46,47,50,51,52,66,67,2,31,10,34])]
stop_words = ["する","課題","授業","*","."]
df2 = df2[~df2["原型"].isin(stop_words )]  # ~df.isin(list) で listに含まれないもの となる
df2
df2["原型"]
df2["原型"].to_csv("siravas.csv") 