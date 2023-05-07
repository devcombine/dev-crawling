# 라이브러리 불러오기
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from collections import defaultdict
import time

'''
# 프로그래머스 크롤링
***
link : https://school.programmers.co.kr/learn?page=1
절차 :

1. 태그 수집 작업 : 필터의 체크박스를 선택하고, 선택했을 때 나오는 강의의 태그에 체크박스 항목명을 추가한다.
    - Python 체크박스 클릭, Python 강의의 tags에 Python 추가
2. 전체 강의의 데이터 수집 : 전체항목 페이지에서 페이지를 넘겨가며 항목의 상세 데이터를 가져온다.

'''

# 강의의 태그를 설정하기 위한 dict 선언
# 강의 : [태그 리스트]
courses = defaultdict(set)

# 1. 태그 수집하기
with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    driver.get("https://school.programmers.co.kr/learn")
    
    # 더보기 버튼 클릭
    more_btn = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[1]/div/div[2]/div[1]/div/div/button')
    more_btn.click()
    
    # 체크박스리스트 가져오기 (section1 : 언어, section2 : 난이도)
    lang_ul = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[1]/div/div[2]/div[1]/div/div/ul')
    level_ul = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[1]/div/div[2]/div[2]/div/div/ul')
    
    for i, ul in enumerate([lang_ul, level_ul]):
        ui_id = i + 1
        checkboxes = []
        for i in range(1, len(ul.find_elements(By.TAG_NAME, "li")) + 1):       
            checkbox = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[1]/div/div[2]/div[{ui_id}]/div/div/ul/li[{i}]/label')
            checkboxes.append(checkbox)

        # 하나씩 클릭하면서 가져오기
        for checkbox in checkboxes:
            
            # 체크하기
            checkbox.click()
            time.sleep(1)

            # 현재 체크한 항목명(tag) 가져오기
            tag = checkbox.text.lower()
            if ui_id == 2:
                tag = tag[:3].strip() # 부제목 잘라주기

            # 페이지별로 탐색
            while True:  
                time.sleep(1)

                # 강의 없으면 패스
                try:
                    driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/div')
                    break
                except NoSuchElementException:
                    
                    # 강의 섹션
                    section = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]')
                    for si in range(1, len(section.find_elements(By.TAG_NAME, "a")) + 1):
                        course_title = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]/div[2]/div[1]/h3').text
                        courses[course_title].add(tag)

                    # 다음 페이지 없으면 나가기
                    next_btn = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/div/button[3]')
                    if not next_btn.is_enabled():
                        break
                    else:
                        next_btn.click()

            # 체크 없애기
            checkbox.click()
            time.sleep(2)      
print("태그 수집 완료")                          

# 2. 전체 강의 가져오기
with webdriver.Chrome(service=Service(ChromeDriverManager().install())) as driver:
    # 파일 쓰기
    f = open(r'programmers3.csv', 'w', encoding='UTF-8')
    cssWriter = csv.writer(f)
    cssWriter.writerow(["title","instructor","description","site","url","price", "rating", "thumbnail_url", "enrollment_count","tags"])
    
    # 프로그래머스 접속
    driver.get("https://school.programmers.co.kr/learn") 

    # 페이지별로 탐색
    while True:
        
        # 강의 섹션
        section = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]')
        for si in range(1, len(section.find_elements(By.TAG_NAME, "a")) + 1):
            
            # 모집 마감 제외
            try:
                badge = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]/div[2]/div[1]/div/span')
                if badge.text == '모집 마감':
                    continue
            except NoSuchElementException:
                badge = None
            course_btn = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]')
            title = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]/div[2]/div[1]/h3').text

            # 기본 강의정보 수집
            try:
                price = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]/div[2]/div[2]/div[1]/strong').text
                price = price.replace("₩", "").replace(",", "")
                price = 0 if price == "무료" else int(price)
            except NoSuchElementException:
                price = None
            try:
                thumbnail_url = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]/div[1]/img').get_attribute("src")
            except NoSuchElementException:
                thumbnail_url = None
            try:
                url = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]').get_attribute("href")
            except NoSuchElementException:
                url = None
            try:
                rating = driver.find_element(By.XPATH, f'//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/a[{si}]/div[2]/div[2]/div[2]').text
            except NoSuchElementException:
                rating = None
            
            # 상세 강의정보 수집
            course_btn.click()
            driver.implicitly_wait(3)
            
            # 수강생 수
            enrollment_count = None
            ul = driver.find_element(By.XPATH, '//*[@id="overview-fixed-menu"]/div/ul')
            for li in ul.find_elements(By.TAG_NAME, "li"):
                if '명' in li.text:
                    enrollment_count = int(li.text[:li.text.index('명')].replace(',', ''))
                    break
            # 강사
            try:
                instructor = driver.find_element(By.CLASS_NAME, "name").text
            except NoSuchElementException:
                instructor = None
            
            if not instructor:
                try:
                    instructor = driver.find_element(By.CLASS_NAME, "mentor-name").text
                except NoSuchElementException:
                    instructor = None
            
            complete_data = [title,instructor,'','프로그래머스',url,price,rating,thumbnail_url,enrollment_count,','.join(courses[title])]

            # 파일에 쓰기
            cssWriter.writerow(complete_data)
            driver.back()
        
        next_btn = driver.find_element(By.XPATH, '//*[@id="edu-service-app-main"]/div/div[2]/div/div/section[2]/div/button[3]')
        
        # 다음 페이지 없으면 끝
        if not next_btn.is_enabled():
            break
        next_btn.click()
        time.sleep(1)

    f.close()
    
print('저장이 완료되었습니다.')