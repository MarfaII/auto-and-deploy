#загружаем нужное
import pandas as pd
import os
import configparser
from datetime import datetime, timedelta

from yahoo_fin.stock_info import get_data
import yfinance as yf
#загружаем самомозданный скласс для БД (pgdb.py)
from pgdb import PGDataBase 


#работаем с config
config = configparser.ConfigParser()
config.read('config.ini')

COMPANIES = (eval(config['Companies']['COMPANIES']))
SALES_PATH = config['Files']['SALES_PATH']
DATABASE_ = config['Database']

#загружаем из таблички (generate_data.py)
sales_df = pd.DataFrame()
if os.path.exists(SALES_PATH):
    sales_df = pd.read_csv(SALES_PATH)
    os.remove(SALES_PATH)    

hist_d ={}
start = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
end = datetime.today().strftime('%Y-%m-%d')

#запрашиваем данные по бирже с yahoo_fin
for ticker in COMPANIES:
    try:
        data = yf.download(ticker, start=start, end=end, interval='1d').stack(level=1).reset_index()
        data = data[['Date', 'Ticker', 'Open', 'Close']]
        hist_d[ticker] = data
    except Exception as e:
        print(f"Ошибка для {ticker}: {e}")

#создаем экземпляр класса БД

database = PGDataBase(
    host=DATABASE_['HOST'],   
    port=DATABASE_['PORT'],
    database=DATABASE_['DATABASE'],
    user=DATABASE_['USER'],
    password=DATABASE_['PASSWORD']
)

#складываем в БД данные из таблички
for i, row in sales_df.iterrows():
    query = f"insert into sales values ('{row['dt']}', '{row['company']}', '{row['transaction_type']}', {row['amount']})"
    database.post(query)


#складываем в БД из yahoo_fin
for company, data in hist_d.items():
    for i, row in data.iterrows():
       query = f"insert into stock values ('{row['Date']}', '{row['Ticker']}', {row['Open']}, {row['Close']})"
       database.post(query)