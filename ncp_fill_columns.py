from dbquery import dbQuery
from ncpocr import (fetch_data, get_next_num_after_keyword, get_kcal_value, 
                    get_report_num, list_to_string, get_nutri_value, get_product_name,
                    get_serving_size)

class NutriDataSaver:

    def __init__(self):
        self.db = dbQuery()

    # 하나에 대한 상품의 nutri_facts에 있는 문자열에서 각각의 성분 추출하여 column에 저장 할 딕셔너리 형 만들어 반환
    # 이미지에서 영양성분을 못찾은 경우 String에 있는 영양성분을 대신 넣는 로직 추가해야 함. 
    def get_data_for_db(self, table_name, product_id):

        nutri_facts, nutri_image = self.db.find_nutri_facts_nutri_image_by_id(table_name, product_id)

        if nutri_image is None:
            #DB에 nutri_facts column이 있는지 검사
            if nutri_facts:
            #있으면 nutri_facts 에서 가져온 성분정보를 dictionary 형태로 받아오기
                result = self.get_one_nutri_data_from_string(nutri_facts)
                return result
            #없으면 continue
            else: 
                return None

        else:
            #image에서 가져온 영양정보를 dictionary 형태로 받아오기
            result = self.get_one_nutri_data_from_image(nutri_image)
            return result


        # image url이 있는 경우 OCR로 데이터 뽑아와서 product_data에 입력하고,
        # image url은 없지만 nutri_facts 가 None이 아닌 경우 데이터 처리해서 product_data에 입력하고,
        # image url도, nutri_facts 도 없는 경우 null 값 넣는다. -> 이 부분은 spring boot에서 처리 해줬다.


    #하나의 row에서 product_name이 DB에 존재하면 놔두고 없으면 OCR 에서 뽑아 온 Data에서 가지고 온 제품명 저장
    def select_and_save_product_name(self, table_name, nutri_image, product_id):

        product_name_tuple = self.db.fetch_product_name(table_name, product_id)
        product_name = product_name_tuple[0]

        #DB에 product_name이 없거나 '상세설명참조'로 되어있으면
        if product_name is None or product_name == '상세설명참조':

            #제품명을 OCR에서 뽑아온 데이터로 만든 dictionary에서 
            ocr_result = self.get_one_nutri_data_from_image(nutri_image)
            product_name_val = ocr_result.get('product_name')
            
            self.db.update_value(table_name, product_id, 'product_name', product_name_val)

        else:
            print(f'기존에 있던 {product_name} 으로 놔두면 됨')



    #하나의 상품에 대해 DB의 nutri_facts column 값에서 각각의 영양성분 추출
    @staticmethod
    def get_one_nutri_data_from_string(text):

        product_data = {}

        serving_size = get_serving_size(text) 
        product_data['serving_size'] = serving_size

        sodium = get_nutri_value(text, '나트륨')
        product_data['sodium'] = sodium

        carb = get_nutri_value(text, '탄수화물')
        product_data['carbohydrate'] = carb

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
    @staticmethod
    def get_one_nutri_data_from_image(url):

        product_data = {}

        #json형식으로 바뀐 데이터들에서 쓸 내용들의 value만 리스트로 받아온다.
        data = fetch_data(url)  

        #리스트에 담겨있던 데이터를 문자열로 바꾼다. 
        nutri_data = list_to_string(data)
        # print(nutri_data)

        #제품명
        product_name = get_product_name(data)
        product_data['product_name'] = product_name

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
        product_data['carbohydrate'] = carb

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


    #영양성분과 상품명 DB에 저장
    def save_nutri_data_to_db(self, table_name):

        #tuple list형식으로 product_id와 nutri_image를 받아온다.
        # results = self.db.fetch_all_nutri_facts(table_name)

        product_id_list = self.db.fetch_all_product_id(table_name)

        if product_id_list is None:
            print(f"No product ids found for table {table_name}")
            return

        for product_id in product_id_list:
            id = product_id[0]

            # product_name 값 채워주기
            # product_id로 nutri_image 가지고 온다
            result = self.db.fetch_nutri_image(table_name, id)
            nutri_image = result[0]

            #product_name 없는 것은 OCR로 추출한 제품명 넣어주기.
            self.select_and_save_product_name(table_name, nutri_image, id)

            #dictionary형 반환값
            data = self.get_data_for_db(table_name, id)
            if isinstance(data, dict):
                self.db.update_nutri_facts(table_name, id, data)
            else: 
                print(f"Data for product_id {id} is not a dictionary. Received: {data}")

    
    # def bulk_insert():
