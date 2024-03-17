import requests
from bs4 import BeautifulSoup as BS
import time
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"}

def create_soup(url):
    res = requests.get(url,headers=headers)
    res.raise_for_status()
    soup = BS(res.text,'lxml')
    return soup

def news_scrap():
    soup = create_soup('https://news.naver.com/main/main.naver?mode=LSD&mid=shm&sid1=104')
    cluster_groups = soup.find_all("div",attrs={"class":"cluster_group _cluster_content"})
    for idx, cluster in enumerate(cluster_groups):
        title = cluster.find("div",attrs={"class":"cluster_text"}).a.get_text()
        url = cluster.find("div",attrs={"class":"cluster_text"}).a["href"]
        soup_main = create_soup(url)
        body = soup_main.find("div",attrs={"class":"_article_body_contents"}).get_text().strip()
        if soup_main.find("em",attrs={"class":"img_desc"}):
            body.replace(soup_main.find("em",attrs={"class":"img_desc"}).get_text(),"")
        sentence_lst = body.split(".")
        global curr_time
        curr_time = time.strftime("%Y%m%d%H%M")
        with open(f"global_news{curr_time}.txt","a",encoding="utf8") as news:
            news.write(f"{idx+1}.{title}")
            news.write("\n\n")
            for i in range(0,5):
                news.write(f"{sentence_lst[i]}. ")
            news.write("\n\n")
        if idx >= 3:
            break

news_scrap()