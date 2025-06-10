import json
import os
import shutil
from pathlib import Path

import kagglehub
import pandas as pd
import pyarrow as pa
from pyarrow import csv
# windows specific implementation

OUT_DIR_STR = ".\\out"
DB_PATH = 'data_sets\\rotten_tomatoes_Essential_2000s_Movies'
MOVIES_CSV_PATH = '\\movies.csv\\movies.csv'
CRITIC_REVIEWS_CSV_PATH = '\\critic_reviews.csv\\critic_reviews.csv'
USER_REVIEWS_CSV_PATH = '\\user_reviews.csv\\user_reviews.csv'

MOVIES_CSV_PATH_LINUX = '/movies.csv/movies.csv'
CRITIC_REVIEWS_CSV_PATH_LINUX = '/critic_reviews.csv/critic_reviews.csv'
USER_REVIEWS_CSV_PATH_LINUX = '/user_reviews.csv/user_reviews.csv'


# self.df_movies = pd.read_csv(path + MOVIES_CSV_PATH_LINUX)
# self.df_critic_reviews = pd.read_csv(path + CRITIC_REVIEWS_CSV_PATH_LINUX)
# self.df_user_reviews = pd.read_csv(path + USER_REVIEWS_CSV_PATH_LINUX)

class CsvFileHelper:
    SCHEMA = pa.schema([
        ('user_id', pa.int64()),
        ('movie_names', pa.list_(pa.string())),
        ('movies_years', pa.list_(pa.int32())),
        ('movies_crit_rating', pa.list_(pa.float32())),
        ('movies_users_rating', pa.list_(pa.float32())),
        ('movies_critics_text_reviews', pa.string()),
        ('user_prev_text_reviews', pa.list_(pa.string())),
        ('rec_title', pa.string()),
        ('rec_mean_crit_score', pa.float32()),
        ('rec_mean_user_score', pa.float32()),
        ('rec_user_verdict', pa.string()),
    ])

    @staticmethod
    def get_movies_df():
        path = kagglehub.dataset_download("bwandowando/rotten-tomatoes-essential-2000s-movies")
        return pd.read_csv(path + MOVIES_CSV_PATH_LINUX)

    @staticmethod
    def get_critic_reviews_df():
        path = kagglehub.dataset_download("bwandowando/rotten-tomatoes-essential-2000s-movies")
        return pd.read_csv(path + CRITIC_REVIEWS_CSV_PATH_LINUX)

    @staticmethod
    def get_user_reviews_df():
        path = kagglehub.dataset_download("bwandowando/rotten-tomatoes-essential-2000s-movies")
        return pd.read_csv(path + USER_REVIEWS_CSV_PATH_LINUX)

    @staticmethod
    def save_data_frame(data_frame, thread_prefix=10):
        if not os.path.isdir(OUT_DIR_STR):
            Path(OUT_DIR_STR).mkdir()
        data_frame.to_csv(f'{OUT_DIR_STR}\\data_{len(data_frame)}.csv')

    @staticmethod
    def save_rows_as_data_frame(rows):
        if not os.path.isdir(OUT_DIR_STR):
            Path(OUT_DIR_STR).mkdir()

        table = pa.Table.from_pylist(rows, schema=CsvFileHelper.SCHEMA)

        ready_table = CsvFileHelper.prepare_table_for_csv(table)
        csv.write_csv(ready_table,f'{OUT_DIR_STR}\\data_{len(rows)}.csv')
        # df = table.to_pandas()
        # df.to_csv(f'{OUT_DIR_STR}\\data_{len(df)}.csv')

    @staticmethod
    def wipe_out_dir():
        if os.path.isdir(OUT_DIR_STR):
            shutil.rmtree(OUT_DIR_STR)

    @staticmethod
    def get_df_from_out_files() -> pd.DataFrame:
        if os.path.isdir(OUT_DIR_STR):
            result_df = pd.DataFrame()
            file_sources = [file for file in Path(OUT_DIR_STR).rglob('*.csv') if file.is_file()]
            for source in file_sources:
                # convert_options = csv.ConvertOptions(column_types=CsvFileHelper.SCHEMA)
                # table = csv.read_csv(source)
                # table.to_pylist()
                # result_df = pd.concat([result_df, table.to_pandas()])
                result_df = pd.concat([result_df, pd.read_csv(source,engine='pyarrow')])
                # result_df = result_df.drop(columns=['Unnamed: 0'])
            return result_df
        else:
            print("ERROR no out directory returning empty DataFrame")
            return pd.DataFrame()

    @staticmethod
    def only_test_purpouse() -> pd.DataFrame:
        test_frame_name = f'{OUT_DIR_STR}\\one_record.csv'
        file_sources = [file for file in Path(OUT_DIR_STR).rglob('*') if file.is_file()]

        def file_finder(file_src):
            return [source for source in file_src if source == test_frame_name]

        filtered_list = file_finder(file_sources)
        if not filtered_list:
            data_df = CsvFileHelper.get_df_from_out_files()
            result = data_df.iloc[:1].copy()
            result.to_csv(f'{OUT_DIR_STR}\\one_record.csv')
            return result
        else:
            return pd.read_csv(filtered_list[0])

    @staticmethod
    def prepare_table_for_csv(table):
        columns = {}

        for field in table.schema:
            name = field.name
            column = table[name]
            print(f'name: {name} column: {column}')
            # Check if this is a list column
            if pa.types.is_list(field.type):
                # Convert each list to a properly formatted string
                # Option 1: JSON format
                list_values = column.to_pylist()
                print("list values: ",list_values)
                json_strings = [json.dumps(lst) if lst is not None else None for lst in list_values]
                print("json_strings: ", list_values)
                columns[name] = pa.array(json_strings)
                print("columns[name] ", columns[name])

                # Option 2: Comma-separated values (alternative approach)
                # csv_strings = [','.join(lst) if lst is not None else None for lst in list_values]
                # columns[name] = pa.array(csv_strings)
            else:
                columns[name] = column

        return pa.table(columns)

    # @staticmethod
    # # Function to read back and parse the list columns
    # def read_csv_with_lists(file_path, list_columns):
    #     # Read the CSV
    #     read_table = csv.read_csv(file_path)
    #
    #     # Convert to Python dictionary for manipulation
    #     data = {col: read_table[col].to_pylist() for col in read_table.column_names}
    #
    #     # Parse the list columns
    #     for col in list_columns:
    #         if col in data:
    #             # Parse JSON strings back to lists
    #             data[col] = [json.loads(item) if item is not None else None for item in data[col]]
    #
    #     # Create new schema
    #     fields = []
    #     for name in data:
    #         if name in list_columns:
    #             fields.append((name, pa.list_(pa.string())))
    #         else:
    #             # Infer type from the original table
    #             for field in table.schema:
    #                 if field.name == name:
    #                     fields.append((name, field.type))
    #                     break
    #
    #     # Create new table with proper schema
    #     new_rows = []
    #     for i in range(len(data[list(data.keys())[0]])):
    #         row = {k: data[k][i] for k in data}
    #         new_rows.append(row)
    #
    #     return pa.Table.from_pylist(new_rows, schema=pa.schema(fields))
