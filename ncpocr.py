#OCR로 추출 한 텍스트 데이터에서 필요한 부분만 뽑는 작업.
import configparser

import requests 
import uuid
import time
import json
import io, sys, re, os

# 파이썬의 표준 출력과 표준 에러 출력을 UTF-8 인코딩으로 변경하는 코드
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

config = configparser.ConfigParser()
config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_file_path)


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
    

    if 'images' in data and len(data['images']) > 0 and 'fields' in data['images'][0]:
        # Extract all 'inferText' values from the 'fields' list inside the 'images' list
        infer_texts = [item['inferText'] for item in data['images'][0]['fields']]

        return infer_texts
        # for text in infer_texts:
        #     print(text)
    else:
        print("The images key is missing or empty")


#list를 문자열로 변환
def list_to_string(data):
    if data is None:
        return ""
    else:
        result = ""
        for text in data:
            result += text
        print(result)
        return result 



#OCR로 받아온 텍스트 데이터에서 제품명 추출
def get_product_name(data):

    if data is None:
        return "data is None"
    try:
        #제품명이 포함 된 요소의 인덱스 찾기 
        start_index = next(
            (i for i, s in enumerate(data) if '제품명' in s), None
        )
        if start_index is None:
            return None
        start_index += 1

          # start_index = data.index('제품명') +1 
        potential_end_keywords = ['식품유형', '내용량', '보관방법', '수입원', '100']

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
            product_name = ''.join(data[start_index:])

        else: 
            product_name = ''.join(data[start_index:end_index])
        
        #product_name이 100자를 넘어가게되면 100자까지만 출력
        return product_name[:100]
    
    except (ValueError, IndexError):
        return '제품명 없음'



#OCR로 받아온 텍스트 데이터에서 품목보고번호 추출
def get_report_num(data):
    if data is None:
        return 'data is None'
    
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



#1회 제공량 얻어오기(param: string)
def get_serving_size(text):

    # 지정해 준 keyword 앞에 위치한 value 바로 앞에 위치 한 value를 가지고 오거나
    # keyword를 포함하는 value를 가지고 온다. 
    # keywords = ['g)당', 'g당', 'g 당', '당']

    # '개(/d+g)당', 'g당', ' g당' 이 형식으로 나와있는 것들을 찾고
    serving_size_patterns = r'개?\s*[\(]?(\d+\s*(?:g|mg|l|ml))\s*[\)]?\s*당'
    match = re.search(serving_size_patterns, text)

    if match:
        value = match.group(1)
        # 찾은 부분 안에서 숫자만 추출해낸다.
        refined_pattern = r'(\d{2,})'
        match = re.search(refined_pattern, value)

        if match:
            return float(match.group(1))
        
        else:
            return None
    
    else: 
        return None



#Keyword 다음에 있는 숫자 추출
#OCR로 받아온 데이터에서 '내용량' 추출할 때 사용
def get_next_num_after_keyword(data, keyword):
    if data is None:
        return "data is None"
    
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
                return float(numbers[0].replace(',',''))
        
    #키워드 뒤에 숫자가 없으면 None을 반환한다.        
    return None



#OCR로 뽑아 온 데이터에서 칼로리 추출
def get_kcal_value(data):
    if data is None:
        return 'data is None'
    
    elif '영양정보' in data:
        for i, item in enumerate(data):
            if item in ['kcal', 'kcall', ' kcal'] and i>0:
                kcal_value = data[i-1]

                if kcal_value.isdigit():
                    return float(kcal_value)
    else:            
        return None



#문자열에서 영양성분 있는 부분 
def get_nutri_value(text, keyword):
    pattern = r'{}\s*(?:g)?\s*(\d+[\,]?\d*\.?\d*|\.\d+)\s*(?:g|mg)?'.format(keyword)
    match = re.search(pattern, text)
    if match:
        value = float(match.group(1).replace(',',''))
        return value
    return None



#문자열에서 칼로리 추출
def get_kcal_from_string(text):
    pattern = r'(?:kcal|Kcal)?[\)]?\s*(\d+[\,]?\d*\.?\d*|\.\d+)\s*(?:kcal|Kcal)'
    match = re.search(pattern, text)
    if match:
        value = float(match.group(1).replace(',',''))
        return value
    return None
                


