
from util import CsvFileHelper

from sentence_transformers import SentenceTransformer

""" 
this one will probably not be used since there is little to no gain from it in project 
to install require pip install -U sentence-transformers https://sbert.net/
pip install torch torchvision torchaudio
pip install transformers
pip install sentence-transformers
pip install accelerate
"""
class SBERTVectorizer:

    def __init__(self):
        """ all posible models https://sbert.net/docs/sentence_transformer/pretrained_models.html
        all-MiniLM-L6-v2 version has dimension of (382,0)
        it's more of correlation between text not sure if i gonna use it for text input the only application can be for
        movies titles since it always produce (382,0) dim vector
        """
        self.model_name = "all-MiniLM-L6-v2"
        self.model = SentenceTransformer('all-MiniLM-L6-v2',device=None, trust_remote_code=False)
        self.data_to_process = CsvFileHelper.get_df_from_out_files()

    def __call__(self, *args, **kwargs):
        critics_reviews = self.data_to_process['movies_critics_text_reviews']
        embedings =self.model.encode(critics_reviews)
        print(f'###### embedings shape #####\n {embedings.shape}')
        print(f' embedings \n {embedings}')

