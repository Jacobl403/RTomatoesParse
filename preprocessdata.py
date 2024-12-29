from util import CsvFileHelper

class PreprocessData:
    def __init__(self):
        self._data_to_process = CsvFileHelper.get_df_from_out_files()

    def preprocess(self):
        print(self._data_to_process['movie_names'].iloc[745:787])