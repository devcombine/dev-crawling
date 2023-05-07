from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from pandas import DataFrame
import time

Delay=2.5

global driver
global xpath

course_data = []
course_urls = []
course_name = []
course_rate = []
course_tag = []
course_lan = []
course_level = []
course_ins = []
course_rev_cnt = []
course_vat_price = []
course_price = []

for page in range(1, 58): 
    with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
        driver.get("https://www.inflearn.com/courses/it-programming?order=seq&page="+str(page))
        for element in driver.find_elements(By.CLASS_NAME, "course-data"):
            attrs = []
            for attr in element.get_property('attributes') :
                attrs.append(attr['value'])
            course_data.append(attrs[1])
        # url
        for element in driver.find_elements(By.CLASS_NAME, "course_card_back"):
            aTag = element.find_element(By.CLASS_NAME, "e_course_click")
            url = aTag.get_attribute('href')
            course_urls.append(url)

# 강의명
i = 0
for course in course_data:
    course_name.append(course[course_data[i].find('"course_title\":"')+16:course_data[i].find('","course_level":')])
    i += 1

# 별점
i = 0
for course in course_data:
    course_rate.append(course[course_data[i].find('"star_rate":')+12:course_data[i].find(',"review_count":')])
    i += 1

# 카테고리
i = 0
for course in course_data:
    course_tag.append(course[course_data[i].find('"second_category":"')+19:course_data[i].find('","skill_tag":')])
    i += 1

# 사용언어
i = 0
for course in course_data:
    course_lan.append(course[course_data[i].find('"skill_tag":"')+13:course_data[i].find('","seq0_instructor_id":')])
    i += 1

# 난이도
i = 0
for course in course_data:
    course_level.append(course[course_data[i].find('"course_level":"')+16:course_data[i].find('","first_category":')])
    i += 1

# 강사명
i = 0
for course in course_data:
    course_ins.append(course[course_data[i].find('"seq0_instructor_name":"')+24:course_data[i].find('","student_count":')])
    i += 1

# 후기 개수
i = 0
for course in course_data:
    course_rev_cnt.append(course[course_data[i].find('"review_count":')+15:course_data[i].find(',"is_new_course":')])
    i += 1

# 원가 가격
i = 0
for course in course_data:
    course_vat_price.append(course[course_data[i].find('"reg_vat_price":')+16:course_data[i].find(',"selling_price":')])
    i += 1

# 현재 가격
i = 0
for course in course_data:
    course_price.append(course[course_data[i].find('"reg_price":')+12:course_data[i].find(',"reg_vat_price":')])
    i += 1
    
# 데이터프레임
raw_data = {'Site': 'Inflearn', 
            'Lecture_name': course_name,
            'Rate': course_rate,
            'Tag': course_tag,
            'Language': course_lan, 
            'Level': course_level, 
            'Teacher': course_ins, 
            'Rate_count': course_rev_cnt,
            'Origin_price': course_vat_price, 
            'New_price': course_vat_price, 
            'Url': course_urls}
df=DataFrame(raw_data)
df.to_csv('Inflearn.csv',index=False, encoding="utf-8-sig")#csv로 저장

print('저장이 완료되었습니다.')