import numpy as np
from tf_keras.src.preprocessing.text import text_to_word_sequence
from util import CsvFileHelper
from gensim.models import Word2Vec
from itertools import zip_longest
"""

https://radimrehurek.com/gensim/models/word2vec.html
Version with gensim
output is word vec[size] representing each word with characteristics 

ATTENTION Here is a big todo: currently max columns is hardcoded to 1500 words, 
however there is a need to update this to be more dynamicly so it would be based on mean max size value and add zeros to existing ones
  
"""
class Word2vector_vectorizer:
    def __init__(self,use_gem_version=False):
        self._data_to_process = CsvFileHelper.get_df_from_out_files()
        self._model = self.__initialize_gem_model()
        self.HARD_CODED_MAX_SIZE =1500
    def __initialize_gem_model(self):
        print("Word2Vec model initialized ...")
        critics_reviews = self._data_to_process['movies_critics_text_reviews']
        # need to be in ['hello','world'] format rather than "hello world"
        self._sequences = [text_to_word_sequence(review) for review in critics_reviews]
        """Alternative you can use 
        return self.__example_of_setting_up_step_by_step(sequences)
        """
        return Word2Vec(sentences=self._sequences,vector_size=100,workers=4,min_count=1)

    def __call__(self, *args, **kwargs):
        self.__print_vectorizer_info()
        """
        #time consuming part
        preprocessed_not_optimized = self.__optimize_preprocess_data()
        preprocessed_mean_optimization = self.__optimize_preprocess_data(optimization='mean')
        preprocessed_value_optimization = self.__optimize_preprocess_data(optimization='value', sequence_size=1500)
        print(preprocessed_not_optimized.shape)
        print(preprocessed_mean_optimization.shape)
        print(preprocessed_value_optimization.shape)
        """


    def __optimize_preprocess_data(self, optimization=None, sequence_size=0):
        if optimization == 'value':
            sliced_sequences = [sequence if len(sequence) < sequence_size else sequence[:sequence_size] for sequence in self._sequences]
        elif optimization == 'mean':
            all_sizes = [len(sequence) for sequence in self._sequences]
            mean = np.mean(all_sizes, dtype='int')
            sliced_sequences = [sequence if len(sequence) < mean else sequence[:mean] for sequence in self._sequences]
        else:
            sliced_sequences = self._sequences
        sequences_list = [self._model.wv[sequence].reshape(-1) for sequence in sliced_sequences]
        """zip_longest works as classical zip ([1,2,3] [a,b] ) -> [[1,a],[2,b]] however it's adding extra fillvalue 
        so result looks like this  fillval=x ([1,2,3] [a,b] ) -> [[1,a],[2,b],[3,x]]
        transposition is doing the trick basically we fill rows then change rows to columns and vice versa
        
        np.pad(tmp_all,(0,max_size) ,mode='constant') was consider here but for some reason didn't work as planed
        """
        return np.array(list(zip_longest(*sequences_list, fillvalue=0))).T


    def __print_vectorizer_info(self):
        print("########### vocab ########## :",self._model.wv)
        print("########### VECTOR  SIZE ########## :",self._model.vector_size)
        print("########### vectors number of words ########## :",self._model.wv.vectors.shape[0])
        print("###########  vocab list ########## :",self._model.wv.index_to_key)

    def __example_of_setting_up_step_by_step(self,sequences):
        model_tmp = Word2Vec(vector_size=100, min_count=1)
        print("building vocab ...")
        model_tmp.build_vocab(sequences)
        print("Word2Vec training started ...")
        model_tmp.train(sequences)
        return model_tmp

    def get_vocab(self):
        return self._model.wv.index_to_key
    def __save_model(self):
        path = ""
        self._model.save(path)
    def load_model(self):
        path = ""
        self._model.load(path)
    def __user_defined_word_2_vec(self):
        pass
