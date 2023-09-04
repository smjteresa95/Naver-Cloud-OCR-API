from dbsetup import get_connection

class dbQuery:

    def __init__(self):
        self.conn = get_connection()
        self.cursor = self.conn.cursor()


    #영양성분 이미지Url 가져오기
    def fetch_nutri_image_from_table(self, table_name):
        query = f'SELECT product_id, nutri_image FROM {table_name}'

        self.cursor.execute(query)
    
        results = self.cursor.fetchall()
        return results
    

    
    def save_value(self, table_name, data):
        columns = data.keys()
        values = tuple(data.values)

        columns_string = ', '.join(columns)
        columns_value = ', '.join(values)

        query = f'INSERT INTO {table_name} ({columns_string}) VALUES ({columns_value})'

        self.cursor.execute(query)
        self.conn.commit()



    #nutri_fact 가져오기
    def fetch_nutri_fact(self, table_name, product_id):
        #쿼리문에 product_id를 직접 넣어주는 것은 위험
        query = f'SELECT nutri_fact FROM {table_name} WHERE product_id = {product_id}'
        #DB fuction expects tuple or list for its param. 
        self.cursor.execute(query, (product_id,))
        results = self.cursor.fetchone()
        return results


    #영양성분 이미지에서 뽑아온 데이터로 성분 컬럼 채우기
    #data는 다음과 같은 딕셔너리 형식으로 되어있는 것을 쓰면 된다. 
    # data = {
    #     'column1': 'new_value1',
    #     'column2': 'new_value2'
    # }
    def update_nutri_facts(self, table_name, product_id, data):

        #SET(변경할 값) 구문 
        #.item() 으로 key와 value 값을 각각 묶어 list로 만들 수 있다. 
        set_clause = ', '.join([f"{key} = %s" for key, _ in data.items()])

        query = f'''
        UPDATE {table_name}
        SET {set_clause}
        WHERE id = %s
        '''

        #data에서 value 꺼내오기
        values = list(data.values()) + [product_id]

        self.cursor.execute(query, values)
        self.conn.commit()



    def close(self):
        self.conn.close()



