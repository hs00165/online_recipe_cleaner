# Import the modules
import sys
import random
import requests
import string
from bs4 import BeautifulSoup
import csv
from numpy import genfromtxt
import funcs
import pandas as pd
import pickle

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

cv = CountVectorizer()

data = pd.read_csv("../data/training_data_ingredients_file.csv", sep=',', header=None)
data.columns =['label', 'ingredients_score', 'url', 'section']


x = data['section']
y = data['label']


x = cv.fit_transform(x)


x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1)

model = MultinomialNB()

model.fit(x_train, y_train)

pickle.dump(model, open("ingredients_model.pkl","wb"))
pickle.dump(cv, open("ingredients_vectorizer.pkl","wb"))

print("Accuracy:      "+str(model.score(x_test,y_test)))

	



