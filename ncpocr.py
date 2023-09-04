import configparser

import requests
import uuid
import time
import json
import io, sys, re

# 파이썬의 표준 출력과 표준 에러 출력을 UTF-8 인코딩으로 변경하는 코드
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

config = configparser.ConfigParser()
config.read(r'C:\Users\msong\Desktop\Bootcamp\bitcamp\Project KINNI\VisionAPI\vision_api\config.ini')


image_url = 'https://sitem.ssgcdn.com/84/22/80/qlty/1000034802284_q1.jpg'


#json 형식으로 데이터 뽑아온 후 텍스트로 바꿔오기
def fetch_data(image_url):

    api_url = config['NCPOCR']['api_url']
    secret_key = config['NCPOCR']['secret_key']

    request_json = {
        "images": [
            {
                "format": "jpg",
                "name" : "demo",
                "data" : None,
                "url" : image_url
            }
        ],

        "lang": 'ko',
        "requestId": str(uuid.uuid4()),
        "resultType": str(uuid.uuid4()),
        "version": 'V2',
        "timestamp": int(round(time.time()*1000))
    }

    headers = {
        'Content-Type': 'application/json',
        'X-OCR-SECRET': secret_key
    }

    response = requests.post(api_url, data=json.dumps(request_json).encode('UTF-8'), headers=headers)

    data = response.json()

    if 'images' in data and len(data['images']) > 0:
        # Extract all 'inferText' values from the 'fields' list inside the 'images' list
        infer_texts = [item['inferText'] for item in data['images'][0]['fields']]

        return infer_texts
        # for text in infer_texts:
        #     print(text)
    else:
        print("The images key is missing or empty")




def list_to_string(data):
    result = ""
    for text in data:
        result += text
    
    return result 



def get_product_name(data):
    try:
        #제품명이 포함 된 요소의 인덱스 찾기 
        start_index = next(
            (i for i, s in enumerate(data) if '제품명' in s), None
        ) + 1
        if start_index is None:
            return '제품명이 없는듯?!'

          # start_index = data.index('제품명') +1 
        potential_end_keywords = ['식품유형', '내용량', '보관방법', '수입원']

        end_index = None

        # start_index 부터 시작해서 각각 요소의 index 와 value를 얻어온다. 
        # 즉, '제품명' 이 존재하는 리스트의 인덱스 값을 알아낸다.
        for i, value in enumerate(data[start_index:], start=start_index):
            # 현재 value에서 potential_end_keywords 에 있는 값을 중 하나가 존재하면,
            # any() 함수가 true를 반환한다. 
            if any(keyword in value for keyword in potential_end_keywords):
                #현재 인덱스를 end_index로 설정한다. 
                end_index = i
                break

        if end_index is None:
            # return data[start_index + 1]
            return ''.join(data[start_index:])

        return ''.join(data[start_index:end_index])
    
    except (ValueError, IndexError):
        return '제품명 없음'



def get_report_num(data):
    found = False

    for item in data:

        #ocr로 fetch 해 온 data list에 keyword가 존재하는지
        for keyword in ['품목보고번호', '품목보고']:
            if keyword in item:
                found = True

                numbers_in_keyword_item = re.findall(r'(\d{5,}\s*-?\s*\d+)', item)
                if numbers_in_keyword_item: 
                    return numbers_in_keyword_item[0]

            if found:
                numbers = re.findall(r'(\d{5,}\s*-?\s*\d+)', item)
                if numbers:
                    return numbers[0]
        
    #키워드 뒤에 숫자가 없으면 None을 반환한다.        
    return None



#1회 제공량 얻어오기
def get_serving_size(data):

    # 경우의 수
    # '1개(30g)당', ''1개(25', '1개(30g)당', "(30", '100g당', '100g', '1개(110g)당'


    # 100g당 이 하나의 value로 존재하면 100을 return 하면 되고, 
    # 없으면 지정해 준 keyword 앞에 위치한 value 중에서 
    keywords = ['g)당', 'g당', 'g 당', '당']




def get_next_num_after_keyword(data, keyword):
    found = False

    for item in data:

        #ocr로 fetch 해 온 data list에 keyword가 존재하는지
        if keyword in item:
            found = True

            numbers_in_keyword_item = re.findall(r'(\d+\.\d+|\d+)', item)
            if numbers_in_keyword_item: 
                return numbers_in_keyword_item[0]

        if found:
            numbers = re.findall(r'(\d+\,?\d+\.?\d+)', item)
            if numbers:
                return numbers[0]
        
    #키워드 뒤에 숫자가 없으면 None을 반환한다.        
    return None



def get_kcal_value(data):
    if '영양정보' in data:
        for i, item in enumerate(data):
            if item in ['kcal', 'kcall'] and i>0:
                kcal_value = data[i-1]

                if kcal_value.isdigit():
                    return int(kcal_value)
    return None



def get_nutri_value(text, keyword):

    pattern = r'{}\s*(?:g)?\s*(\d+[\,]?\d*\.?\d*|\.\d+)\s*(?:g|mg)?'.format(keyword)
    match = re.search(pattern, text)
    if match:
        value = match.group(1)
        return value
    return None
                


data = fetch_data(image_url)

# data = ['제품명 :', '팡올레', '식품유형 :', '빵류(가열하지', '않고', '섭취하는', '냉동식품)', '원재료명 :', '밀가루,스타터(밀가루,정제수,정제소금),계란,설탕,바터(우유),유채유,효모,탈지', '분유,글리세린지방산에스테르,정제소금,밀단백,밀글루텐,당근추출물,비타민C,', '우유단백', '밀,계란,우유', '함유', '제조원 :', 'BRIOCHE', 'PASQUIER', 'AUBIGNY', '원산지 :', '프랑스', '내용량 :', '280g(1,044kcal)', '업소명 및', '(주)에스에이치에스', '전화:070-7136-5973', '소재지 :']
print(data)
# # serving = get_next_num_after_keyword(data, '내용량')
# # print(serving)

product_name = get_product_name(data)
print(product_name)

# nutri_data = list_to_string(data)
# print(nutri_data)

# carb = get_nutri_value(nutri_data, '트랜스지방')
# print(carb)
