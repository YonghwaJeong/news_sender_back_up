from tkinter import *
import tkinter.ttk as ttk
from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time
import thecampy
from account import *
import requests
from tcaccount import *
import tkinter.messagebox as messagebox
import sys,os

root = Tk() 
root.title("Mail Sender") 
root.geometry("+650+200")
root.resizable(False,False)

# default browser setting
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080") 
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36")
if  getattr(sys, 'frozen', False): 
    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    browser = webdriver.Chrome(chromedriver_path,options=options)
else:
    browser = webdriver.Chrome(options=options)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def international_news():
    global curr_time
    curr_time = time.strftime("%m%d%H%M%S")
    browser.get("https://www.segye.com/newsList/0101040000000")
    soup = BS(browser.page_source,'lxml')
    news_list = soup.find("ul",attrs={"class":"listBox"}).find_all("li")
    for idx, news in enumerate(news_list):
        title = news.a.find("strong",attrs={"class":"tit"}).get_text()
        whole_text = news.a.find("span",attrs={"class":"cont"}).get_text()
        text_list = whole_text.split(".")
        title_head = "국제뉴스"
        with open(f"news_summary{curr_time}.txt","a",encoding="utf8") as f:
            f.write(f"{idx+1}. {title}")
            f.write("\n")
            for i in range(0,4):
                f.write(f"{text_list[i].strip()}. ")
            f.write("\n\n")
        progress_var.set(100*(idx+1)/4)
        progress_bar.update()
        if idx >= 3:
            break
    ent_subject.insert(0,f"{title_head}_{curr_time}")
    messagebox.showinfo("알림","스크랩이 완료되었습니다.")

def business_news():
    global curr_time
    curr_time = time.strftime("%m%d%H%M%S")
    browser.get("https://www.segye.com/newsList/0101030300000")
    soup = BS(browser.page_source,'lxml')
    news_list = soup.find("ul",attrs={"class":"listBox"}).find_all("li")
    for idx, news in enumerate(news_list):
        title = news.a.find("strong",attrs={"class":"tit"}).get_text()
        whole_text = news.a.find("span",attrs={"class":"cont"}).get_text()
        text_list = whole_text.split(".")
        title_head = "경제뉴스"
        with open(f"news_summary{curr_time}.txt","a",encoding="utf8") as f:
            f.write(f"{idx+1}. {title}")
            f.write("\n")
            for i in range(0,4):
                f.write(f"{text_list[i].strip()}. ")
            f.write("\n\n")
        progress_var.set(100*(idx+1)/4)
        progress_bar.update()
        if idx >= 3:
            break
    ent_subject.insert(0,f"{title_head}_{curr_time}")
    messagebox.showinfo("알림","스크랩이 완료되었습니다.")

def asahi_news():
    global curr_time
    curr_time = time.strftime("%m%d%H%M%S")
    res = requests.get("https://www.asahi.com/international/list/?iref=com_inttop_all_list")
    res.raise_for_status()
    soup = BS(res.text,'lxml')
    news_list = soup.find("ul",attrs={"class":"List"}).find_all("li")
    for idx, news in enumerate(news_list):
        sub_url = "https://www.asahi.com/"+news.a["href"]
        res = requests.get(sub_url)
        soup = BS(res.text,'lxml')
        title = soup.find("div",attrs={"class":"_2XWts"}).h1.get_text()
        body_parts = soup.find("div",attrs={"class":"_27jha"}).find_all("p")
        body_whole = [part.get_text().strip() for part in body_parts]
        body_text = "".join(body_whole)
        text_list = body_text.split("。")
        title_head = "일본뉴스"
        with open(f"news_summary{curr_time}.txt","a",encoding="utf8") as f:
            f.write(f"{idx+1}. {title}")
            f.write("\n")
            for i in range(0,4):
                f.write(f"{text_list[i]}。")
            f.write("\n\n")
        progress_var.set(100*(idx+1)/4)
        progress_bar.update()
        if idx >= 3:
            break
    ent_subject.insert(0,f"{title_head}_{curr_time}")
    messagebox.showinfo("알림","스크랩이 완료되었습니다.")


def news_scrap():
    if radio_var.get() == 1:
        international_news()
    elif radio_var.get() == 2:
        business_news()
    elif radio_var.get() == 3:
        asahi_news()

def get_news():
    try:
        f = open(f"news_summary{curr_time}.txt","r",encoding="utf8")
        news = f.read()
        f.close()
        if len(news)>=1500:
            news = news[0:1500]
        return news
    except Exception:
        messagebox.showerror("에러","읽어올 파일이 존재하지 않습니다.")

def send_mail():
    response = messagebox.askyesno("확인 알림",f"위문 편지를 보내시겠습니까?\n\n이름 : 정용화\n생년월일 : 19980814\n입대일자 : 20210927\n입대부대 : {unit_entry.get()}")
    if response == 1:
        name = "정용화"
        bday = 19980814
        enlist_date = 20210927
        unit = unit_entry.get()
        subject = ent_subject.get()
        context = get_news()
        email = ent_from.get()
        password = ent_pw.get()
        try:
            my_soldier = thecampy.Soldier(name, bday, enlist_date, unit)
            msg = thecampy.Message(subject, context)
            tc = thecampy.Client(email,password)
            tc.get_soldier(my_soldier)
            tc.send_message(my_soldier, msg)
            messagebox.showinfo("알림","성공적으로 메일이 전송되었습니다.")
        except Exception as err:
            messagebox.showerror("에러메시지","메일을 전송하지 못했습니다.")

def pw_check():
    messagebox.showinfo("알림",f"비밀번호 : {ent_pw.get()}")

def reset():
    progress_var.set(0)
    progress_bar.update()
    ent_subject.delete(0,len(ent_subject.get()))

def program_off():
    browser.quit()
    root.destroy()

# News selecting Frame and radiobuttons
selecting_Frame = LabelFrame(root,text="뉴스선택",relief="solid",bd=1)
selecting_Frame.pack(padx=5,pady=5)
image_frame = Frame(selecting_Frame,bd=0)
image_frame.pack()
img1 = PhotoImage(file=resource_path("news_sender_img/international.png"))
img2 = PhotoImage(file=resource_path("news_sender_img/business.png"))
img3 = PhotoImage(file=resource_path("news_sender_img/japanese.png"))
label1 = Label(image_frame,image = img1).pack(side="left")
label2 = Label(image_frame,image = img2).pack(side="left")
label3 = Label(image_frame,image = img3).pack(side="left")
radiobutton_frame = Frame(selecting_Frame,bd=0)
radiobutton_frame.pack()
# given value will be used to select function
# Note) selected value = radio_var.get()
radio_var = IntVar()
R1 = Radiobutton(radiobutton_frame,text="국제뉴스",variable=radio_var,value=1)
R1.pack(side="left",padx=25)
R1.select()
R2 = Radiobutton(radiobutton_frame,text="경제뉴스",variable=radio_var,value=2)
R2.pack(side="left",padx=25)
R3 = Radiobutton(radiobutton_frame,text="일본어뉴스",variable=radio_var,value=3)
R3.pack(side="left",padx=25)

# headless option(deleted) and scraping button
button_frame = Frame(root,relief="solid",bd=0)
button_frame.pack(pady=10)
Button(button_frame,fg="blue",padx=10,pady=7,text="작업시작",command=news_scrap).pack(side="left")
Button(button_frame,fg="red",padx=10,pady=7,text="작업리셋",command=reset).pack(side="left")

# progress frame
progress_frame = LabelFrame(root,text="진행상황",relief="solid",bd=1,padx=5,pady=5)
progress_frame.pack(fill="x",padx=5,pady=3)
progress_var = DoubleVar()
progress_bar = ttk.Progressbar(progress_frame,maximum=100,mode="determinate",variable=progress_var)
progress_bar.pack(fill="x")

# Mail info frame
mail_frame = LabelFrame(root,text="위문편지 설정",relief="solid",bd=1)
mail_frame.pack(fill="x",padx=5,pady=5)
label_frame = Frame(mail_frame,bd=0)
label_frame.pack(side="left",padx=5,pady=5)
Label(label_frame , text="제목").pack(padx=5,pady=5)
Label(label_frame ,text="발신자").pack(padx=5,pady=5)
Label(label_frame ,text="비밀번호").pack(padx=5,pady=5)
entry_frame = Frame(mail_frame,bd=0)
entry_frame.pack(side="left",padx=5,pady=5)
pw_frame = Frame(entry_frame,bd=0)
pw_frame.pack(side="bottom",padx=5,pady=5)
ent_subject = Entry(entry_frame,width=42)
ent_from = Entry(entry_frame,width=42)
ent_from.insert(0,TC_EMAIL_ADDRESS)
ent_pw = Entry(pw_frame,width=37)
ent_pw.insert(0,TC_EMAIL_PASSWORD)
pw_check_button = Button(pw_frame,text="체크",fg="green",command=pw_check)
ent_subject.pack(padx=3,pady=5)
ent_from.pack(padx=3,pady=5)
ent_pw.pack(side="left",padx=3,pady=5)
pw_check_button.pack(side="right")
ent_pw.config(show="*")

# soldier info frame
soldier_frame = LabelFrame(text="수신자 정보",relief="solid",bd=1)
soldier_frame.pack(fill="x",padx=5,pady=5)
subframe1 = Frame(soldier_frame, bd=0)
subframe2 = Frame(soldier_frame, bd=0)
subframe1.pack(fill="x",padx=5,pady=5)
subframe2.pack(fill="x",padx=5,pady=5)
soldier_name = Label(subframe1,text="   이름    ")
soldier_name.pack(side="left")
name_entry = Entry(subframe1,width=17)
name_entry.insert(0,"정용화")
name_entry.pack(side="left")
soldier_bday = Label(subframe1,text="생년월일 ")
bday_entry = Entry(subframe1,width=17)
bday_entry.insert(0,"19980814")
bday_entry.pack(side="right")
soldier_bday.pack(side="right",ipadx=2)
soldier_enlist_date = Label(subframe2,text="입영일자")
soldier_enlist_date.pack(side="left",ipadx=2)
enlist_date_entry = Entry(subframe2,width=17)
enlist_date_entry.insert(0,"20210927")
enlist_date_entry.pack(side="left")
soldier_unit = Label(subframe2,text="입대부대 ")
unit_entry = Entry(subframe2,width=17)
unit_entry.insert(0,"육군훈련소")
unit_entry.pack(side="right")
soldier_unit.pack(side="right",ipadx=2)

name_entry.config(state="readonly")
bday_entry.config(state="readonly")
enlist_date_entry.config(state="readonly")

# bottom frame
bottom_frame = Frame(root,bd=0)
bottom_frame.pack(fill="x")
close_button = Button(bottom_frame,text="닫기",padx=5,pady=5,width=12,command=program_off)
close_button.pack(side="right",padx=5,pady=5)
send_button = Button(bottom_frame,fg="blue",text="보내기",padx=5,pady=5,width=12,command=send_mail)
send_button.pack(side="right",padx=5,pady=5)

root.mainloop()