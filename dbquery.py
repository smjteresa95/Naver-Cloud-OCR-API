from dbsetup import get_connection

class dbQuery:

    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()



    #전체 영양성분 이미지Url 가져오기
    def fetch_nutri_image(self, table_name):
        query = f'SELECT product_id, nutri_image FROM {table_name}'

        self. cursor.execute(query)

        results = self.cursor.fetchall()
        return results
    

    #전체 product_id, 영양성분 문자열 가져오기    
    def fetch_all_nutri_facts(self, table_name):
        query = f'SELECT product_id, nutri_facts FROM {table_name}'
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(f'Error occurred: {e}')
            return None
        


    #전체 product_id 가져오기
    def fetch_all_product_id(self, table_name):
        query = f'SELECT product_id FROM {table_name}'
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(f'Error occurred: {e}')
            return None



    #전체 product_id, 성분표이미지 가져오기    
    def fetch_all_nutri_image(self, table_name):
        query = f'SELECT product_id, nutri_image FROM {table_name}'
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(f'Error occurred: {e}')
            return None



    #product_id로 nutri_facts와 nutri_image 가져오기
    def find_nutri_facts_nutri_image_by_id(self, table_name, product_id):
        query = f'SELECT nutri_facts, nutri_image FROM {table_name} WHERE product_id = %s'
        self.cursor.execute(query, (product_id,))
        results = self.cursor.fetchone()
        return results



    #nutri_fact 가져오기
    def fetch_nutri_fact(self, table_name, product_id):
        #쿼리문에 product_id를 직접 넣어주는 것은 위험
        query = f'SELECT nutri_facts FROM {table_name} WHERE product_id = %s'
        #DB fuction expects tuple or list for its param. 
        self.cursor.execute(query, (product_id,))
        results = self.cursor.fetchone()
        return results
    


    #product_name 가져오기
    def fetch_product_name(self, table_name, product_id):
        #쿼리문에 product_id를 직접 넣어주는 것은 위험
        query = f'SELECT product_name FROM {table_name} WHERE product_id = %s'
        #DB fuction expects tuple or list for its param. 
        self.cursor.execute(query, (product_id,))
        results = self.cursor.fetchone()
        return results
    


    #column에 단일 값 업데이트
    def update_value(self, table_name, product_id, column_name, value):
        query = f'''
        UPDATE {table_name}
        SET {column_name} = %s
        WHERE product_id = %s
        '''
        self.cursor.execute(query, (value, product_id))
        self.conn.commit()



    #column에 단일 값 저장
    def save_value(self, table_name, column_name, value):
        query = f'INSERT INTO {table_name} ({column_name}) VALUES (%s)'
        self.cursor.execute(query, (value,))
        self.conn.commit()
        


    #영양성분 이미지에서 뽑아온 데이터로 성분 컬럼 채우기
    #data는 다음과 같은 딕셔너리 형식으로 되어있는 것을 쓰면 된다. 
    # data = {
    #     'column1': 'new_value1',
    #     'column2': 'new_value2'
    # }
    def update_nutri_facts(self, table_name, product_id, data):

        #SET(변경할 값) 구문 
        #.item() 으로 key와 value 값을 각각 묶어 list로 만들 수 있다. 
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])

        query = f'''
        UPDATE {table_name}
        SET {set_clause}
        WHERE product_id = %s
        '''

        #data에서 value 꺼내오기
        values = list(data.values())
        values.append(product_id)

        try:
            self.cursor.execute(query, values)
            self.conn.commit()
        except Exception as e:
            print(f'Error: {e}')
    


    def close_database(self):
        self.cursor.close()
        self.conn.close()




