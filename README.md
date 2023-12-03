# Naver-Cloud-OCR-API
Extract nutrition data using Naver Cloud OCR API

<h3 align="left">Project description:</h3>
As a part of a Kkini project, our team needed nutrition information for each food product. After getting the nutrition facts images by web scraping, fetch text from the image via OCR API. Process text data as needed then save them into the database.
</br></br>
Kkini project의 일부로, 서비스를 하기 위해 식품의 영양성분 데이터가 필요하지만 데이터를 얻어올 방법이 없어 추가적으로 만들었습니다.            
Naver Clova의 OCR (Optical Character Recognition) API를 사용하여 영양성분표 이미지에서 필요한 데이터를 추출하고 가공하는 Python 스크립트입니다. 데이터베이스에 저장된 영양성분표 이미지를 분석하여 중요한 영양 정보를 자동으로 식별하고 추출합니다. 추출된 데이터는 필요에 맞게 가공되어 다시 데이터베이스에 저장됩니다. 


<h3 align="left">Set up</h3>
Database info, and api key are stored in config.ini file. which is currently ignored by git. <br>

```
# config.ini
[NCPOCR]
api_url =  # Fill in the API URL
secret_key =  # Fill in the secret key

[database]
host =  # Fill in the database host
port = 3306
user =  # Fill in the database user
password =  # Fill in the database password
db =  # Fill in the database name
charset = utf8mb4
```

Create a `config.ini` file with the necessary information for connecting to the Naver Cloud OCR API and the database. The comments (`# Fill in ...`) are used to indicate where to enter the information. 

```
pip install sqlalchemy
```

```
pip install pandas
```

<h3 align="left">How to use</h3>

run execute.py file



