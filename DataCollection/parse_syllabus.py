from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import re
import json
import os

options = Options()
# do not open browser window
# options.headless = True
driver = webdriver.Chrome(options=options)
skip_major = ['文系教養科目', '英語科目', '第二外国語科目', '日本語・日本文化科目', '教職科目', '広域教養科目', '理工系教養科目']


def get_major_urls():
    # archived
    url = "http://www.ocw.titech.ac.jp/index.php?module=Archive&action=ArchiveIndex&lang=JA"
    driver.get(url)
    wait_load()
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    schools = soup.select("#left-body-1 > ul > li")  # 学院一覧
    majors = {}
    for school in schools:
        if school.select_one("li > a").text == '初年次専門科目':
            continue
        links = school.select("li > ul > li > a")
        for link in links:
            if link.text == "共通専門科目":
                continue
            majors[link.text] = "http://www.ocw.titech.ac.jp/" + link['href']
    f = open('syllabus_url_archived.json', 'w')
    json.dump(majors, f, ensure_ascii=False, indent=4)
    f.close()

    # current
    url = "http://www.ocw.titech.ac.jp/index.php?module=General&action=T0100&GakubuCD=10&lang=JA"
    driver.get(url)
    wait_load()
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")
    schools = soup.select("#left-body-1 > ul > li")  # 学院一覧
    majors = {}
    for school in schools:
        if school.select_one("li > a").text == '初年次専門科目':
            continue
        links = school.select("li > ul > li > a")
        for link in links:
            if link.text == "共通専門科目":
                continue
            majors[link.text] = "http://www.ocw.titech.ac.jp/" + link['href']
    f = open('syllabus_url_current.json', 'w')
    json.dump(majors, f, ensure_ascii=False, indent=4)
    f.close()


def parse_syllabus(url):
    # options = Options()
    # # do not open browser window
    # # options.headless = True
    # driver = webdriver.Chrome(options=options)
    driver.get(url)
    # time.sleep(3)
    wait_load()
    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "html.parser")

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
            dic[item.select_one("dt").text.strip()] = re.search(
                r'\d+', item.select_one("dd > img")['src']).group()
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
            dic[item.select_one("dt").text.strip()] = item.select_one(
                "dd").text.strip().replace("\xa0\xa0", " ")

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
            try:
                dic[h3.text] = syl.select_one("p").text
            except BaseException:
                pass
    return dic


def get_lecture_urls(html):
    # driver.get(url)
    # time.sleep(3)
    # html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    tables = soup.select_one("#tab2_scroll")
    lectures = tables.select("td.course_title")
    hrefs = {}
    for lecture in lectures:
        link = lecture.select_one("a")
        if "http://www.ocw.titech.ac.jp" not in link['href']:
            hrefs[link.text] = "http://www.ocw.titech.ac.jp" + link['href']
        else:
            hrefs[link.text] = link['href']
    return hrefs


def wait_load():
    while True:
        try:
            driver.find_element_by_id("wrapper")
            break
        except NoSuchElementException:
            continue


def hard_refresh():
    driver.execute_script("location.reload(true);")


def get_annual_list(url, major_name):
    for year in range(2019, 2015, -1):
        print(major_name)
        print(year)
        if major_name in skip_major:
            print('skip:' + major_name)
            continue
        if os.path.exists('./output/' + major_name + '_' + str(year) + '.json'):
            print('file exists: ./output/' + major_name + '_' + str(year) + '.json')
            continue
        driver.get(url)
        wait_load()
        driver.find_element_by_css_selector(
            "#archive_nendo_tabs > ul > li:nth-child(" + str(2020 - year) + ") > a").click()

        wait_load()
        hard_refresh()
        wait_load()

        html = driver.page_source.encode('utf-8')
        save_syllabus(html, year, major_name)


def save_syllabus(html, year, major_name):
    lecture_urls = get_lecture_urls(html)
    lectures = []
    total = len(lecture_urls)
    now = 0
    for title, href in lecture_urls.items():
        now += 1
        if "学士特定" in title or "研究プロジェクト" in title:
            continue
        lecture = parse_syllabus(href)
        if lecture is not None:
            print(" * " + lecture['講義名']['日本語'] + "[" + str(now) + "/" + str(total) + "]")
        lectures.append(lecture)
    f = open('output/' + major_name + '_' + str(year) + '.json', 'w')
    json.dump(lectures, f, ensure_ascii=False, indent=4)
    f.close()


if __name__ == "__main__":
    if not (os.path.exists("./syllabus_url_current.json")
            and os.path.exists("./syllabus_url_archived.json")):
        get_major_urls()

    f = open('syllabus_url_current.json', 'r')
    urls = json.load(f)
    for major_name, url in urls.items():
        print(major_name)
        print(2020)
        if major_name in skip_major:
            print('skip:' + major_name)
            continue
        if os.path.exists('./output/' + major_name + '_2020.json'):
            print('file exists: ./output/' + major_name + '_2020.json')
            continue
        driver.get(url)
        wait_load()
        html = driver.page_source.encode('utf-8')
        save_syllabus(html, 2020, major_name)
    f.close()

    f = open('syllabus_url_archived.json', 'r')
    urls = json.load(f)
    for major_name, url in urls.items():
        get_annual_list(url, major_name)

    driver.close()
    driver.quit()
