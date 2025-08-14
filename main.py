import time

import pandas as pd

import data_parser as dp
import  preproccesor_examples as pe
from preproccesor_examples import KerasTextVectorizer


#project name :HasbeMovie

# Download latest version
def init():
    # CsvFileHelper.wipe_out_dir()
    test = dp.DataParser()
    start = time.time()
    test.run()
    end = time.time()
    print("done saving data to test.csv. Executed in {} ... \n".format(float(end - start)))


if __name__ == '__main__':
    # init() #do not run leave data with 2 values
    # PreprocessData().preprocess()
    # user = CsvFileHelper.get_user_reviews_df()
    word_2_vec = pe.Word2vector_vectorizer(use_gem_version=True)
    keras_text_vec = KerasTextVectorizer()
    vocab1=word_2_vec.get_vocab()
    vocab2=keras_text_vec.get_vocab()
    print("vocab of word_2_vec: \n",vocab1)
    print("vocab of text_vec: \n",vocab2)
    print("size of vocab word_2_vec",len(vocab1))
    print("size of vocab text_vec",len(vocab2))
    #todo: find proper data in keagle to use/ systemize data to make it clear what is used/ keep track on which data is used and save it to md or notion
    #todo: can also have a lazy day in which i create repository with all design patterns




# URI = "https://www.rottentomatoes.com/m/madame_web"
#
# reviewsAttr = "/reviews"
#
# topCriticsAttr = "/reviews?type=top_critics"
#
# allAudienceAttr = "/reviews?type=user"
#
# verifiedAudience = "/reviews?type=verified_audience"
