from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def convert_to_excel(name,date,director,link):
    df=pd.DataFrame(data=name,columns=["Movie names"])
    df["Director"]=director
    df["Release Date"]=date
    df["Link"]=link
    df.to_csv("moviesdata.csv")

def send_email():
    sender="akshsood0@gmail.com"
    password="MANJU._.ATUl1"
    reciever="nanda.grow10x@gmail.com"
    msg=MIMEMultipart()
    msg["From"]=sender
    msg["To"]=reciever
    msg["Subject"]="Movies Result From Bot"
    body="hey this is the attchment dontaining the data that i collected from the web "
    msg.attach(MIMEText(body,"plain"))
    attachment=open("moviesdata.csv","rb")
    p=MIMEBase("application","octect-stream")
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header("Content-Disposition", "attachment; filename=moviesdata.csv")
    msg.attach(p)
    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sender,password)
    server.send_message(msg)
    server.quit()

def get_details(driver,movies_links):
    i=0
    release_date_list=[]
    director_list=[]
    for m in movies_links:
        driver.get(m)
        page = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "__next")))
        try:
            date=page.find_elements_by_xpath("//a[@class='ipc-link ipc-link--baseAlt ipc-link--inherit-color TitleBlockMetaData__StyledTextLink-sc-12ein40-1 rgaOW']")
            release_date_list.append(date[0].text)
        except:
            release_date_list.append("not found")
        cast_page_link=page.find_element_by_link_text("Cast & crew")
        cast_page_link.click()
        try:
            page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table[@class='simpleTable simpleCreditsTable']")))
            cells=page.find_elements_by_tag_name("tr")
            d=[]
            for c in cells:
                d.append(c.text)
            director_list.append(d)
        except:
            d=[]
            d.append("Not available")
            director_list.append(d)
        i=i+1
        print("\r",f'Current Progress : {i}',end="")
    return release_date_list,director_list

movies_name=[]
movies_links=[]
loc = "D:/softwares/chromedriver.exe"
driver = webdriver.Chrome(loc)
driver.get("https://imdb.com")
search = driver.find_element_by_name("q")
search.send_keys("The Exorcist")
search.send_keys(Keys.RETURN)
second_page = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, "The Exorcist"))
)
second_page.click()
third_page=second_page = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, "Horror"))
)
third_page.click()
forth_page=WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.LINK_TEXT, "Feature Films"))
)
forth_page.click()


while len(movies_name)<50:
    fifth_page=WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "main")))
    movie_list=fifth_page.find_elements_by_class_name("lister-item-header")
    for movie in movie_list:
        link=movie.find_element_by_tag_name("a")
        movies_name.append(link.text)
        movies_links.append(link.get_attribute("href"))
    link=fifth_page.find_element_by_link_text("Next »")
    link.click()    

release_date_list,director_list=get_details(driver,movies_links)
driver.quit()
o=[]
for x in director_list:
    name=""
    for y in x:
        f=y.split(" ")
        name=name+f[0]+" "+f[1]+","
    o.append(name[:-1])
convert_to_excel(movies_name,release_date_list,o,movies_links)
send_email()
