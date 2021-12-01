from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time

def convert_to_excel(name,cat,sub_cat,pic,price,prod_link):
    df=pd.DataFrame(data=name,columns=["Product names"])
    df["Category"]=cat
    df["Sub Category"]=sub_cat
    df["Availability/Price"]=price
    df["Product Pic"]=pic
    df["Link"]=prod_link
    df.to_csv("supermart_scrap.csv")

cat_links=[]
loc = "D:/softwares/chromedriver.exe"
driver = webdriver.Chrome(loc)
driver.get("https://www.supermart.ae/")
f1 = driver.find_element_by_class_name("w2c-catalog-item")
a=f1.find_element_by_tag_name("a")
l=a.get_attribute("href")
driver.get(l)
page = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "category-sub-menu")))
cc=page.find_elements_by_tag_name("ul")
for c in cc:
    dd=c.find_elements_by_tag_name("a")
    for d in dd:
        y=d.get_attribute("href")
        cat_links.append(y)
print(f"total links are {len(cat_links)}")
cat=[]
sub_cat=[]
name=[]
pic=[]
price=[]
prod_link=[]
i=0

for c in cat_links:
    try:
        driver.get(c)
        time.sleep(6)
        page_x=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "main-page-content")))
        products=page_x.find_element_by_id("js-product-list")
        bread_crumb=page_x.find_element_by_xpath("//section[@id='wrapper']//div[@class='col']")
        main_cat=bread_crumb.find_elements_by_tag_name("span")[1].text
        grid=products.find_elements_by_tag_name("article")
        i=i+1
        for g in grid:
            gl=g.text.split("\n")
            z=g.find_element_by_class_name("product-price-and-shipping")
            s=g.find_element_by_class_name("product-category-name")
            q=g.find_element_by_class_name("h3")
            t=g.find_element_by_tag_name("img")
            pl=q.find_element_by_tag_name("a").get_attribute("href")
            prod_link.append(pl)
            pic.append(t.get_attribute("src"))
            price.append(z.text)
            sub_cat.append(s.text)
            name.append(q.text)
            cat.append(main_cat)
        print("\r",f'Current Progress of page: {i}',end="")   
    except:
        print("error occured")
        continue

convert_to_excel(name,cat,sub_cat,pic,price,prod_link)
