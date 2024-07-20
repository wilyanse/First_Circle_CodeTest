import pandas as pd
from sqlalchemy import create_engine
import transformation

def upload_data():
    users = transformation.users
    users.to_sql('users', engine, if_exists='replace', index=False)
    print("Data uploaded successfully!")

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
