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
import os

#from nltk.stem import PorterStemmer
#from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

path = os.path.dirname(__file__)
my_file = path+'/photo.png'

ingredients_model = pickle.load(open(path+"/ingredients_model.pkl","rb"))
ingredients_cv = pickle.load(open(path+"/ingredients_vectorizer.pkl","rb"))

instructions_model = pickle.load(open(path+"/instructions_model.pkl","rb"))
instructions_cv = pickle.load(open(path+"/instructions_vectorizer.pkl","rb"))





def main():

	# Use the full page instead of a narrow central column
	st.set_page_config(layout="wide")

	image_scores = []
	image_string = ""



	# Declaring the session_state variables
	if 'section_list_prettify_state' not in st.session_state:
	    st.session_state.section_list_prettify_state = []
	if 'cleaned_flag' not in st.session_state:
	    st.session_state.cleaned_flag = 0
	if 'ingredients_record_score' not in st.session_state:
	    st.session_state.ingredients_record_score = 0
	if 'instructions_record_score' not in st.session_state:
	    st.session_state.instructions_record_score = 0	
	if 'ingredient_element_number' not in st.session_state:
	    st.session_state.ingredient_element_number = 0
	if 'instructions_element_number' not in st.session_state:
	    st.session_state.instructions_element_number = 0	
	if 'image_list' not in st.session_state:
	    st.session_state.image_list = []
	if 'website_title_list' not in st.session_state:
	    st.session_state.website_title_list = []	
	if 'first_title' not in st.session_state:
	    st.session_state.first_title = []
	if 'displayed_image_number' not in st.session_state:
	    st.session_state.displayed_image_number = -1
	if 'access_denied_flag' not in st.session_state:
	    st.session_state.access_denied_flag = 0
	if 'section_model_matrix' not in st.session_state:
	    st.session_state.section_model_matrix = []
	if 'section_disp_matrix' not in st.session_state:
	    st.session_state.section_disp_matrix = []




	col1, col2, col3= st.columns((2.5,0.18,1))

	with col1:
		st.image(path+"/logo.PNG", width = 500)
		st.subheader("An A.I.-powered application designed to bypass food blogs and generate an easy-to-follow recipe.")
		st.write("By Harrison Sims")
		st.write("")
		st.write("")
		web_address=st.text_input("Recipe web address:")
		# debug_command = st.checkbox("Debug output to terminal?")
		st.write("")
		st.write("")


	with col2:
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		st.write("")
		clean_command = st.button("Clean!")
		
	if clean_command==False:
		with col3:
			st.image(path+"/Wordcloud.png", use_column_width=True)


	col5, col6 = st.columns(2)

	if clean_command and web_address:
		# Getting the Soup and images of the webpage
		st.session_state.displayed_image_number = -1
		soup, st.session_state.image_list = online_funcs.pull_webpage(web_address)

		# Now need to pull in section list from the webpage and generate the vector for each section
	

		st.session_state.cleaned_flag = 1
		st.session_state.currentImage = 0
		st.session_state.access_denied_flag = 0




		# # Step 1
		# section_list, section_list_prettify = online_funcs.get_section_list(soup)
		# st.session_state.section_list_prettify_state = section_list_prettify


		# IDEA!!!
		# Sometimes, different parts of the instructions are split up by header tags.
		# This makes my code think that it should treat them separately, and only select 
		# one part as the instructions. Obviously this is not great...
		# A solution:
		# IF there are no header tags within a header (eg, no h5 within h4)
		# AND there are a few of these headers in a row ( h4, h4, h4)
		# THEN creat another section that has these sections grouped together!
		# Note this sounds pretty difficult to implement...
		# To achieve this, just compare the current header with the last one:
		# if they are the same, try adding them together!




		# Generating the matix of sections for:
		# 1) The model to evaluate:   section_model_matrix
		# 2) To display to the user:  section_disp_matrix
		st.session_state.section_model_matrix, st.session_state.section_disp_matrix = online_funcs.TEMP_get_section_list(soup)


		# I see BS at this point...
		# for sect in st.session_state.section_model_matrix:
		# 	print(sect)


		# testy_final_prettify_section_list, testy_final_text_section_list = online_funcs.TEMP_get_section_list(soup)
		# print(len(testy_final_prettify_section_list))
		# print(len(testy_final_text_section_list))




		if len(st.session_state.section_model_matrix) <=5:
			st.session_state.access_denied_flag = 1

		# if debug_command:
		# 	print("")
		# 	print("      *** DEBUG OUTPUT ***       ")
		# 	print("")
		# 	print(soup.prettify())

		
		# section_matrix = []
		# for section in section_list:
		# 	# = Editting the section to have no punctuation, use stemming be form a list =
		# 	# ============================================================================
		# 	final_section_text = online_funcs.process_section(section)
		# 	section_matrix.append(final_section_text)
		# 	if debug_command:
		# 		print(final_section_text)

		st.session_state.ingredients_record_score = 0.0
		st.session_state.instructions_record_score = 0.0
		section_count = 0
		st.session_state.ingredient_element_number = -1
		st.session_state.instructions_element_number = -1

		st.session_state.website_title_list = online_funcs.get_title(soup)
		st.session_state.first_title = online_funcs.process_title(st.session_state.website_title_list[0])
		# print("*******")
		# print(st.session_state.website_title_list[0])
		# print(st.session_state.first_title)
		for section in st.session_state.section_model_matrix:

			# print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
			# print(section)

			if(len(section) >= 5) and len(online_funcs.listToString(section)) < 5000:

				# section_temp = [word for word in section if not word in stopwords.words('english')]
				section_sub = online_funcs.listToString(section)
				section_test = [section_sub]

				ingredients_section_vector = ingredients_cv.transform(section_test)
				ingredients_prediction = ingredients_model.predict_proba(ingredients_section_vector)

				instructions_section_vector = instructions_cv.transform(section_test)
				instructions_prediction = instructions_model.predict_proba(instructions_section_vector)

				# For diagnosing when it doesn't work
				# if instructions_prediction[0,1] >= 0.90:
				print("==== "+str(instructions_prediction[0,1])+" ===="+str(ingredients_prediction[0,1]))
				print(section_test)
				print("")

				if ingredients_prediction[0,1] >= st.session_state.ingredients_record_score:
					st.session_state.ingredients_record_score = ingredients_prediction[0,1]
					st.session_state.ingredient_element_number = section_count

				if instructions_prediction[0,1] >= st.session_state.instructions_record_score:
					st.session_state.instructions_record_score = instructions_prediction[0,1]
					st.session_state.instructions_element_number = section_count


			section_count+=1

	

	if st.session_state.cleaned_flag == 1:

		download_string = ' '.join(st.session_state.first_title) + "\n\n ========   Ingredients ========\n" 
		download_file_name = '_'.join(st.session_state.first_title)+'.txt'

		with col1:
			st.write("")
			st.write("")
			st.title(st.session_state.website_title_list[0])
			if st.session_state.access_denied_flag == 1:
				st.error("Uh oh... - Website access denied :(")
				st.write("Please try another website.")

		with col5:
			st.subheader("Ingredients")
			if st.session_state.ingredients_record_score >= 0.3:
				st.success("Succesfully identified the Ingredients.")
				st.success("Prediction score = "+str(st.session_state.ingredients_record_score*100.)+" %")
				st.write("")
				for i in st.session_state.section_disp_matrix[st.session_state.ingredient_element_number]:
					if i.isspace() == False and len(i) > 0:
						st.write("-- "+str(i))
						download_string = download_string +"\n-- "+str(i)
			else:
				if st.session_state.access_denied_flag == 0:
					st.error("***WARNING***: Cannot identify ingredients with certainty.")
					st.error("Prediction score = "+str(st.session_state.instructions_record_score*100.)+" %")
					st.write("")
					for j in st.session_state.section_disp_matrix[st.session_state.ingredient_element_number]:
						if j.isspace() == False and len(j) > 0:
							st.write("-- "+str(j))
							download_string = download_string +"\n-- "+str(j)

		with col6:
			st.subheader("Instructions")
			if st.session_state.instructions_record_score >= 0.3:
				st.success("Succesfully identified the Instructions.")
				st.success("Prediction score = "+str(st.session_state.instructions_record_score*100.)+" %")
				st.write("")
				download_string = download_string + "\n\n========   Instructions ========\n"
				for k in st.session_state.section_disp_matrix[st.session_state.instructions_element_number]:
					if k.isspace() == False and len(k) > 0:
						st.write("-- "+str(k))
						download_string = download_string +"\n-- "+str(k)
			else:
				if st.session_state.access_denied_flag == 0:
					st.error("***WARNING***: Cannot identify instructions with certainty.")
					st.error("Prediction score = "+str(st.session_state.instructions_record_score*100.)+" %")
					st.write("")
					download_string = download_string + "\n\n========   Instructions ========\n"
					for l in st.session_state.section_disp_matrix[st.session_state.instructions_element_number]:
						if l.isspace() == False and len(l) > 0:
							st.write("-- "+str(l))
							download_string = download_string +"\n-- "+str(l)



	with col3:

		if st.session_state.cleaned_flag == 1 and len(st.session_state.image_list) >= 1:

			nImages = len(st.session_state.image_list)
			
			image_score_record = 0
			for imageNum in range(nImages):
				image_string = str(st.session_state.image_list[imageNum].attrs['src'])
				image_score = online_funcs.match_title_score(st.session_state.first_title, image_string)

				if image_score > image_score_record and "http" in image_string:
					# print(image_string)
					# print(image_score)
					image_score_record = image_score
					st.session_state.displayed_image_number = imageNum

			if st.session_state.displayed_image_number != -1:
				# st.write(st.session_state.image_list[st.session_state.displayed_image_number].attrs['src'])
				# st.write(image_score_record)
				st.image(st.session_state.image_list[st.session_state.displayed_image_number].attrs['src'], use_column_width=True)
			if st.session_state.displayed_image_number == -1:
				st.image(path+"/no_image.PNG", use_column_width=True)


	if(clean_command):
		st.download_button('Download Recipe!', download_string, 'text_test.txt')

main()