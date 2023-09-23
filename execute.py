from ncp_fill_columns import NutriDataSaver

# 실행파일

# Step 1. OCR 혹은 텍스트에서 받아온 영양성분을 테이블 컬럼에 넣어준다.
# 테이블이 여러개일 때 모두 각각의 테이블에 대해서 적용 할 수 있게끔 한다.
saver = NutriDataSaver()
saver.save_nutri_data_to_db('rawdata')


    #원래는 테이블명을 리스트에 담아서 순서대로 실행시키려고 했으나
    #다음과 같이 에러가 떠서 위와 같은 1차원적인 방법으로 진행했다. 

    #각각의 테이블의 product id 가 같아서 그런 것으로 보인다. 

    #Error occurred in fetch_all_nutri_facts: 1052 (23000): Column 'product_id' in field list is ambiguous
    #No product ids found for table ssg_data, oasis_data

