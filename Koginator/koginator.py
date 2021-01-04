# -*- coding: utf-8 -*-
import sys
import classification

def main():
    clf = classification.classification()

    #データファイルを読み込む
    clf.load()

#    while True:
#        str = input()
#        print(str)
#        if str == "1":
#            break



##################################################
#ここから

#問題を出力
#print(clf.queation([0, 1, 2], [1, 3, 5]))
    queation_list = []
    input_list = []
    while True:
        
        queation = clf.queation(queation_list, input_list)
        queation_list.append(queation)

        print("ーーーーーーーーーーーーーーーーーーーー")
        print(queation)
        print("￣￣￣￣￣￣￣￣￣∨￣￣￣￣￣￣￣￣￣￣")
        print("　　　　　　　　∧_∧")
        print("　　　　　　　 < ｀∀´>　")
        print("　　　　　　　　(　∽) ")
        print("　　　　　　　  )ノ")
        print("　　　　　　　　（_　")
        print("　　　　　　　[il=li]　")
        print("　　　　　　　　)=(_") 
        print("　　　　　　　(-==-)") 
        print("　　　　　　　 `ｰ‐'' ") 
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓") 
        print("┃ 「YES」なら 5 、「NO」なら 1	┃")
        print("┃ 「わからない場合」は 3 を入力 ┃") 
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛") 


#回答を受け取る
#input()
        str = input()
        input_list.append(str)
        answer = clf.answer(queation_list, input_list)

#回答があるかどうかを調べる
#str = clf.answer([0, 1, 2], [1, 3, 5])
#もし～ならば(if, else, elsif)

        if answer == "":
            pass
        else:
            print("＿人人人人人人＿") 
            print(answer)
            print("￣Y^Y^Y^Y^Y^Y￣") 
            break

#回答があったら出力してループを抜ける
#print

#回答がなかったら1に戻る
#～のあいだ(while, else)
'''
    #回答について正解なのかを確認する
    print("↑は正解でしたか？")
    print("1:正解") 
    print("2:不正解") 

    #正解かどうかの入力をうける
    if input() == "1":
        #そのまま保存
        pass
    else :
        #正解を得る
        print("正解を選んでください")
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓") 

        #正解のリストを表示
        for i in range(len(clf.clf.classes_)):
            print(i,"：", clf.clf.classes_[i])

        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛") 
    
        answer = clf.clf.classes_[input()]

    clf.save(answer, queation_list, input_list)
 '''   
#ここまで
##################################################
if __name__ == "__main__":
    sys.exit(int(main() or 0))

