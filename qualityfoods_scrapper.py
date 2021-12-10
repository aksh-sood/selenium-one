import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import requests
import re

i=1
title=[]
tags=[]
category=[]
vendor=[]
quantity=[]
price=[]
images=[]
description=[]
plink=[]
primary_list=[]
main_url="https://www.qualityfood.ae"
file_name=main_url.split("/")[-1].split(".")[1]
def convert_to_excel(title,category,description,price,vendor,quantity,tags,images):
    df=pd.DataFrame(data=title,columns=["Product Name"])
    df["Category"]=category
    df["description"]=description
    df["Price"]=price
    df["vendor"]=vendor
    df["quantity"]=quantity
    df["Tags"]=tags
    df["Product Pic"]=images
    
    df.to_csv(file_name+"_scrapper"+".csv")

    
CLEANR=re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
def cleanhtml(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext

def description_data(x):
    y=cleanhtml(x).split("\n")
    filter_object=filter(lambda x:x!="",y)
    return list(filter_object)

loc = "D:/softwares/chromedriver.exe"
driver = webdriver.Chrome(loc)
ac=ActionChains(driver)
driver.get(main_url)
nav = driver.find_element_by_class_name("tmenu_nav")
nav_title=nav.find_elements_by_tag_name("li")
for index,head in enumerate(nav_title):
    if index==1:
        pass
    else:
        ac.move_to_element(head).perform()
        
primary_list=nav.find_elements_by_tag_name("a")

for plist in primary_list:
    if plist.get_attribute("href")!="javascript:;": 
        plink.append(plist.get_attribute("href"))
driver.quit()
plink=list(set(plink))

for l in plink:
  print("\r",i,end="")
  i=i+1
  try:
    link=l+"/products.json"
    json_data=requests.get(link).json()
    dictionaries=json_data["products"]
    for p in dictionaries:
      tag=""
      tags_list=p["tags"]
      b=description_data(p["body_html"])
      title.append(p["title"])
      category.append(p["product_type"])
      price.append(p["variants"][0]["price"])
      vendor.append(p["vendor"])
      try:
        for t in tags_list:
            tag=tag+t+","
        tags.append(tag[:-1])
      except:
        tags.append("No tags")
      try:
        images.append(p["images"][0]["src"])
      except:
        images.append("No images")
      try:
        quantity.append(b[0])
      except:
        quantity.append("No quantity")
      try:
        if b[1]!="Product Description:" and b[1]!="ProductÂ Description:Â " and b[1]!="Product Description:Â" and b[1]!="Â":
          description.append(b[1])
        else:
          description.append("No description")
      except:
        description.append("No description")
  except:
    print("Error continue")

convert_to_excel(title,category,description,price,vendor,quantity,tags,images)
