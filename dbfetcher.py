# 이부분은 현재 springboot에서 해주고 있어, 포함하지 않도록 한다. 
import configparser
from sqlalchemy import create_engine

# Parse the config.ini file
config = configparser.ConfigParser()
config.read(r'config.ini')


#Retreive database table as pandas DataFrame
import pandas as pd
from sqlalchemy import create_engine

# Extract the values from the config.ini file
host = config['database']['host']
user = config['database']['user']
password = config['database']['password']
db = config['database']['db']
charset = config['database']['charset']

# Create the connection string using the extracted values
connection_string = f'mysql+mysqlconnector://{user}:{password}@{host}/{db}?charset={charset}'

# Create the engine
engine = create_engine(connection_string)

select_clause = '''
    nut_image,
    category_name,
    product_name,
    serving_size,
    kcal,
    carbohydrate,
    protein,
    fat,
    sodium,
    cholesterol,
    saturated_fat,
    trans_fat,
    sugar,
    image
'''

rawdata_df = pd.read_sql(f"SELECT {select_clause} FROM rawdata", engine)

#to_sql을 이용해 product table로 bulk insert
# rawdata_df.to_sql(name='product', con=engine, if_exists='append', index=False)

