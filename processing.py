import pandas as pd
import glob
import os

from processor import Processor

def find_csv_files(directory):
    patterns = {
        'pricing-*.csv': [],
        'transactions-*.csv': [],
        'users-*.csv': []
    }

    for root, dirs, files in os.walk(directory):
        for file in files:
            for pattern in patterns.keys():
                if glob.fnmatch.fnmatch(file, pattern):
                    file_path = os.path.join(root, file)
                    patterns[pattern].append(file_path)
    
    return patterns

def process_files(patterns, process_users, process_transactions, process_pricing):
    for pattern, files in patterns.items():
        for file_path in files:
            if pattern == 'pricing-*.csv':
                print(f'Processing pricing file: {file_path}')
                process_pricing.add_csv(file_path)
                
            elif pattern == 'transactions-*.csv':
                print(f'Processing transactions file: {file_path}')
                process_transactions.add_csv(file_path)
                
            elif pattern == 'users-*.csv':
                print(f'Processing users file: {file_path}')
                process_users.add_csv(file_path)

def correct_amount(process_transactions, process_pricing):
    unique_pricing = process_pricing.dataframe.loc[process_pricing.dataframe.groupby(['product'])['puk'].idxmax()]
    merged_df = pd.merge(process_transactions.dataframe, unique_pricing, on='product')
    desired_cols = ['trans_id', 'user_id', 'product', 'price', 'trans_date']
    merged_df = merged_df[desired_cols]
    merged_df = merged_df.rename(columns={'price': 'amount'})

    process_transactions.dataframe = merged_df
    process_transactions.clean_data(process_transactions.dataframe)
    process_transactions.type_check(process_transactions.dataframe)

directory = r'1_DataSources'
patterns = find_csv_files(directory)
columns = [
    ['user_id', 'name', 'email', 'date_joined'],
    ['trans_id', 'user_id', 'product', 'amount', 'trans_date'],
    ['puk', 'product', 'price']
]
types = [
    ['int', 'str', 'str', 'datetime'],
    ['int', 'int', 'str', 'int', 'datetime'],
    ['int', 'str', 'int']
]
process_users = Processor(columns[0], types[0])
process_transactions = Processor(columns[1], types[1])
process_pricing = Processor(columns[2], types[2])
process_files(patterns, process_users, process_transactions, process_pricing)
correct_amount(process_transactions, process_pricing)