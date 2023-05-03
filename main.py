import requests
from bs4 import BeautifulSoup
import os
import sys
from datetime import datetime
import csv
import asyncio

now = datetime.now().date()
ORIGIN_PATH = 'https://edu.goorm.io'
header = ['title', 'instructor', 'description', 'url', 'price', 'tag', 'category',
          'rating', 'thumbnail_url', 'is_package', 'is_free', 'enrollment_count', 'uploade_date']


def parse_detail(detail_url: str) -> dict:
    """
    url 상세 페이지 파싱 함수
    포함된 정보 : title', 'instructor', 'description', 'url', 'price', 'tag', 'category', 'rating', 'thumbnail_url', 'is_package', 'is_free', 'enrollment_count', 'uploade_date'
    """
    
    row_template = dict.fromkeys(header)  # 딕셔너리 초기화
    path_res = requests.get(detail_url)
    path_soup = BeautifulSoup(path_res.content, 'html.parser')

    row_template['url'] = detail_url

    # min 정보 변수
    row_template['title'] = path_soup.find('h1').text
    row_template['instructor'] = str(path_soup.find(
        'div', attrs={'class': '_2xx4v5'}).text).replace('캡틴', '')

    row_template['thumbnail_url'] = path_soup.find(
        'div', attrs={'data-mkt-id': 'edu_lectureDetail_img_thumbnail'}).get('style').replace('background-image:url(', '').replace(')', '')
    description = path_soup.find(
        'p', attrs={"class": "RoScUb"}).text
    row_template['description'] = None if description == '' else description

    # Table 파싱
    questions = path_soup.find_all('div', attrs={'class': 'GIADkp'})
    answers = path_soup.find_all(
        'div', attrs={'class': '_2yM5um'})
    for question, answer in zip(questions, answers):
        if question.text == '태그':
            row_template['tag'] = answer.text.replace(
                ' ', '').replace(',', '-')  # 정해진 규칙이 없어서 dash 로 다중 구분
        if question.text == '카테고리':
            row_template['category'] = list(
                answer.text.replace(' ', '').split(','))[-1]

    # 가격 관련 변수
    price = path_soup.find(
        'div', attrs={'data-mkt-id': 'edu_lecture_div_lecturePrice'}).text
    row_template['is_free'] = False if price != '무료' else True
    row_template['price'] = int(
        price.replace(',', '')) if price != '무료' else 0

    # 기타
    row_template['rating'] = float(
        path_soup.find('span', attrs={"class": "_2KWt9f"}).text)
    row_template['is_package'] = False          # groom은 default가 False

    return row_template


# tsv 파일 쓰기 -> String의 , 공백으로 tsv 저장
os.makedirs('./result/', exist_ok=True
f = open('./result/' + f'{now}_groomedu.tsv', 'w', newline='')
wr = csv.writer(f, delimiter='\t')
wr.writerow(header)

# 동기적으로 실행하기
q = 1  # QueryString 초기화
count = 1  # cmd counter
while True:
    try:
        res = requests.get(
            f'https://edu.goorm.io/category/programming?page={q}&sort=newest')

        print(f'QueryString Page Change : {q}.')
        soup = BeautifulSoup(res.text, 'html.parser')
        link_list = [a['href'] for a in soup.select('a[href]')]
        # 구름에듀는 분야 - 백엔드 & 프론트 & 데엔이 나뉘어져 있지 않아, 분류 기준을 두고 전처리를 다시 해야할 것 같긴하다.
        i = 0
        for link in link_list:
            if link.startswith('/lecture/'):

                # file 쓰기
                value_list = list(parse_detail(ORIGIN_PATH + link).values())
                wr.writerow(value_list)

                #   추후에 log로 변경하기
                print(f'[{count}] - {ORIGIN_PATH + link}')
                count += 1
                i += 1

        if i == 0:
            print("lecture Content가 더 이상 찾을 수 없습니다.")
            break
        q += 1

    except Exception as e:
        print('requests : ', e)
        break

print('저장이 완료되었습니다.')
f.close()  # 파일 종료
