from  sentence_transformers import SentenceTransformer
from  .text_preprocessorI import TextPreprocessorI


class SBERTVectorizer(TextPreprocessorI):

    def __int__(self,model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)

    def transform_fit(self, text: list):
        print("SBERTVectorizer textPreprocess transform_fit for list called ...")
        embeddings = self.model.encode(text,convert_to_numpy=True)
        return embeddings

    def get_model(self):
        return self.model