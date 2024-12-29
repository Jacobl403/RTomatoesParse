import numpy as np
import pandas as pd
import kagglehub
import re
import threading
import multiprocessing
from util import CsvFileHelper

N_ROWS = 2000
NUMBER_OF_THREADS = 4
DB_PATH = 'data_sets\\rotten_tomatoes_Essential_2000s_Movies'
MOVIES_CSV_PATH = '\\movies.csv\\movies.csv'
CRITIC_REVIEWS_CSV_PATH = '\\critic_reviews.csv\\critic_reviews.csv'
USER_REVIEWS_CSV_PATH = '\\user_reviews.csv\\user_reviews.csv'

MOVIES_CSV_PATH_LINUX = '/movies.csv/movies.csv'
CRITIC_REVIEWS_CSV_PATH_LINUX = '/critic_reviews.csv/critic_reviews.csv'
USER_REVIEWS_CSV_PATH_LINUX = '/user_reviews.csv/user_reviews.csv'

    # path = kagglehub.dataset_download("bwandowando/rotten-tomatoes-essential-2000s-movies")
    # print('Path to MOVIES_CSV_PATH {}'.format( path+MOVIES_CSV_PATH))
    # print("Path to CRITIC_REVIEWS_CSV_PATH:", path+CRITIC_REVIEWS_CSV_PATH)
    # print("Path to USER_REVIEWS_CSV_PATH:", path+USER_REVIEWS_CSV_PATH)

class DataParser:
    def __init__(self):
        path = kagglehub.dataset_download("bwandowando/rotten-tomatoes-essential-2000s-movies")
        print(path + MOVIES_CSV_PATH)
        # self.df_movies = pd.read_csv(path + MOVIES_CSV_PATH,nrows=N_ROWS)
        # self.df_critic_reviews = pd.read_csv(path + CRITIC_REVIEWS_CSV_PATH,nrows=N_ROWS)
        # self.df_user_reviews = pd.read_csv(path + USER_REVIEWS_CSV_PATH,nrows=N_ROWS)
        self.df_movies = pd.read_csv(path + MOVIES_CSV_PATH_LINUX,nrows=N_ROWS)
        self.df_critic_reviews = pd.read_csv(path + CRITIC_REVIEWS_CSV_PATH_LINUX,nrows=N_ROWS)
        self.df_user_reviews = pd.read_csv(path + USER_REVIEWS_CSV_PATH_LINUX,nrows=N_ROWS)
        self.df_users_with_movies = pd.DataFrame()
        self.df_meta_data = pd.DataFrame()


    def prepeare_and_create(self):
        thread_list = []
        user_sets = list(set(self.df_user_reviews['userId']))
        step = int(len(user_sets) / NUMBER_OF_THREADS)
        adjust_step = len(user_sets) % NUMBER_OF_THREADS
        for i in range(NUMBER_OF_THREADS):
            if i < NUMBER_OF_THREADS - 1:
                thread_list.append(
                    multiprocessing.Process(target=self.add_user_to_new_pd, args=(user_sets[i * step:(i + 1) * step],)))
            else:
                thread_list.append(
                    multiprocessing.Process(target=self.add_user_to_new_pd,
                                     args=(user_sets[(i - 1) * step: i * step + adjust_step],)))

    def run(self):
        user_sets = np.array(list(set(self.df_user_reviews['userId'])))
        print(type(user_sets))
        user_sets_array = np.array_split(user_sets,4)
        print(user_sets_array)

        with multiprocessing.Pool(4) as p:
            print(p.map(self.add_user_to_new_pd, user_sets_array))

        print(" \n ended all process  \n")

    def add_user_to_new_pd(self, user_set):
        print('thread {} started user set {}'.format(threading.get_ident(), len(user_set)))
        df_users_with_movies = pd.DataFrame()
        for user_id in user_set:
            user_subset = self.df_user_reviews[self.df_user_reviews['userId'] == user_id]
            # self.df_user_reviews = self.df_user_reviews.drop(index=user_subset.index)
            if user_subset.empty is True:
                continue
            """tutaj musze dropowac jeden film i w y dac positive / negative /medieocere bazujac na ocenie użytkownika. Są dwie opcje:
            1. użytkownik ma kilka filmow i dropuje jeden randomowo
            2. użytkownik ma tylko 1 film 
            """
            number_of_indexs = len(user_subset)
            if number_of_indexs <= 1:
                continue
            # pick recommended movie and fill data
            rec_movie = user_subset.sample(1)
            rec_movie_info = self.df_movies[self.df_movies['movieId'].str.match(rec_movie['movieId'].iloc[0])]
            # todo: consider adding here critic and user comments
            rec_movie_dic = {'rec_title': rec_movie_info['movieTitle'].iloc[0],
                             'rec_mean_crit_score': self.evaluate_mean_avg_score(rec_movie_info['critic_score'].iloc[0],
                                                                                 is_critic=True),
                             'rec_mean_user_score': self.evaluate_mean_avg_score(
                                 rec_movie_info['audience_score'].iloc[0]),
                             'rec_user_verdict': self.evaluate_user_verdict(rec_movie)}

            # drop recomended movie
            user_subset = user_subset.drop(index=rec_movie.index)

            movies_names = []
            movies_years = []
            movies_crit_rating = []
            movies_users_rating = []
            all_movies_critics_text_reviews = []
            all_movie_user_text_review = []
            # tutaj musze wypeniac nowy df
            for movieId in user_subset['movieId']:
                movie_info = self.df_movies[self.df_movies['movieId'].str.match(movieId)]
                movie_name = str(movie_info['movieTitle'].iloc[0])
                movie_year = int(movie_info['movieYear'].iloc[0])
                movie_crit_rating = self.evaluate_mean_avg_score(movie_info['critic_score'].iloc[0], True)
                movie_user_rating = self.evaluate_mean_avg_score(movie_info['audience_score'].iloc[0])
                critic_subset = self.df_critic_reviews[self.df_critic_reviews['movieId'].str.match(movieId)]
                critics_text_reviews = critic_subset['quote'].tolist()

                movies_names.append(movie_name)
                movies_years.append(movie_year)
                movies_crit_rating.append(movie_crit_rating)
                movies_users_rating.append(movie_user_rating)
                all_movies_critics_text_reviews.append(critics_text_reviews)

            # print(type(rec_movie))

            new_row = {'user_id': user_id, 'rec_title': rec_movie_dic['rec_title'],
                       'rec_mean_crit_score': rec_movie_dic['rec_mean_crit_score'],
                       'rec_mean_user_score': rec_movie_dic['rec_mean_user_score'],
                       'movie_names': movies_names, 'movies_years': movies_years,
                       'movies_crit_rating': movies_crit_rating, 'movies_users_rating': movies_users_rating,
                       'movies_critics_text_reviews': all_movies_critics_text_reviews,
                       'user_prev_text_reviews': user_subset['quote'].tolist(),
                       'rec_user_verdict': rec_movie_dic['rec_user_verdict']}
            df_users_with_movies = pd.concat([df_users_with_movies, pd.DataFrame.from_records(new_row)])

        CsvFileHelper.save_data_frame(df_users_with_movies,threading.get_ident())
        print('thread {} ended   \n'.format(threading.get_ident()))

    def evaluate_user_verdict(self, rec_movie):
        user_verdict = rec_movie['rating'].iloc[0]
        if 0 <= user_verdict < 3.0:
            return 'Negative'
        if 3.0 <= user_verdict < 3.5:
            return 'Mediocre'
        if 3.5 <= user_verdict <= 5.0:
            return 'Positive'

    # todo: not sure if i should adjust some points since ex:79% is equal to 3.9 which dosent look like compareble verdict
    # also adjust critic score
    def evaluate_mean_avg_score(self, proc_str: str, is_critic=False):
        proc_str = re.sub('[%]', '', proc_str)
        result = (float(proc_str) / 10.0) / 2.0
        if is_critic is True:
            return result * 1.5
        return result

    # breakpoint_here= True
    # if breakpoint_here is True:
    #     break
