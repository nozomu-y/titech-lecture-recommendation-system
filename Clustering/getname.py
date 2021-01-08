
#科目コードから講義名(日本語)をえる
def GetNameJ(code):
    import json
    #syllabus_path = '../DataCollection/output.json'
    syllabus_paths = [
        '../DataCollection/output/csc_2020.json',
        '../DataCollection/output/csc_2019.json',
        '../DataCollection/output/csc_2018.json',
        '../DataCollection/output/csc_2017.json',
        '../DataCollection/output/csc_2016.json'
    ]
    str=''
    for path in syllabus_paths:
        with open(path) as f:
            lectures = json.load(f)
    
        for lecture in lectures:
            str=lecture['科目コード']
            if(code==str):
                return lecture['講義名']['日本語']
    return 'not_exit'

#科目コードから講義名(英語)を得る
def GetNameE(code):
    import json
    #syllabus_path = '../DataCollection/output.json'
    syllabus_paths = [
        '../DataCollection/output/csc_2020.json',
        '../DataCollection/output/csc_2019.json',
        '../DataCollection/output/csc_2018.json',
        '../DataCollection/output/csc_2017.json',
        '../DataCollection/output/csc_2016.json'
    ]
    str=''
    for path in syllabus_paths:
        with open(path) as f:
            lectures = json.load(f)
    
        for lecture in lectures:
            str=lecture['科目コード']
            if(code==str):
                return lecture['講義名']['英語']
    return 'not_exit'

#科目コードから、関連する科目の科目コードを得る
def GetRelaSub(code):
    import json
    #syllabus_path = '../DataCollection/output.json'
    syllabus_paths = [
        '../DataCollection/output/csc_2020.json',
        '../DataCollection/output/csc_2019.json',
        '../DataCollection/output/csc_2018.json',
        '../DataCollection/output/csc_2017.json',
        '../DataCollection/output/csc_2016.json'
    ]
    str=''
    for path in syllabus_paths:
        with open(path) as f:
            lectures = json.load(f)
        for lecture in lectures:
            str=lecture['科目コード']
            if(code==str):
                if '関連する科目' in lecture.keys():
                    relaSubs=lecture['関連する科目']
                    lis=[]
                    for sub in relaSubs:
                        if '科目コード' in sub.keys():
                            lis.append(sub['科目コード'])
                        
                    return lis
    return []
   
"""
if __name__ == '__main__':
    GetNameJ(code)
"""

"""
import getname
getname.GetNameJ('CSC.T352')
のように使う
"""
