# Import the modules
import sys
import random
import requests
from bs4 import BeautifulSoup
import string
import csv
from numpy import genfromtxt
import funcs
import online_funcs
from recipe_scrapers import scrape_me
from wordcloud import WordCloud

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')




import matplotlib.pyplot as plt

contents = funcs.word_cloud_list_gen()

# print(contents.split())

cleaned_contents = []

for word in contents.split():
	temp_string = online_funcs.clean_string_no_numbers(word)

	if temp_string != '':
		cleaned_contents.append(temp_string)


cleaned_contents = [word for word in cleaned_contents if not word in stopwords.words('english')]







test = ' '.join(cleaned_contents)

print(test)

wordcloud = WordCloud(width = 3000, height = 2500, random_state=1,background_color='white', colormap='Dark2').generate(test)


# lower max_font_size
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()

