import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
import unicodedata



headers = {"user-agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"}


def get_novel_list(page_no, categoryCode):
    url = f"https://series.naver.com/novel/top100List.series?rankingTypeCode=WEEKLY&categoryCode={categoryCode}&page={page_no}"
    response = requests.get(url, headers=headers)
    html = bs(response.text, "lxml")
    title_list = html.select("#content > div > ul > li > div.comic_cont > h3 > a")
    summary_list = html.select("#content > div > ul > li > div.comic_cont > p")
    
    title_list_txt = []

    for i in range(len(title_list)) :
        title_list_txt.append(title_list[i].text)
        title_list_txt
        
    summary_list_txt = []

    for i in range(1, len(summary_list),2) :
        summary_list_txt.append(unicodedata.normalize("NFKD", summary_list[i].text))
    
    df_title_list_txt = pd.DataFrame(title_list_txt)
    df_summary_list_txt = pd.DataFrame(summary_list_txt)
    title_summary = pd.concat([df_title_list_txt, df_summary_list_txt],axis=1) 
        
    return title_summary


#시작할 페이지 번호
page_no = 1
categoryCode = 209
# 데이터를 저장할 빈 변수 선언
novel_list_df = pd.DataFrame()
    
while True:
    print(page_no, categoryCode)

    get_novel_list(page_no, categoryCode)
    #마지막 날짜를 가져
    #마지막 날짜를 비교했을 때 같으면 while 종료
    if get_novel_list(page_no, categoryCode).equals(get_novel_list(page_no-1, categoryCode)) :
        break
        
    novel_list_df = pd.concat([novel_list_df, get_novel_list(page_no, categoryCode)])
#     novel_list_df.concat(title_summary)
    page_no += 1

novel_list_df = novel_list_df.reset_index(drop=True)
novel_list_df.columns = ["제목","요약"]


genre = "BL"

file_name = f"novel_list_top_100_{genre}.csv"

novel_list_df.to_csv(file_name, index=False)