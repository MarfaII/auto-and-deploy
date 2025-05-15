from datetime import datetime, timedelta
from random import randint
import pandas as pd
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
COMPANIES = eval(config['Companies']['COMPANIES'])
today = datetime.today()
yesterday = today - timedelta(days=1)

if 1 <= today.weekday() <= 5:
    d = {
        'dt': [yesterday.strftime('%Y-%m-%d')] * len(COMPANIES*2),
        'company': COMPANIES * 2,
        'transaction_type': ['buy'] * len(COMPANIES) + ['sell'] * len(COMPANIES),
        'amount': [randint(0, 1000) for _ in range(len(COMPANIES) * 2)]
    }
df = pd.DataFrame(d)
df.to_csv('data_sales.csv', index=False)
