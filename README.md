# Naver-Cloud-OCR-API
Extract nutrition data using Naver Cloud OCR API

<h3 align="left">Project description:</h3>
As a part of a Kkini project, our team needed nutrition information for each food product. After getting the nutrition facts images by web scraping, fetch text from the image via OCR API. Process text data as needed then save them into the database.

<h3 align="left">How to use the project</h3>
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

