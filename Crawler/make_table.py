import pandas as pd
import os
from datetime import datetime
from sqlalchemy import text
from sqlalchemy import create_engine

# --------- instart to mysql start --------- #

def make_engine():
  # read environment variables from .env file
  conf = {}
  with open('.env', 'r') as f:
    for line in f:
      key, value = line.strip().split('=')
      conf[key] = value

  # connect to mysql
  engine = create_engine('mysql+pymysql://'+conf['USER']+':'+conf['PWD']+'@'+conf['HOST']+':'+conf['PORT']+'/'+conf['DB'])
  return engine

def create_table(engine):
    with engine.connect() as con:
        con.execute(text(
            """
            CREATE TABLE IF NOT EXISTS word_counts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                datetime DATETIME,
                main_sec VARCHAR(50),
                sub_sub VARCHAR(50),
                word VARCHAR(50),
                frequency INT)
            """
        ))

def insert_data(engine, datetime_val, main_sec_val, sub_sub_val, word_val, frequency_val):
    with engine.connect() as con:
        con.execute(text(
            """
            INSERT INTO word_counts (datetime, main_sec, sub_sub, word, frequency)
            VALUES (:datetime_val, :main_sec_val, :sub_sub_val, :word_val, :frequency_val)
            """
        ), {
            'datetime_val': datetime_val,
            'main_sec_val': main_sec_val,
            'sub_sub_val': sub_sub_val,
            'word_val': word_val,
            'frequency_val': frequency_val
        })
        con.commit()


# Insert data into MySQL
engine = make_engine()
create_table(engine)

# Insert data
# word_counts_pandas.to_sql('word_counts', engine, if_exists='append', index=False)
for i in range(10):
   insert_data(engine,datetime(2024,7,4,0,0,i),i*100,i*100+i,str(i)+"번째",i+5)
   
# --------- instart to mysql end --------- #


