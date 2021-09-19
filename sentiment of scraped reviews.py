import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

df=pd.read_csv("etsy_reviews.csv")



df["Sentiment"]=""
df=df.iloc[:,1:]

def check_review(reviewtext):
    '''
    Check the review is positive or negative'''
    file = open("pickle_model.pkl", 'rb')
    pickle_model = pickle.load(file)
    file_1 = open("feature.pkl", 'rb')
    vocab = pickle.load(file_1)
    #reviewText has to be vectorised, that vectorizer is not saved yet
    #load the vectorize and call transform and then pass that to model preidctor
    #load it later
    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    vectorised_review = transformer.fit_transform(loaded_vec.fit_transform([reviewtext]))
    # Add code to test the sentiment of using both the model
    # 0 == negative   1 == positive
    out = pickle_model.predict(vectorised_review)
    return out[0]

for i in range(7692):
    a=df["reviews"][i]
    n=check_review(a)
    df["Sentiment"][i]=n

df.to_csv("Final_Etsy_Screapped_Reviews.csv",index=False)