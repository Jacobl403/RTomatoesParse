import os
import shutil
from pathlib import Path
import pandas as pd

# windows specific implementation

OUT_DIR_STR = ".\\out"


class CsvFileHelper:

    @staticmethod
    def save_data_frame(data_frame, thread_prefix):
        if not os.path.isdir(OUT_DIR_STR):
            Path(OUT_DIR_STR).mkdir()
        data_frame.to_csv(f'{OUT_DIR_STR}\\data_{thread_prefix}')

    @staticmethod
    def wipe_out_dir():
        if os.path.isdir(OUT_DIR_STR):
            shutil.rmtree(OUT_DIR_STR)

    @staticmethod
    def get_df_from_out_files() -> pd.DataFrame:
        if os.path.isdir(OUT_DIR_STR):
            result_df = pd.DataFrame()
            file_sources = [file for file in Path(OUT_DIR_STR).rglob('*') if file.is_file()]
            for source in file_sources:
                result_df = pd.concat([result_df, pd.read_csv(source)])
            return result_df
        else:
            print("ERROR no out directory returning empty DataFrame")
            return pd.DataFrame()
