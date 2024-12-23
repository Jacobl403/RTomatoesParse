# import tensorflow as tf
# import keras
# import pandas as pd
# import os
# import kagglehub
# import re
# import time
# import threading
# N_ROWS =20000
# DB_PATH ='data_sets\\rotten_tomatoes_Essential_2000s_Movies'
# MOVIES_CSV_PATH = '\\movies.csv\\movies.csv'
# CRITIC_REVIEWS_CSV_PATH =  '\\critic_reviews.csv\\critic_reviews.csv'
# USER_REVIEWS_CSV_PATH = '\\user_reviews.csv\\user_reviews.csv'

# """ todo: it is possible that df_test['Btime'].iloc[0] that can be depracated
#     it should be changed df.iloc[0, df.columns.get_loc('Btime')] = x (recommended)
# """

# LOCK = threading.Lock()
# df_movies = pd.read_csv(DB_PATH + MOVIES_CSV_PATH, nrows=N_ROWS)
# df_critic_reviews = pd.read_csv(DB_PATH + CRITIC_REVIEWS_CSV_PATH, nrows=N_ROWS)
# df_user_reviews = pd.read_csv(DB_PATH + USER_REVIEWS_CSV_PATH, nrows=N_ROWS)
# def initRt2000s():
#     # path = kagglehub.dataset_download("bwandowando/rotten-tomatoes-essential-2000s-movies")
#     # print('Path to MOVIES_CSV_PATH {}'.format( path+MOVIES_CSV_PATH))
#     # print("Path to CRITIC_REVIEWS_CSV_PATH:", path+CRITIC_REVIEWS_CSV_PATH)
#     # print("Path to USER_REVIEWS_CSV_PATH:", path+USER_REVIEWS_CSV_PATH)
#     print("movies\n")
#     print(df_movies.dtypes)
#     print("\n critic_rev \n")
#     print(df_critic_reviews.dtypes)
#     print("\n user_rev \n")
#     print(df_user_reviews.dtypes)

#     print(" \n movies v\n")
#     print(df_movies.iloc[0])
#     print("\n critic_rev  v\n")
#     print(df_critic_reviews.iloc[0])
#     print("\n user_rev v \n")
#     print(df_user_reviews.iloc[0])

#     start = time.time()
#     make_new_users_pd(df_user_reviews,df_critic_reviews,df_movies)
#     end = time.time()
#     print("done saving data to test.csv. Executed in {} ... \n".format(float(end - start)))


# def make_new_users_pd(df_users,df_critic_reviews,df_movies):
#     df_users_with_movies = pd.DataFrame()
#     df_meta_data = pd.DataFrame()
    
#     if os.path.isfile('kappa.csv') is False:
#         print("Starting to modify data for new csv ... \n")
#         thread1 = threading.Thread(target=add_user_to_new_pd,
#                                    args=(df_user_reviews, df_critic_reviews ,df_movies, df_users_with_movies ,df_meta_data))
#         thread2 = threading.Thread(target=add_user_to_new_pd,
#                                    args=(df_user_reviews, df_critic_reviews, df_movies, df_users_with_movies, df_meta_data))
#         thread3 = threading.Thread(target=add_user_to_new_pd,
#                                    args=(df_user_reviews, df_critic_reviews, df_movies, df_users_with_movies, df_meta_data))
#         thread4 = threading.Thread(target=add_user_to_new_pd,
#                                    args=(df_user_reviews, df_critic_reviews, df_movies, df_users_with_movies, df_meta_data))
#         thread1.start()
#         thread2.start()
#         thread3.start()
#         thread4.start()
#         thread1.join()
#         thread2.join()
#         thread3.join()
#         thread4.join()
#     df_users_with_movies.to_csv('test.csv')


# def add_user_to_new_pd(df_users : pd.DataFrame , df_critic_reviews , df_movies,df_users_with_movies,df_meta_data ):
#     for user_id in df_users['userId']:
#         with LOCK:
#             user_subset = df_users[df_users['userId'] == user_id]
#             print("Thread {} is working on {} \n".format(threading.get_ident(), user_id))
#             df_users = df_users.drop(index=user_subset.index)
#         if user_subset.empty is True:
#             continue
#         """tutaj musze dropowac jeden film i w y dac positive / negative /medieocere bazujac na ocenie użytkownika. Są dwie opcje:
#         1. użytkownik ma kilka filmow i dropuje jeden randomowo
#         2. użytkownik ma tylko 1 film 
#         """
#         number_of_indexs = len(user_subset)
#         if number_of_indexs == 1:
#             continue
#         # pick recommended movie and fill data
#         rec_movie = user_subset.sample(1)
#         rec_movie_info = df_movies[df_movies['movieId'].str.match(rec_movie['movieId'].iloc[0])]
#         # todo: consider adding here critic and user comments
#         rec_movie_dic = {'rec_title': rec_movie_info['movieTitle'].iloc[0],
#                          'rec_mean_crit_score': evaluate_mean_avg_score(rec_movie_info['critic_score'].iloc[0],
#                                                                         is_critic=True),
#                          'rec_mean_user_score': evaluate_mean_avg_score(rec_movie_info['audience_score'].iloc[0]),
#                          'rec_user_verdict': evaluate_user_verdict(rec_movie)}

#         # drop recomended movie
#         user_subset = user_subset.drop(index=rec_movie.index)

#         movies_names = []
#         movies_years = []
#         movies_crit_rating = []
#         movies_users_rating = []
#         all_movies_critics_text_reviews = []
#         all_movie_user_text_review = []
#         # tutaj musze wypeniac nowy df
#         for movieId in user_subset['movieId']:
#             movie_info = df_movies[df_movies['movieId'].str.match(movieId)]
#             movie_name = str(movie_info['movieTitle'].iloc[0])
#             movie_year = int(movie_info['movieYear'].iloc[0])
#             movie_crit_rating = evaluate_mean_avg_score(movie_info['critic_score'].iloc[0], True)
#             movie_user_rating = evaluate_mean_avg_score(movie_info['audience_score'].iloc[0])
#             critic_subset = df_critic_reviews[df_critic_reviews['movieId'].str.match(movieId)]
#             critics_text_reviews = critic_subset['quote'].tolist()

#             movies_names.append(movie_name)
#             movies_years.append(movie_year)
#             movies_crit_rating.append(movie_crit_rating)
#             movies_users_rating.append(movie_user_rating)
#             all_movies_critics_text_reviews.append(critics_text_reviews)

#         # print(type(rec_movie))

#         new_row = {'user_id': user_id, 'rec_title': rec_movie_dic['rec_title'],
#                    'rec_mean_crit_score': rec_movie_dic['rec_mean_crit_score'],
#                    'rec_mean_user_score': rec_movie_dic['rec_mean_user_score'],
#                    'movie_names': movies_names, 'movies_years': movies_years,
#                    'movies_crit_rating': movies_crit_rating, 'movies_users_rating': movies_users_rating,
#                    'movies_critics_text_reviews': all_movies_critics_text_reviews,
#                    'user_prev_text_reviews': user_subset['quote'].tolist(),
#                    'rec_user_verdict': rec_movie_dic['rec_user_verdict']}
#         df_users_with_movies = pd.concat([df_users_with_movies, pd.DataFrame.from_records(new_row)])
#         print("Thread {} has added new row  df_users size {} \n".format(threading.get_ident(),df_users.size))
# def evaluate_user_verdict(rec_movie):
#     user_verdict = rec_movie['rating'].iloc[0]
#     if 0 <= user_verdict < 3.0:
#         return 'Negative'
#     if 3.0 <= user_verdict < 3.5:
#         return 'Mediocre'
#     if 3.5 <= user_verdict <= 5.0:
#         return 'Positive'

# #todo: not sure if i should adjust some points since ex:79% is equal to 3.9 which dosent look like compareble verdict
# #also adjust critic score
# def evaluate_mean_avg_score(proc_str : str, is_critic =False):
#     proc_str = re.sub('[%]','',proc_str)
#     result = (float(proc_str) / 10.0)/ 2.0
#     if is_critic is True:
#         return result * 1.5
#     return result

# # breakpoint_here= True
# # if breakpoint_here is True:
# #     break