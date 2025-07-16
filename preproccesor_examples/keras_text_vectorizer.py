from util import CsvFileHelper
from keras.src.layers import TextVectorization
import tensorflow as tf
import numpy as np
#kers_core.layers.StringLookup` can be used for categorical value

class KerasTextVectorizer:
    def __init__(self):
        #load file
        self.data_to_process = CsvFileHelper.get_df_from_out_files()
        """ get text features here: probably I will use tf_idf
        output_sequence_length is how many columns for single sentence
        ngrams =N (up to 3) used to catch correlation between words [probobly will not use it to MUCH resources are consumed]
        output_mode is type of vectorization? should be performed types: 'int', 'one_hot', 'multi_hot', 'count', 'tf_idf'
        pad_to_max_tokens if true then output columns will be padded to max_tokens=N
        for more info https://keras.io/api/layers/preprocessing_layers/text/text_vectorization/"""
        self.vectorizer = TextVectorization(output_mode='tf_idf')

    def __call__(self, *args, **kwargs):
        # get text features
        critics_reviews = self.data_to_process['movies_critics_text_reviews']
        self.vectorizer.adapt(critics_reviews)
        self.print_info()



    def for_learning_purpose(self):
        #check if vocabulary is correcly asigned
        self.print_info()
        #how to use info and how to check
        self.show_step_by_step_what_was_done()
        #check final data
        self.check_output_data_for_df_input()


    def print_info(self):
        vocab = self.vectorizer.get_vocabulary()
        weights = self.vectorizer.get_weights()
        config = self.vectorizer.get_config()
        build_config = self.vectorizer.get_build_config()

        print("########## Vocabulary  ######## \n", vocab)
        print("########## Vocabulary size  ######## \n", len(vocab))
        print("######## weights ########### \n", weights)
        print("######## config ########### \n", config)
        print("######## build_config ########### \n", build_config)
        # print("######## vectorizer_np ########### \n",vectorizer_np)

    """only applicable if you choose output_mode=int """
    def show_step_by_step_what_was_done(self):
        all_vocab = self.vectorizer.get_vocabulary()
        example_text = "This was an, amazing show ;can't wait to watch next / season pegx"
        #step 1 setialize / before this sanitizer can be used
        serialized_str = tf.strings.lower(example_text)
        print(serialized_str)
        #step 2 tokinize whole string
        tokenized = tf.strings.split(serialized_str)
        print(tokenized)
        #step 3 add indexes to words/ vectorize based on adapt data
        vectorized = self.vectorizer(tokenized)
        print(vectorized)
        #check index of each word
        indices = vectorized.numpy()
        print("indices \n",indices)
        print("decipher back to word \n", indices)
        deciphered_words = []
        for numb in indices:
            deciphered_words.append(all_vocab[numb[0]])
        print(deciphered_words)



    """this part was took from claudie ai"""
    def check_output_data_for_df_input(self):
        output_mode_option =self.vectorizer.get_config().get('output_mode')
        critics_reviews = self.data_to_process['movies_critics_text_reviews']
        if output_mode_option == "int":
            all_vocab = self.vectorizer.get_vocabulary()
            print("\n=== PROCESSING ALL SAMPLE TEXTS ===")
            all_vectorized = self.vectorizer(critics_reviews)
            for i, (text, vector) in enumerate(zip(critics_reviews, all_vectorized.numpy())):
                print(f"\nText {i + 1}: '{text}'")
                print(f"Vector: {vector}")

                # Show word mapping for this text
                words = []
                for idx in vector:
                    if idx < len(all_vocab) and idx > 0:
                        words.append(all_vocab[idx])
                    elif idx == 0:
                        words.append('[PAD]')
                print(f"Words: {words}")

        else:
            all_vectorized = self.vectorizer(critics_reviews)
            print("hello")
            print(all_vectorized)



