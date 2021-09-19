

import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

data = pd.read_csv('balanced_reviews.csv')

data.dropna(inplace=True)

data = data[data['overall'] != 3]

data['Positivity'] = np.where(data['overall'] > 3, 1, 0)

data['Positivity'].value_counts()

features_train, features_test, labels_train, labels_test = train_test_split(
    data['reviewText'], data['Positivity'], random_state=42)

# Using TF-IDF Vectorizer
vect = TfidfVectorizer(min_df=5).fit(features_train)

features_train_vectorized = vect.transform(features_train)

model = LogisticRegression()
model.fit(features_train_vectorized, labels_train)

predictions = model.predict(vect.transform(features_test))

confusion_matrix(labels_test, predictions)

roc_auc_score(labels_test, predictions)

pkl_filename = 'model_files/trained_model.pkl'
vocab_filename = 'model_files/vocab.pkl'

# Writing model to pickle file
with open(pkl_filename, 'wb') as file:
    pickle.dump(model, file)

# Saving TF-IDF vocabulary
with open(vocab_filename, 'wb') as file:
    pickle.dump(vect.vocabulary_, file)
