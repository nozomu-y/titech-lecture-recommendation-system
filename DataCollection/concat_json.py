import os
import json

json_paths = os.listdir(path='./output/')
lectures = []

for json_path in json_paths:
    if '.json' in json_path:
        print(json_path)
        f = open('./output/' + json_path, 'r')
        data = json.load(f)
        lectures.extend(data)
        f.close()

f = open('syllabus.json', 'w')
json.dump(lectures, f, ensure_ascii=False, indent=4)
f.close()
