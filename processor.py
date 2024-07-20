import pandas as pd
from logger_config import setup_logger

logger = setup_logger('processing')
class Processor:
    def __init__(self, columns, types):
        self.dataframe = pd.DataFrame(columns=columns)
        self.columns = columns
        self.types = types
    
    def add_csv(self, filepath):
        new_entries = pd.read_csv(filepath)
        try:
            new_entries = self.clean_data(new_entries)
            new_entries = new_entries[self.columns]
            logger.info('Adding ' + str(new_entries.shape[0]) + ' entries from: ' + filepath)
            self.dataframe = (self.dataframe.copy() if new_entries.empty else new_entries.copy() if self.dataframe.empty
                                else pd.concat([self.dataframe, new_entries], ignore_index=True)
                                )
        except KeyError as e:
            logger.error(e)

    def type_check(self, df):
            new_df = df.copy()
            new_df['errors'] = new_df.apply(self.check_entries, axis=1)
            errors_df = new_df[new_df['errors'].apply(lambda x: bool(x))]
            if not errors_df.empty: print(errors_df[[self.columns[0], 'errors']])
    
    def check_entries(self, row):
        errors = []
        for cur in range(len(self.columns)):
            if self.types[cur] == 'datetime':
                if pd.isna(row[self.columns[cur]]):
                    errors.append(str(self.columns[cur]) + ' is not datetime')
                    logger.error(str(self.columns[cur]) + ' is not datetime')
            elif self.types[cur] == 'int':
                if not isinstance(row[self.columns[cur]], int):
                    if self.columns[cur] == -1:
                        errors.append(str(self.columns[cur]) + ' has an incorrect data type')
                        logger.error(str(self.columns[cur]) + ' has an incorrect data type')
                        continue
                    errors.append(str(self.columns[cur]) + ' is not ' + str(self.types[cur]))
                    logger.error(str(self.columns[cur]) + ' is not ' + str(self.types[cur]))
            else:
                if not isinstance(row[self.columns[cur]], str):
                    errors.append(str(self.columns[cur]) + ' is not ' + str(self.types[cur]))
                    logger.error(str(self.columns[cur]) + ' is not ' + str(self.types[cur]))
        return errors

    def clean_data(self, df):
        new_df = df

        for cur in range(len(self.columns)):
            if self.types[cur] == 'int':
                new_df[self.columns[cur]] = pd.to_numeric(new_df[self.columns[cur]], errors='coerce', downcast='integer')
                if self.columns[cur] == 'amount':
                    new_df[self.columns[cur]] = new_df[self.columns[cur]].fillna(-1).astype(int)
            elif self.types[cur] == 'datetime':
                new_df[self.columns[cur]] = pd.to_datetime(new_df[self.columns[cur]], errors='coerce', format='mixed')
            else:
                new_df[self.columns[cur]] = new_df[self.columns[cur]].astype(str)
        new_df = self.drop_nulls(new_df)
        return new_df

    def get_dataframe(self):
        return self.dataframe

    def drop_nulls(self, df):
        return df.dropna()