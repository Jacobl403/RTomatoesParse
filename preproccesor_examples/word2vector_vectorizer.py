from util import CsvFileHelper







class Word2vector_vectorizer:
    def __init__(self):
        
        self.data_to_process = CsvFileHelper.get_df_from_out_files()