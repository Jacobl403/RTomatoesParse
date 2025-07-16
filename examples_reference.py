import kagglehub
import tensorflow as tf
import keras
import numpy as np
import gensim
from sklearn.preprocessing import OneHotEncoder
from util import CsvFileHelper

import pandas as pd
from sentence_transformers import SentenceTransformer

def init_examples():
    (train_images, train_labels), (test_images, test_labels) = tf.keras.datasets.mnist.load_data()
    print(train_images[:1].reshape(-1, 28 * 28) / 255.0)
    model = keras.Sequential([
        keras.layers.Dense(512, activation='relu', input_shape=(784,)),
        keras.layers.Dropout(0.2),
        keras.layers.Dense(10)
    ])

    model.compile(optimizer='adam',
                  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=[keras.metrics.SparseCategoricalAccuracy()])

    model.summary()
    # keras.utils.plot_model(model, to_file='model_1.png', show_shapes=True)
    print(model.get_state_tree())


def show_layer_values(x):
    
    tf.print(x)
    return x


def more_examples():
    # I want to have model where there is an input layer / GRU / LSTM / dropout / dense
    MOVIES_CSV_PATH_LINUX = '/movies.csv/movies.csv'
    MOVIES_CSV_PATH = '\\movies.csv\\movies.csv'
    path = kagglehub.dataset_download("bwandowando/rotten-tomatoes-essential-2000s-movies")
    df_movies = pd.read_csv(path + MOVIES_CSV_PATH_LINUX)
    all_movies = df_movies['movieTitle'].values.reshape(1,-1)

    encoder = OneHotEncoder(sparse_output=False,handle_unknown='ignore')
    encoder.fit(all_movies)
    single_df = CsvFileHelper.get_df_from_out_files()


    # text values
    user_previous_rev = single_df['user_prev_text_reviews']  # single list of values
    movie_crit_rev = single_df['movies_critics_text_reviews']  # 2d list of values  | I should resolve issue
    movie_names = single_df['movie_names']  # single list of values

    numerical_feathers = single_df[['movies_crit_rating','movies_users_rating','movies_years','rec_mean_crit_score']] # keras.layers.Normalization
    categorical_feathers = single_df[['movie_names']] #not included for now
    text_feathers = single_df[['movies_critics_text_reviews','user_prev_text_reviews']]
    print(categorical_feathers._values)
    # categorical_input = encoder.transform(categorical_feathers.values)
    # print(encoder.categories_)
    # print(categorical_input)

    # print(numerical_input)
    #I can test with only TextVectorization and Numerical
    # x = keras.layers.Normalization(axis=-1).adapt(numerical_input)
    # model = SentenceTransformer("all-mpnet-base-v2")
    # model.encode(user_previous_rev)

    #     # testowanko = SBERTVectorizer().transform_fit(movie_names)
    #
    # print(testowanko)
    #
    # res = movie_crit_rev.apply(lambda x: str(x).replace('[', '').replace(']', '').replace('\\', ''))  # should be moved to create
    # print(movie_crit_rev[0]) # need to be sanitize / single element in array
    # print(user_previous_rev.to_list())
    #tdifd
    # print(movie_names)

    # sample_data = np.random.rand(1, 10, 255)
    # inputs = keras.layers.Input(shape=(10,255))
    # print(sample_data.shape[0]," ",sample_data.shape[1]," ",sample_data.shape[2])
    # x = keras.layers.GRU(units=20,return_sequences=True)(inputs)
    # print(x[1])
    # x = keras.layers.LSTM(units=20)(x)
    # x = keras.layers.Dense(units=10, activation="softmax")(x)

    # model = keras.Sequential(x)
    # model.compile()
    # print(model.get_state_tree())
    # model(x)
    # i want to see what is possibility of parsing float/object/string data

def looking_into_pd():

    MOVIES_CSV_PATH_LINUX = '/movies.csv/movies.csv'
    CRITIC_REVIEWS_CSV_PATH_LINUX = '/critic_reviews.csv/critic_reviews.csv'
    USER_REVIEWS_CSV_PATH_LINUX = '/user_reviews.csv/user_reviews.csv'
    path = kagglehub.dataset_download("bwandowando/rotten-tomatoes-essential-2000s-movies")
    df_movies = pd.read_csv(path + MOVIES_CSV_PATH_LINUX)
    df_critic_reviews = pd.read_csv(path + CRITIC_REVIEWS_CSV_PATH_LINUX)
    df_user_reviews = pd.read_csv(path + USER_REVIEWS_CSV_PATH_LINUX)
    print(df_movies['movieTitle'].values)
    print()
    print()


"""below is example of  tensorflow tutorial on NLP processing"""
# critics_review_str = str(self._data_to_process['movies_critics_text_reviews'].iloc[0])
# vocab = sorted(set(critics_review_str))
# print('Size of vocab : ', len(vocab), ' vocab : ', vocab)
# # think about removing [, $ and other unnecessary chars  ]
# ids_from_chars = ks.layers.StringLookup(mask_token=None, vocabulary=(list(vocab)))
# chars_from_id = ks.layers.StringLookup(invert=True, vocabulary=ids_from_chars.get_vocabulary())
#
# slices = tf.strings.unicode_split(critics_review_str, "UTF-8")
# all_ids = ids_from_chars(slices)
# print("All Ids : ", all_ids)
# ids_dataset = tf.data.Dataset.from_tensor_slices(all_ids)
# print('example of ids_dataset', ids_dataset.take(1).as_numpy_iterator().next())
# batch_size = 101
# sequences = ids_dataset.batch(batch_size, drop_remainder=True)
#
# split_input_text = lambda sequence: (sequence[:-1], sequence[1:])

# val = split_input_text(sequences.take(1)).index(0)