import os
import json

json_paths = os.listdir(path='./output/')
syllabus = []

for json_path in json_paths:
    if '.json' in json_path:
        f = open('./output/' + json_path, 'r')
        data = json.load(f)
        syllabus.extend(data)
        f.close()

f = open('syllabus.json', 'w')
json.dump(syllabus, f, ensure_ascii=False, indent=4)
f.close()


lectures = {}

for lecture in syllabus:
    lectures[lecture['科目コード']] = lecture['講義名']
    if '関連する科目' in lecture.keys():
        lectures[lecture['科目コード']]['関連する科目'] = []
        for related_lecture in lecture['関連する科目']:
            if '科目コード' in related_lecture.keys():
                lectures[lecture['科目コード']]['関連する科目'].append(related_lecture['科目コード'])
f.close()

f = open('lecture_codes.json', 'w')
json.dump(lectures, f, ensure_ascii=False, indent=4)
f.close()
