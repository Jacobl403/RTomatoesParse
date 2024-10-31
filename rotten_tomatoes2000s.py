import tensorflow as tf
import keras
import pandas as pd
import os

N_ROWS =2000
MOVIES_CSV_PATH = 'data_sets\\rotten_tomatoes_Essential_2000s_Movies\\movies.csv\\movies.csv'
CRITIC_REVIEWS_CSV_PATH =  'data_sets\\rotten_tomatoes_Essential_2000s_Movies\\critic_reviews.csv\\critic_reviews.csv'
USER_REVIEWS_CSV_PATH =  'data_sets\\rotten_tomatoes_Essential_2000s_Movies\\user_reviews.csv\\user_reviews.csv'

def initRt2000s():
    df_movies = pd.read_csv(MOVIES_CSV_PATH,nrows=N_ROWS)
    df_critic_reviews = pd.read_csv(CRITIC_REVIEWS_CSV_PATH,nrows=N_ROWS)
    df_user_reviews = pd.read_csv(USER_REVIEWS_CSV_PATH,nrows=N_ROWS)
    # print("movies\n")
    # print(df_movies.dtypes)
    # print("\n critic_rev \n")
    # print(df_critic_reviews.dtypes)
    # print("\n user_rev \n")
    # print(df_user_reviews.dtypes)
    #
    # print(" \n movies v\n")
    # print(df_movies.iloc[0])
    # print("\n critic_rev  v\n")
    # print(df_critic_reviews.iloc[0])
    # print("\n user_rev v \n")
    # print(df_user_reviews.iloc[0])
    make_new_users_pd(df_user_reviews,df_critic_reviews,df_movies)


def make_new_users_pd(df_users,df_critic_reviews,df_movies):
    df_new = pd.DataFrame()
    df_meta_data = pd.DataFrame()
    if os.path.isfile('kappa.csv') is False:
        for user_id in df_users['userId']:
            user_subset = df_users[df_users['userId'] == user_id]
            if user_subset.empty is True:
                continue
            # print(user_subset)
            df_users = df_users.drop(index=user_subset.index)

            """tutaj musze dropowac jeden film i w y dac positive / negative /medieocere bazujac na ocenie użytkownika. Są dwie opcje:
            1. użytkownik ma kilka filmow i dropuje jeden randomowo
            2. użytkownik ma tylko 1 film 
            """
            number_of_indexs = len(user_subset)
            if number_of_indexs == 1:
                continue
            # pick recommended movie
            recommended_movie = user_subset.sample(1)
            user_subset = user_subset.drop(index=recommended_movie.index)

            movie_names = []

            #tutaj musze wypeniac nowy df
            for movieId in user_subset['movieId']:
                movie_info = df_movies[df_movies['movieId'].str.match(movieId)]
                critic_subset = df_critic_reviews[df_critic_reviews['movieId'].str.match(movieId)]
                critics_text_reviews = critic_subset['quote']
                critic_score = movie_info['critic_score']

            new_row = {'userId': user_id, 'selecedMovie': recommended_movie['movieTitle'].iloc[0], }
                #todo: stworzyc nowy dataFrame i go zapisać 
                # print(critic_subset)



