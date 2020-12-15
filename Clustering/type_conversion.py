import json

syllabus_path = '../DataCollection/output.json'

with open(syllabus_path) as f:
    lectures = json.load(f)

output = {}

for lecture in lectures:
    chunk = ''
    for _ in range(7):
        chunk += lecture['講義名']['日本語']
    if '講義の概要とねらい' in lecture.keys():
        chunk += lecture['講義の概要とねらい']
    if '到達目標' in lecture.keys():
        chunk += lecture['到達目標']
    if 'キーワード' in lecture.keys():
        for keyword in lecture['キーワード']:
            for _ in range(5):
                chunk += keyword
    if '関連する科目' in lecture.keys():
        for subject in lecture['関連する科目']:
            for _ in range(5):
                chunk += subject['講義名']
    if '授業計画・課題' in lecture.keys():
        planbef=''
        plan=''
        taskbef=''
        task=''
        for lesson in lecture['授業計画・課題'].values():
            plan=lesson['授業計画']
            if plan!=planbef:
                chunk += plan
            planbef=lesson['授業計画']
            task=lesson['課題']
            if task!=taskbef:
                chunk += task
            taskbef=lesson['課題']
    output[lecture['科目コード']] = chunk

f = open('chunk.json', 'w')
json.dump(output, f, ensure_ascii=False, indent=4)
f.close()
