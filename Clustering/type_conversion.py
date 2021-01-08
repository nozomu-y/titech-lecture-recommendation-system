import json

output = {}

with open('../DataCollection/syllabus.json') as f:
    lectures = json.load(f)

for lecture in lectures:
    if lecture['科目コード'] not in output.keys():
        output[lecture['科目コード']] = {}
        output[lecture['科目コード']]['講義の概要とねらい'] = ''
        output[lecture['科目コード']]['到達目標'] = ''
        output[lecture['科目コード']]['キーワード'] = ''
        output[lecture['科目コード']]['関連する科目'] = ''
        output[lecture['科目コード']]['授業計画・課題'] = ''
    if '講義の概要とねらい' in lecture.keys():
        output[lecture['科目コード']]['講義の概要とねらい'] += lecture['講義名']['日本語']
    if '到達目標' in lecture.keys():
        output[lecture['科目コード']]['到達目標'] += lecture['到達目標']
    if 'キーワード' in lecture.keys():
        for keyword in lecture['キーワード']:
            output[lecture['科目コード']]['キーワード'] += keyword
    if '関連する科目' in lecture.keys():
        for subject in lecture['関連する科目']:
            output[lecture['科目コード']]['関連する科目'] += subject['講義名']
    if '授業計画・課題' in lecture.keys():
        planbef = ''
        plan = ''
        taskbef = ''
        task = ''
        for lesson in lecture['授業計画・課題'].values():
            plan = lesson['授業計画']
            if plan != planbef:
                output[lecture['科目コード']]['授業計画・課題'] += plan
            planbef = lesson['授業計画']
            task = lesson['課題']
            if task != taskbef:
                output[lecture['科目コード']]['授業計画・課題'] += task
            taskbef = lesson['課題']

f = open('chunk.json', 'w')
json.dump(output, f, ensure_ascii=False, indent=4)
f.close()
