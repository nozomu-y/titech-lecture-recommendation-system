import requests
from bs4 import BeautifulSoup
import re
import json


def parse_syllabus(url):
    res = requests.get(url)
    if res.status_code != 200:
        print("Error:", res.status_code)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")

    dic = {}

    # 講義名
    title = soup.select_one("#right-contents > div.page-title-area.clearfix > h3").text.strip()
    title = title.split("　")[1]
    title_jp = title.split("\xa0\xa0\xa0")[0]
    title_en = title.split("\xa0\xa0\xa0")[1]
    dic['講義名'] = {}
    dic['講義名']['日本語'] = title_jp
    if "学士特定" in title_jp or "研究プロジェクト" in title_jp:
        return None
    dic['講義名']['英語'] = title_en

    # 講義の概要
    overview = soup.select_one("#right-contents > div.gaiyo-data.clearfix").find_all("dl")
    for item in overview:
        if item.select_one("dt").text.strip() == "アクセスランキング":
            dic[item.select_one("dt").text.strip()] = re.search(r'\d+', item.select_one("dd > img")['src']).group()
        elif item.select_one("dt").text.strip() == "担当教員名":
            teachers = item.select("dd > a")
            dic['担当教員名'] = []
            for teacher in teachers:
                dic['担当教員名'].append(teacher.text)
        elif item.select_one("dt").text.strip() == "授業形態":
            form = item.select_one("dd").text
            form = form.replace("\n", "")
            form = form.replace("\t", "")
            form = form.replace(" ", "")
            forms = form.split("/")
            dic['授業形態'] = []
            for f in forms:
                dic['授業形態'].append(f)
        else:
            dic[item.select_one("dt").text.strip()] = item.select_one("dd").text.strip().replace("\xa0\xa0", " ")

    # シラバス
    syllabus = soup.select("#overview > div")
    for syl in syllabus:
        h3 = syl.select_one("h3")
        if h3.text == "授業計画・課題":
            schedule = {}
            classes = syl.select("#lecture_plans > tbody > tr")
            for cls in classes:
                count = cls.select_one("td.number_of_times").text
                count = int(count.split("第")[1].split("回")[0])
                schedule[count] = {}
                schedule[count]['授業計画'] = cls.select_one("td.plan").text
                schedule[count]['課題'] = cls.select_one("td.assignment").text
            dic["授業計画・課題"] = schedule
        elif h3.text == "学生が身につける力(ディグリー・ポリシー)":
            dic['学生が身につける力'] = []
            skills = syl.select("#learing_skill2 > tbody > tr > td")
            for skill in skills:
                if "✔" in skill.text:
                    dic['学生が身につける力'].append(skill.select_one("span").text)
        elif h3.text == "キーワード":
            dic['キーワード'] = re.split(', |,|，|、', syl.select_one("p").text)
        elif h3.text == "関連する科目":
            dic['関連する科目'] = []
            subjects = syl.select("ul > li")
            for subject in subjects:
                sub = {}
                if len(subject.text.split(" ： ")) == 2:
                    sub['科目コード'] = subject.text.split(" ： ")[0]
                    sub['講義名'] = subject.text.split(" ： ")[1]
                else:
                    sub['講義名'] = subject.text.split(" ： ")[0]
                dic['関連する科目'].append(sub)
        else:
            dic[h3.text] = syl.select_one("p").text
    return dic


def get_lecture_urls(url):
    res = requests.get(url)
    if res.status_code != 200:
        print("Error:", res.status_code)
    res.encoding = res.apparent_encoding
    soup = BeautifulSoup(res.text, "html.parser")

    tables = soup.select_one("#tab2_scroll")
    lectures = tables.select("td.course_title")
    hrefs = []
    for lecture in lectures:
        link = lecture.select_one("a")
        hrefs.append("http://www.ocw.titech.ac.jp" + link['href'])
    return hrefs


if __name__ == "__main__":
    # 情工の科目一覧
    url = "http://www.ocw.titech.ac.jp/index.php?module=General&action=T0200&GakubuCD=4&GakkaCD=342300&KeiCD=23&tab=2&focus=200&lang=JA"
    hrefs = get_lecture_urls(url)
    lectures = []
    for href in hrefs:
        lecture = parse_syllabus(href)
        if lecture is not None:
            print(lecture['講義名']['日本語'])
            lectures.append(lecture)

    f = open('output.json', 'w')
    json.dump(lectures, f, ensure_ascii=False, indent=4)
    f.close()
