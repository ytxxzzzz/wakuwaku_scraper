import bs4
import urllib.request
import time

with urllib.request.urlopen("https://www.jma-wakuwaku.com/tokyo/program.html#extMdlProgramList") as f:
    html = f.read()

soup = bs4.BeautifulSoup(html, "html.parser")

# top_of_items = soup.find_all("div", id="ProgramList199")
#program_detail_list = top_of_items[0].find_all("div", class_="program_detail_list")

program_detail_list = soup.find_all("div", class_="program_detail_list")

for program_detail_div in program_detail_list:
    print(program_detail_div.a.get("href"))                 # 詳細ページのリンク
    print(program_detail_div.a.figure.img.get("alt"))       # 整理券制など

    print(program_detail_div.a.div.figure.img.get("alt"))   # 会社名
    print(program_detail_div.a.div.dl.dt.text)            # 概要

    try:
        for img_of_schoolgrade in program_detail_div.find("ul", class_="target").find_all("img"):
            print(img_of_schoolgrade.get("alt"))                       # 対象学年
    except Exception as e:
        print('エラー発生したのでスキップ：' + str(e))

    detail_page_url = 'https://www.jma-wakuwaku.com/tokyo/' + program_detail_div.a.get("href")
    time.sleep(1)
    with urllib.request.urlopen(detail_page_url) as f:
        detail_page = f.read()

    detail = bs4.BeautifulSoup(detail_page, "html.parser")
    print(detail.find("strong").text)                       # 概要説明
    print(detail.find("p").text)                            # 詳細説明

    print(detail.find("img", alt="参加対象").parent.parent.p.strong.text)
    print(detail.find("img", alt="日付").parent.parent.p.strong.text)
    print(detail.find("img", alt="時間割").parent.parent.p.strong.text)
    print(detail.find("img", alt="参加方法").parent.parent.p.strong.text)
    print(detail.find("img", alt="参加料").parent.parent.p.strong.text)
    print(detail.find("img", alt="提供").parent.parent.p.strong.text)
