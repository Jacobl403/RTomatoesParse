import keras as ks
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import json
from util import CsvFileHelper
import tensorflow as tf
from ModelGRU import MyModel
# this is V1 preprocessor for now
class PreprocessData:
    def __init__(self):
        pass

    def preprocess(self):
        data_to_process = CsvFileHelper.get_df_from_out_files()
        # self.validate_data_with_print(data_to_process)
        movies_df = CsvFileHelper.get_movies_df()
        # print(movies_df.info())

        movie_names = movies_df['movieTitle'].replace(" ","_",regex=True)

        # print(movie_names)
        # encoder = OneHotEncoder(sparse_output=False,handle_unknown='ignore')
        # encoder.fit(movie_names)
        single_row = data_to_process.iloc[0]
        # print(encoder.categories_)
        user_movie_names = data_to_process['movie_names'] #categorical data
        movies_crit_rating = data_to_process['movies_crit_rating'] #categorical data
        movies_years = data_to_process['movies_years'] #categorical data
        print(single_row['movies_critics_text_reviews'])
        print("#########################")
        print(single_row['movie_names'])


        array_movie_list = json.loads(user_movie_names.to_numpy())
        # print(array_movie_list)
        # print(type(array_movie_list))
        # print(type(array_movie_list[2]))
        # print(array_movie_list[2])
        #
        # array_movies_crit_rating = json.loads(movies_crit_rating)
        # print(type(array_movies_crit_rating))
        # print(type(array_movies_crit_rating[1]))
        # print(array_movies_crit_rating[2])

        array_movies_years = json.loads(array_movie_list)

        movies_critics_text_reviews = single_row['movies_critics_text_reviews']

        # print(" movies critics text reviews : ", movies_critics_text_reviews)
        result_input = encoder.transform(array_movies_years)
        print("encoded values ", result_input)

#to do: figure out if data i properly extracted and if there is a way to extract it using pyarrow

    def validate_data_with_print(self, data_to_process : pd.DataFrame):
        for column in data_to_process.columns:
            print("column name : ", column, "values :", data_to_process[column].iloc[0],"")

