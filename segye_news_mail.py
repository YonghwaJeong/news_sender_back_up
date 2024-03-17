from email.message import EmailMessage
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time
import smtplib
from account import *

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080") 
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36")
browser = webdriver.Chrome(options=options) 
browser.maximize_window()

def global_news_collect():
    browser.get("https://www.segye.com/newsList/0101040000000")
    soup = BS(browser.page_source,'lxml')
    news_list = soup.find("ul",attrs={"class":"listBox"}).find_all("li")
    for idx, news in enumerate(news_list):
        title = news.a.find("strong",attrs={"class":"tit"}).get_text()
        whole_text = news.a.find("span",attrs={"class":"cont"}).get_text()
        text_list = whole_text.split(".")
        global curr_time
        curr_time = time.strftime("%Y%m%d%H%M")
        with open(f"news_summary{curr_time}.txt","a",encoding="utf8") as f:
            f.write(f"{idx+1}. {title}")
            f.write("\n")
            for i in range(0,4):
                f.write(f"{text_list[i].strip()}. ")
            f.write("\n\n")
        if idx >= 3:
            break

global_news_collect()

def get_news():
    f = open(f"news_summary{curr_time}.txt","r",encoding="utf8")
    news = f.read()
    f.close()
    if len(news)>=1500:
        news = news[0:1500]
    return news

news = get_news()

msg = EmailMessage()
msg["Subject"] = f"세계일보-국제뉴스{curr_time}"
msg["From"] = EMAIL_ADDRESS
msg["To"] = "yonghwa814@gmail.com"
msg["Cc"] = "yonghwa814@gmail.com"
msg.set_content(news)

def mail():
    with smtplib.SMTP("smtp.gmail.com",587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
        smtp.send_message(msg)

mail()
browser.quit()