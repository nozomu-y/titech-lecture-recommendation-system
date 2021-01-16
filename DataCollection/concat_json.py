import os
import json

json_paths = os.listdir(path='./output/')
syllabus = []
lectures = {}

for json_path in json_paths:
    if '.json' in json_path:
        f = open('./output/' + json_path, 'r')
        data = json.load(f)
        syllabus.extend(data)
        for lecture in syllabus:
            lectures[lecture['科目コード']] = lecture['講義名']
        f.close()

f = open('syllabus.json', 'w')
json.dump(syllabus, f, ensure_ascii=False, indent=4)
f.close()

f = open('lecture_codes.json', 'w')
json.dump(lectures, f, ensure_ascii=False, indent=4)
f.close()
