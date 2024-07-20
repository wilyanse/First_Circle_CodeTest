import processing
import pandas as pd

def email_lowercase(users):
    users['email'] = users['email'].str.lower()
    print(users.head())

def product_upper(transactions):
    transactions['product'] = transactions['product'].str.upper()
    print(transactions.head())

def total_amount(transactions, users):
    summed_df = transactions.groupby('user_id')['amount'].sum().reset_index()
    merged_df = pd.merge(users, summed_df, on='user_id')
    merged_df = merged_df.rename(columns={'amount': 'total_spent'})
    merged_df.set_index('user_id', inplace=True)
    print(merged_df.head())

users = processing.process_users.get_dataframe()
transactions = processing.process_transactions.get_dataframe()
pricing = processing.process_pricing.get_dataframe()

email_lowercase(users)
product_upper(transactions)
total_amount(transactions, users)