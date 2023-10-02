from ncp_fill_columns import NutriDataSaver

# 실행파일

# Step 1. OCR 혹은 텍스트에서 받아온 영양성분을 테이블 컬럼에 넣어준다.
# 테이블이 여러개일 때 모두 각각의 테이블에 대해서 적용 할 수 있게끔 한다.
saver = NutriDataSaver()
saver.save_nutri_data_to_db('rawdata')



