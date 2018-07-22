import bs4
import pandas as pd
import urllib.request
import time


df = pd.DataFrame(columns=['date',
                      'program_type',
                      'company',
                      'summary',
                      'detail',
                      'target_grade',
                      'price',
                      'time_table',
                      'system',
                      'summary2',
                      'company2',
                      'target_grade2'
                      ]
             )

with urllib.request.urlopen("https://www.jma-wakuwaku.com/tokyo/program.html#extMdlProgramList") as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, "html.parser")

# top_of_items = soup.find_all("div", id="ProgramList199")
#program_detail_list = top_of_items[0].find_all("div", class_="program_detail_list")

program_detail_list = soup.find_all("div", class_="program_detail_list")

rows = []

for program_detail_div in program_detail_list:
    row = {}
    link_to_detailpage = program_detail_div.a.get("href")          # 詳細ページのリンク
    row['program_type'] = program_detail_div.a.figure.img.get("alt")       # 整理券制など

    row['company'] = program_detail_div.a.div.figure.img.get("alt")       # 会社名
    row['summary'] = program_detail_div.a.div.dl.dt.text                  # 概要

    row['target_grade'] = ""
    try:
        for img_of_targetgrade in program_detail_div.find("ul", class_="target").find_all("img"):
            target_grade_src = img_of_targetgrade.get("src")                      # 対象学年
            src_grade_map = {
                'https://www.jma-wakuwaku.com/img/common/mark-target-chilled.png': "0",
                'https://www.jma-wakuwaku.com/img/common/mark-target-01.png': "1",
                'https://www.jma-wakuwaku.com/img/common/mark-target-02.png': "2",
                'https://www.jma-wakuwaku.com/img/common/mark-target-03.png': "3",
                'https://www.jma-wakuwaku.com/img/common/mark-target-04.png': "4",
                'https://www.jma-wakuwaku.com/img/common/mark-target-05.png': "5",
                'https://www.jma-wakuwaku.com/img/common/mark-target-06.png': "6",
            }
            school_grade = src_grade_map.get(target_grade_src, '不明')
            row['target_grade'] += school_grade
    except Exception as e:
        print('target_gradeの取得でエラー発生したのでスキップ：' + str(e))

    detail_page_url = 'https://www.jma-wakuwaku.com/tokyo/' + program_detail_div.a.get("href")
    time.sleep(2)
    with urllib.request.urlopen(detail_page_url) as f:
        detail_page = f.read()

    detail = bs4.BeautifulSoup(detail_page, "html.parser")
    row['summary2'] = detail.find("strong").text                       # 概要説明
    row['detail'] = detail.find("p").text                             # 詳細説明

    row['target_grade2'] = detail.find("img", alt="参加対象").parent.parent.p.strong.text
    row['date'] = detail.find("img", alt="日付").parent.parent.p.strong.text
    row['time_table'] = detail.find("img", alt="時間割").parent.parent.p.strong.text
    row['system'] = detail.find("img", alt="参加方法").parent.parent.p.strong.text
    row['price'] = detail.find("img", alt="参加料").parent.parent.p.strong.text
    row['company2'] = detail.find("img", alt="提供").parent.parent.p.strong.text

    rows.append(row)

df = pd.DataFrame(rows)
print(df)

df.to_csv('wakuwaku.csv')
