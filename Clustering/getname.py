
# 科目コードから講義名(日本語)をえる
def GetNameJ(code):
    import json
    lecture_codes = '../DataCollection/lecture_codes.json'
    with open(lecture_codes) as f:
        lectures = json.load(f)
    if code in lectures.keys():
        return lectures[code]['日本語']
    return None

# 科目コードから講義名(英語)を得る


def GetNameE(code):
    import json
    lecture_codes = '../DataCollection/lecture_codes.json'
    with open(lecture_codes) as f:
        lectures = json.load(f)
    if code in lectures.keys():
        return lectures[code]['英語']
    return None

# 科目コードから、関連する科目の科目コードを得る


def GetRelaSub(code):
    import json
    lecture_codes = '../DataCollection/lecture_codes.json'
    with open(lecture_codes) as f:
        lectures = json.load(f)
    output = []
    if code in lectures.keys():
        if '関連する科目' in lectures[code].keys():
            for lecture in lectures[code]['関連する科目']:
                output.append(lecture)
    return output

    #  for path in syllabus_paths:
    #  with open(path) as f:
    #  lectures = json.load(f)
    #  for lecture in lectures:
    #  str = lecture['科目コード']
    #  if(code == str):
    #  if '関連する科目' in lecture.keys():
    #  relaSubs = lecture['関連する科目']
    #  lis = []
    #  for sub in relaSubs:
    #  if '科目コード' in sub.keys():
    #  lis.append(sub['科目コード'])

    #  return lis
    #  return []


if __name__ == '__main__':
    print(GetRelaSub('CAP.P211'))
