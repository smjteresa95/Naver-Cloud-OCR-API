# Naver-Cloud-OCR-API
extract nutrition data using Naver Cloud OCR API

##Project description
As a part of a Kkini project, our team needed nutrition information for each food product. After getting the nutrition facts images by web scraping, fetch text from the image via OCR API. Process text data as needed then save them into the database.

##How to use the project
database info, and api key are stored in config.ini file. which is currently ignored by git. <br>
```
[NCPOCR]
api_url = 
secret_key = 

[database]
host = 
port = 3306
user = 
password = 
db = 
charset = utf8mb4
```
<br>
need to make a config.ini file then fill out the blanks. 
