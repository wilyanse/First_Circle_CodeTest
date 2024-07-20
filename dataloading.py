import pandas as pd
from sqlalchemy import create_engine
import transformation
from logger_config import setup_logger

logger = setup_logger('dataloading')

def upload_data():
    users = transformation.users
    users.to_sql('users', engine, if_exists='replace', index=False)
    logger.info(str(users.shape[0]) + ' entries were added to PostgreSQL.')

def query_data():
    query = 'SELECT * FROM users'
    df = pd.read_sql(query, engine)
    print("Data fetched successfully!")
    print(df)

dbname="postgres"
user="postgres"
password="munch"
host="localhost"
port = '5432'

connection_string = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
engine = create_engine(connection_string)

query_data()
