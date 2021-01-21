import sys
import os
import numpy as np

def main():
            
    #相対パス取得
    base = os.path.dirname(os.path.abspath(__file__))

    #ファイルパス取得
    data_file = os.path.normpath(os.path.join(base, './data/data.tsv'))
    label_file = os.path.normpath(os.path.join(base, './data/label_nm.txt'))
    feature_file = os.path.normpath(os.path.join(base, './data/feature_nm.txt'))
        
    #データ読み込み
   # data = np.loadtxt(data_file, delimiter='\t')
    data = open(data_file, 'r', encoding='utf-8').readlines()
    label = open(label_file, 'r', encoding='utf-8').readlines()
    for i in range(len(data)):
        data[i] = data[i].rstrip("\n")
    for i in range(len(label)):
        label[i] = label[i].rstrip("\n")
    feature = open(feature_file, 'r', encoding='utf-8').readlines()
    for i in range(len(feature)):
        feature[i] = feature[i].rstrip("\n")

    data_writer = open(data_file, 'a', encoding='utf-8')

    for i in range(len(data), len(label)): 
        print("「"+ label[i] +"」を思い浮かべてください")
        print("┃ 「YES」なら 5 、「NO」なら 1	┃")
        print("┃ 「わからない場合」は 3 を入力 ┃") 

        input_tsv = ""
        for feature_nm in feature:
            print(feature_nm)

            if input_tsv != "":
                input_tsv = input_tsv + "\t"
            
            input_tsv = input_tsv + input()

        data_writer.write(input_tsv + "\n")   

if __name__ == "__main__":
    sys.exit(int(main() or 0))