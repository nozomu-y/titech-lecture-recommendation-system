# -*- coding: utf-8 -*-
import sys
import classification

class koginator:
    def __init__(self):
        self.clf = classification.classification()
        self.clf.load()
        self.queation_list = []
        self.input_list = []

##################################################
#ここから

#問題を出力
#print(clf.queation([0, 1, 2], [1, 3, 5])
    def getQuestion(self):
        
        question = self.clf.queation(self.queation_list, self.input_list)
        self.queation_list.append(question)
        return question

#回答を受け取る
#input()
    def getAnswer(self, newAns='0'):
        self.input_list.append(newAns)
        self.answer = self.clf.answer(self.queation_list, self.input_list)

#回答があるかどうかを調べる
#str = clf.answer([0, 1, 2], [1, 3, 5])
#もし～ならば(if, else, elsif)

        if self.answer == "":
            return False
        else:
            self.answer = self.answer.split(',')
            return True

    def printAnswer(self):
        print('***************************')
        for ans in self.answer:
            print(ans)
        print('***************************')

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
    kg = koginator()
    while True:
        question = kg.getQuestion()

        print("ーーーーーーーーーーーーーーーーーーーー")
        print(question)
        print("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓") 
        print("┃ 「YES」なら 5 、「NO」なら 1	┃")
        print("┃ 「わからない場合」は 3 を入力 ┃") 
        print("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛") 

        if(kg.getAnswer(input())):
            break

    kg.printAnswer()

