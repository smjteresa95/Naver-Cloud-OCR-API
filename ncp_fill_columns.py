from dbquery import dbQuery
from ncpocr import (fetch_data, get_next_num_after_keyword, get_kcal_value, 
                    get_report_num, list_to_string, get_nutri_value, get_product_name,
                    get_serving_size)

db = dbQuery()

nutri_image_urls = db.fetch_nutri_image('ssg_data')
    

# 하나에 대한 상품의 nutri_facts에 있는 문자열에서 각각의 성분 추출하여 column에 저장 할 딕셔너리 형 만들어 반환
# 이미지에서 영양성분을 못찾은 경우 String에 있는 영양성분을 대신 넣는 로직 추가해야 함. 
def get_data_for_db(table_name, product_id):

    nutri_facts, nutri_image = db.find_nutri_facts_nutri_image_by_id(table_name, product_id)

    print(f'nutri_facts: {nutri_facts}')
    print(f'nutri_image: {nutri_image}')

    if nutri_image is None:
        #DB에 nutri_facts column이 있는지 검사
        if nutri_facts:
        #있으면 nutri_facts 에서 가져온 성분정보를 dictionary 형태로 받아와서 DB에 저장
            result = get_one_nutri_data_from_string(nutri_facts)
            return result
        #없으면 continue
        else: 
            return None

    else:
        #image에서 가져온 영양정보를 dictionary 형태로 받아와서 DB에 저장
        result = get_one_nutri_data_from_image(nutri_image)
        return result

    

# image url이 있는 경우 OCR로 데이터 뽑아와서 product_data에 입력하고,
# image url은 없지만 nutri_facts 가 None이 아닌 경우 데이터 처리해서 product_data에 입력하고,
# image url도, nutri_facts 도 없는 경우 null 값 넣는다.


#하나의 상품에 대해 DB의 nutri_facts column 값에서 각각의 영양성분 추출
def get_one_nutri_data_from_string(text):

    product_data = {}

    serving_size = get_serving_size(text) 
    product_data['serving_size'] = serving_size

    sodium = get_nutri_value(text, '나트륨')
    product_data['sodium'] = sodium
    
    carb = get_nutri_value(text, '탄수화물')
    product_data['carb'] = carb

    sugar = get_nutri_value(text, '당류')
    product_data['sugar'] = sugar

    fat = get_nutri_value(text, '지방')
    product_data['fat'] = fat

    trans_fat = get_nutri_value(text, '트랜스지방')
    product_data['trans_fat'] = trans_fat

    saturated_fat = get_nutri_value(text, '포화지방')
    product_data['saturated_fat'] = saturated_fat

    cholesterol = get_nutri_value(text, '콜레스테롤')
    product_data['cholesterol'] = cholesterol

    protein = get_nutri_value(text, '단백질')
    product_data['protein'] = protein


    return product_data




#하나의 이미지서 뽑은 값을 딕셔너리형으로 반환 
def get_one_nutri_data_from_image(url):

    product_data = {}

    #json형식으로 바뀐 데이터들에서 쓸 내용들의 value만 리스트로 받아온다.
    data = fetch_data(url)  

    #리스트에 담겨있던 데이터를 문자열로 바꾼다. 
    nutri_data = list_to_string(data)
    # print(nutri_data)

    # #제품명
    # product_name = get_product_name(data)
    # product_data['product_name'] = product_name
    # print(f'product_name: {product_name}')


    #총 내용량
    total_serving_size = get_next_num_after_keyword(data, '내용량')

    #1회 제공량
    serving_size = get_serving_size(nutri_data)

    #1회 제공량이 존재하지 않는 경우 총 내용량을 삽입한다.
    if serving_size is None:
        product_data['serving_size'] = total_serving_size
    else:
        product_data['serving_size'] = serving_size
    
    #1회 제공량 당 칼로리
    kcal = get_kcal_value(data)
    product_data['kcal'] = kcal

    #품목보고번호 
    report_num = get_report_num(data)
    product_data['report_num'] = report_num

    sodium = get_nutri_value(nutri_data, '나트륨')
    product_data['sodium'] = sodium

    carb = get_nutri_value(nutri_data, '탄수화물')
    product_data['carb'] = carb

    sugar = get_nutri_value(nutri_data, '당류')
    product_data['sugar'] = sugar

    fat = get_nutri_value(nutri_data, '지방')
    product_data['fat'] = fat

    trans_fat = get_nutri_value(nutri_data, '트랜스지방')
    product_data['trans_fat'] = trans_fat

    saturated_fat = get_nutri_value(nutri_data, '포화지방')
    product_data['saturated_fat'] = saturated_fat
  
    cholesterol = get_nutri_value(nutri_data, '콜레스테롤')
    product_data['cholesterol'] = cholesterol

    protein = get_nutri_value(nutri_data, '단백질')
    product_data['protein'] = protein


    return product_data



def get_nutri_data_from_image(image_url):

    product_data = {}

    #받아온 이미지 링크(출력형태: id, image_url)에서 텍스트 뽑아 품목번호만 출력 
    product_id, url = image_url
    product_data['product_id'] = product_id

    try:
        if url: 
            #json형식으로 바뀐 데이터들에서 쓸 내용들의 value만 리스트로 받아온다.
            data = fetch_data(url)  

            #리스트에 담겨있던 데이터를 문자열로 바꾼다. 
            nutri_data = list_to_string(data)
            print(nutri_data)

            #제품명
            product_name = get_product_name(data)
            product_data['product_name'] = product_name
            print(f'product_name: {product_name}')


            #총 내용량
            total_serving_size = get_next_num_after_keyword(data, '내용량')
            print(f'total serving: {total_serving_size}')



            #1회 제공량
            serving_size = get_serving_size(nutri_data)

            #1회 제공량이 존재하지 않는 경우 총 내용량을 삽입한다.
            if serving_size is None:
                product_data['serving_size'] = total_serving_size
            else:
                product_data['serving_size'] = serving_size
            print(f'serving_size: {serving_size}')



            #칼로리: 총 내용량의 칼로리가 아닌, 1회 제공량 당 칼로리를 넣어야 하는데,
            #현재는 
            kcal = get_kcal_value(data)
            product_data['kcal'] = kcal
            print(f'kcal: {kcal}')

            #품목보고번호 
            report_num = get_report_num(data)
            product_data['report_num'] = report_num
            print(f'report_num: {report_num}')

            # sodium = extract_nutri_data(nutri_data, '나트륨', data)
            sodium = get_nutri_value(nutri_data, '나트륨')
            product_data['sodium'] = sodium
            print(f'sodium: {sodium}')

            # carb = extract_nutri_data(nutri_data, '탄수화물', data)
            carb = get_nutri_value(nutri_data, '탄수화물')
            product_data['carb'] = carb
            print(f'carb: {carb}')

            # sugar = extract_nutri_data(nutri_data, '당류',data)
            sugar = get_nutri_value(nutri_data, '당류')
            product_data['sugar'] = sugar
            print(f'sugar: {sugar}')

            # fat = extract_nutri_data(nutri_data, '지방', data)
            fat = get_nutri_value(nutri_data, '당류')
            product_data['fat'] = fat
            print(f'fat: {fat}')

            # trans_fat = extract_nutri_data(nutri_data, '트랜스지방', data)
            trans_fat = get_nutri_value(nutri_data, '트랜스지방')
            product_data['trans_fat'] = trans_fat
            print(f'trans_fat: {trans_fat}')

            # saturated_fat = extract_nutri_data(nutri_data, '포화지방', data)
            saturated_fat = get_nutri_value(nutri_data, '포화지방')
            product_data['saturated_fat'] = saturated_fat
            print(f'saturated_fat: {saturated_fat}')

            # cholesterol = extract_nutri_data(nutri_data, '콜레스테롤', data)
            cholesterol = get_nutri_value(nutri_data, '콜레스테롤')
            product_data['cholesterol'] = cholesterol
            print(f'cholesterol: {cholesterol}')

            # protein = extract_nutri_data(nutri_data, '단백질', data)
            protein = get_nutri_value(nutri_data, '단백질')
            product_data['protein'] = protein
            print(f'protein: {protein}')
    
            print('---------------------------------------------------')

        else:
            print(f"Product {product_id} has no nutrition facts image")
        

    except Exception as e:
        print(f"Error processing product with ID {product_id} and URL {url}: {e}")

    return product_data



product_id_list = db.fetch_all_product_id('ssg_data')

for product_id in product_id_list:
    id = product_id[0]

    #dictionary형 반환값
    data = get_data_for_db('ssg_data', id)
    if isinstance(data, dict):
        db.update_nutri_facts('ssg_data', id, data)
    else: 
        print(f"Data for product_id {id} is not a dictionary. Received: {data}")


db.close_database()