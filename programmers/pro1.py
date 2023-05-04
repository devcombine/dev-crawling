from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver import ActionChains
import csv

with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    
    f = open(r'programmers.csv', 'w', encoding = 'UTF-8')
    cssWriter = csv.writer(f)
    cssWriter.writerow(["title", "price", "thumbnail_url", "url"])
    
    for i in range(1,11):
        driver.get("https://school.programmers.co.kr/learn?page={}".format(i))
        driver.implicitly_wait(10)
        print("{} page".format(i))

        for j in range(1,13):
            try:
                element_name = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{}]/div[2]/div[1]/h3'.format(j)).text
                element_price = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{}]/div[2]/div[2]/div/strong'.format(j)).text
                element_price = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{}]/div[2]/div[2]/div[1]/strong'.format(j)).text.replace("₩","").replace(",","")
                if element_price == "무료":
                    element_price = "0"
                element_price = int(element_price)
                #element_rate = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{}]/div[2]/div[2]/div[2]'.format(j))
                element_thumb = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{}]/div[1]/img'.format(j)).get_attribute("src")
                element_url = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{}]'.format(j)).get_attribute("href")
                print("강의명: ", element_name)
                print("가격: ", element_price)
                #print("평점: ", element_rate)
                print("썸네일주소: ", element_thumb)
                print("주소: ", element_url)
                print(" ")
            except NoSuchElementException:
                continue
            
            cssWriter.writerow([element_name, element_price, element_thumb, element_url])
        
    f.close()
                