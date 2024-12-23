import time

import pandas as pd
import examples_reference as er
import rotten_tomatoes2000s as rt
import data_parser as dp
# Download latest version
def init():
    # csv = pd.read_csv('data_sets\\movies_dataset.csv', nrows=20000)
    #
    # print(csv)
    pass

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # init()
    # er.init_examples()
    # rt.initRt2000s()
    test = dp.DataParser()
    start = time.time()
    test.run()
    end = time.time()
    print("done saving data to test.csv. Executed in {} ... \n".format(float(end - start)))







# URI = "https://www.rottentomatoes.com/m/madame_web"
#
# reviewsAttr = "/reviews"
#
# topCriticsAttr = "/reviews?type=top_critics"
#
# allAudienceAttr = "/reviews?type=user"
#
# verifiedAudience = "/reviews?type=verified_audience"
