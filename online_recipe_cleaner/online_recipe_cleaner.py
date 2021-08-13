import streamlit as st
import sys
import random
import requests
import string
from bs4 import BeautifulSoup
import csv
from numpy import genfromtxt
import online_funcs
import pandas as pd
import pickle

#from nltk.stem import PorterStemmer
#from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

ingredients_model = pickle.load(open("ingredients_model.pkl","rb"))
ingredients_cv = pickle.load(open("ingredients_vectorizer.pkl","rb"))

instructions_model = pickle.load(open("instructions_model.pkl","rb"))
instructions_cv = pickle.load(open("instructions_vectorizer.pkl","rb"))





def main():

	# Use the full page instead of a narrow central column
	st.set_page_config(layout="wide")

	st.title("Recipe Cleaner")

	st.subheader("An A.I. powered app designed to bypass food blogs and generate an easy-to-follow recipe.")
	st.write("Harrison Sims")

	col1, col2 = st.beta_columns((3,1))


	with col1:
		web_address=st.text_input("Recipe web address:")


	with col2:
		st.write(" ")
		st.write(" ")
		clean_command = st.button("Clean!")

	col3, col4 = st.beta_columns(2)


	if clean_command:
		# Now need to pull in section list from the webpage and generate the vector for each section
		section_list, section_list_prettify = online_funcs.get_section_list(web_address)
		section_matrix = []

		for section in section_list:
		    # = Editting the section to have no punctuation, use stemming be form a list =
		    # ============================================================================
		    final_section_text = online_funcs.process_section(section)
		    section_matrix.append(final_section_text)

		ingredients_record_score = 0.0
		instructions_record_score = 0.0
		section_count = 0
		ingredient_element_number = -1
		instructions_element_number = -1

		for section in section_matrix:

			if(len(section) >= 5):

				section_temp = [word for word in section if not word in stopwords.words('english')]
				section_sub = online_funcs.listToString(section_temp)
				section_test = [section_sub]

				ingredients_section_vector = ingredients_cv.transform(section_test)
				ingredients_prediction = ingredients_model.predict_proba(ingredients_section_vector)

				instructions_section_vector = instructions_cv.transform(section_test)
				instructions_prediction = instructions_model.predict_proba(instructions_section_vector)

				# For diagnosing when it doesn't work
				# if instructions_prediction[0,1] >= 0.90:
				# 	print("==== "+str(instructions_prediction[0,1])+" ====")
				# 	print(section_test)
				# 	print("")

				if ingredients_prediction[0,1] >= ingredients_record_score:
					ingredients_record_score = ingredients_prediction[0,1]
					ingredient_element_number = section_count

				if instructions_prediction[0,1] >= instructions_record_score:
					instructions_record_score = instructions_prediction[0,1]
					instructions_element_number = section_count


			section_count+=1


		with col3:
			if ingredients_record_score >= 0.3:
				st.subheader("Ingredients")
				st.success("Score = "+str(ingredients_record_score*100.)+" %")
				st.write("")
				for i in online_funcs.format_section(section_list_prettify[ingredient_element_number]):
					if i.isspace() == False and len(i) > 0:
						st.write("-- "+str(i))
			else:
				st.error("        ***WARNING***")
				st.write(" ")
				st.error(" cannot identify ingredients with certainty")
				st.error(" Score = "+str(ingredients_record_score*100.)+" %")
				st.write("")
				for j in online_funcs.format_section(section_list_prettify[ingredient_element_number]):
					if j.isspace() == False and len(j) > 0:
						st.write("-- "+str(j))

		with col4:
			if instructions_record_score >= 0.3:
				st.subheader("Instructions")
				st.success("Score = "+str(instructions_record_score*100.)+" %")
				st.write("")
				for k in online_funcs.format_section(section_list_prettify[instructions_element_number]):
					if k.isspace() == False and len(k) > 0:
						st.write("-- "+str(k))
			else:
				st.error("        ***WARNING***")
				st.write(" ")
				st.error(" cannot identify instructions with certainty")
				st.error(" Score = "+str(instructions_record_score*100.)+" %")
				st.write("")
				for l in online_funcs.format_section(section_list_prettify[instructions_element_number]):
					if l.isspace() == False and len(l) > 0:
						st.write("-- "+str(l))


main()