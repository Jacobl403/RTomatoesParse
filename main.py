import time

import pandas as pd

import data_parser as dp
import examples_reference
from preprocessdata import PreprocessData
from util import CsvFileHelper

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
    PreprocessData().preprocess()
    # user = CsvFileHelper.get_user_reviews_df()

    # print(type(CsvFileHelper.SCHEMA))
    # examples_reference.more_examples()
    # examples_reference.looking_into_pd()






# URI = "https://www.rottentomatoes.com/m/madame_web"
#
# reviewsAttr = "/reviews"
#
# topCriticsAttr = "/reviews?type=top_critics"
#
# allAudienceAttr = "/reviews?type=user"
#
# verifiedAudience = "/reviews?type=verified_audience"
