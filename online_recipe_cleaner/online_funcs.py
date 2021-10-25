# Import the modules
import sys
import random
import requests
import string
from bs4 import BeautifulSoup
import re
import io
import textwrap

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

# test

def listToString(s): 
    
    # initialize an empty string
    str1 = " " 
    
    # return string  
    return (str1.join(s))


def pull_webpage(web_address):
	page = requests.get(web_address)

	soup = BeautifulSoup(page.text, 'html.parser')

	image_list = soup.findAll('img',{"src":True})

	return soup, image_list




def match_score(section_list, final_ingredients_list, toggle_score_method):

	score = 0

	if toggle_score_method == 1:
		if len(final_ingredients_list) != 0:

			for word3 in final_ingredients_list:
				if word3 in section_list:
					score += 1
			score = score*100/(1.*len(final_ingredients_list))

	if toggle_score_method == 2:
		if len(section_list) != 0:

			for word3 in section_list:
				if word3 in final_ingredients_list:
					score += 1
			score = score*100/(1.*len(section_list))

	return score




def TEMP_get_section_list(soup):

	prettify_temp_string = ""
	text_string = ""
	display_string = []
	non_repeating_display_string = []
	final_section_list_display = []
	final_section_list_model = []
	prev_line = ""
	step1 = ""

	list_flag = 0
	li_flag = 0
	p_flag = 0
	temp_flag = 0


	prettified_webpage = soup.prettify()

	webpage_file = io.StringIO(prettified_webpage)

	for line in webpage_file:

		flag = 0


		
		
		if flag == 0:
			prettify_temp_string = prettify_temp_string + line


		if "</h1" in line or "</h2" in line or "</h3" in line or "</h4" in line:

			seen = set()
			result = []
			for item in display_string:
			    if item not in seen:
			        seen.add(item)
			        non_repeating_display_string.append(item)


			final_section_list_display.append(non_repeating_display_string)
			final_section_list_model.append(TEMP_process_section_for_model(text_string))
			# print("")
			# print("")
			# print("")
			# print("")
			# print("")
			# print("")
			# print("/////////////////////////////////////////////////////////////")
			# print("******")
			# print(TEMP_process_section_for_model(text_string))
			# print("******")
			# print(prettify_temp_string)
			prettify_temp_string = ""
			text_string = ""
			step1 = ""
			display_string = []
			non_repeating_display_string = []
			flag = 1


		# need seperate flags for each tag:
		if "<li" in line:
			li_flag = 1
			user_flag = "<li>  "
		if "</li" in line:
			li_flag = 0

		if "<p" in line:
			p_flag = 1
			user_flag = "<p>  "
		if "</p" in line:
			p_flag = 0




		if "<" not in line and ">" not in line and "{" not in line and "}" not in line and flag == 0 and (li_flag == 1 or p_flag == 1):
			# Need this to be conditional of being inside a <li> or something similar
			text_string = text_string + " " + line.strip()
			step1 = step1 + line

			temp_flag = 1

		if temp_flag == 1 and li_flag == 0 and p_flag == 0:
			step2 = ' '.join(step1.split())
			display_string.append(textwrap.fill(step2, 64))
			temp_flag = 0
			step1 = ""


		prev_line = line


	seen = set()
	result = []
	for item in display_string:
	    if item not in seen:
	        seen.add(item)
	        non_repeating_display_string.append(item)

	final_section_list_display.append(non_repeating_display_string)
	final_section_list_model.append(TEMP_process_section_for_model(text_string))
	# print("")
	# print("")
	# print("")
	# print("")
	# print("")
	# print("")
	# print("/////////////////////////////////////////////////////////////")
	# print("******")
	# print(TEMP_process_section_for_model(text_string))
	# print("******")
	# print(prettify_temp_string)


	return final_section_list_model, final_section_list_display



	

def get_section_list(soup):
	# ========================== Accessing the webpage =============================
	# ==============================================================================
	heading_list = []
	section_list = []
	section_list_prettify = []



	# ======= Generating the section lists for each section of the webpage =========
	# ==============================================================================
	target = soup.find_all(["h1", "h2", "h3", "h4", "legend"])

	for i in range(len(target)):
		exit_flag = 0
		# If the header has siblings,
		# search through siblings
		if len(target[i].find_next_siblings()) >= 1 and exit_flag==0:
		    for sib in target[i].find_next_siblings():
		        if sib.name=="h1" or sib.name=="h2" or sib.name=="h3" or sib.name=="h4" or sib.name=="legend":
		            exit_flag=1
		            break
		        else:
		            heading_list.append(target[i].text.strip())
		            section_list.append(sib.text.strip())
		            section_list_prettify.append(sib.prettify())
		# If the header has no siblings,
		# search through parents!
		if exit_flag==0 and target[i].parent is not None:
			for uncles in target[i].parent.find_next_siblings():
				if uncles.name=="h1" or uncles.name=="h2" or uncles.name=="h3" or uncles.name=="h4" or uncles.name=="legend":
					exit_flag=1
					break
				else:
					heading_list.append(target[i].text.strip())
					section_list.append(uncles.text.strip())
					section_list_prettify.append(uncles.prettify())
		# If the parent isn't the header,
		# search for grand parents!
		if exit_flag==0 and target[i].parent.parent is not None:
			for great_uncles in target[i].parent.parent.find_next_siblings():
				if great_uncles.name=="h1" or great_uncles.name=="h2" or great_uncles.name=="h3" or great_uncles.name=="h4" or great_uncles.name=="legend":
					exit_flag=1
					break
				else:
					heading_list.append(target[i].text.strip())
					section_list.append(great_uncles.text.strip())
					section_list_prettify.append(great_uncles.prettify())
		# If the g parent isn't the header,
		# search for grand parents!
		if exit_flag==0 and target[i].parent.parent.parent is not None:
			for gg_uncles in target[i].parent.parent.parent.find_next_siblings():
				if gg_uncles.name=="h1" or gg_uncles.name=="h2" or gg_uncles.name=="h3" or gg_uncles.name=="h4" or gg_uncles.name=="legend":
					exit_flag=1
					break
				else:
					heading_list.append(target[i].text.strip())
					section_list.append(gg_uncles.text.strip())
					section_list_prettify.append(gg_uncles.prettify())
		# If the gg parent isn't the header,
		# search for grand parents!
		if exit_flag==0 and target[i].parent.parent.parent.parent is not None:
			for ggg_uncles in target[i].parent.parent.parent.parent.find_next_siblings():
				if ggg_uncles.name=="h1" or ggg_uncles.name=="h2" or ggg_uncles.name=="h3" or ggg_uncles.name=="h4" or ggg_uncles.name=="legend":
					exit_flag=1
					break
				else:
					heading_list.append(target[i].text.strip())
					section_list.append(ggg_uncles.text.strip())
					section_list_prettify.append(ggg_uncles.prettify())
		# If the ggg parent isn't the header,
		# search for grand parents!
		if exit_flag==0 and target[i].parent.parent.parent.parent.parent is not None:
			for gggg_uncles in target[i].parent.parent.parent.parent.parent.find_next_siblings():
				if gggg_uncles.name=="h1" or gggg_uncles.name=="h2" or gggg_uncles.name=="h3" or gggg_uncles.name=="h4" or gggg_uncles.name=="legend":
					exit_flag=1
					break
				else:
					heading_list.append(target[i].text.strip())
					section_list.append(gggg_uncles.text.strip())
					section_list_prettify.append(gggg_uncles.prettify())

	return section_list, section_list_prettify


def TEMP_format_section(section_prettify):

	flag=0
	text_string = ""
	final_prettify_section_list = []
	final_text_section_list = []
	prettify_temp_string = ""

	section_prettify_list = io.StringIO(section_prettify)
	for line in section_prettify_list:
		flag = 0
		

		if "</h1" in line or "</h2" in line or "</h3" in line or "</h4" in line:

			final_prettify_section_list.append(prettify_temp_string)
			final_text_section_list.append(text_string)
			# print("")
			# print("/////////////////////////////////////////////////////////////")
			# print(text_string)
			# print(prettify_temp_string)
			prettify_temp_string = ""
			text_string = ""
			flag = 1


		if "<" not in line and flag == 0:
			text_string = text_string + line


		if flag == 0:
			prettify_temp_string = prettify_temp_string + line


	final_prettify_section_list.append(prettify_temp_string)
	final_text_section_list.append(text_string)


	return final_prettify_section_list, final_text_section_list



def TEMP_process_section_for_model(section):
    condensed_section_text = [] # Section after getting rid of punctuation
    final_section_model = [] # Section words after stemming is applied
    step3 = []
    step4_list = []
    total_string = ""

    section_text = section.split()

    section_text = [word for word in section_text if not word in stopwords.words('english')]


    





    for word in section_text:
        condensed_section_text.append(word.translate(str.maketrans('', '', string.punctuation)))
    # Stemming the strings to simpler terms
    ps = PorterStemmer()
    for word1 in condensed_section_text:
    	# the clean_string function takes out any non-alphanumeric characters 
    	word2 = clean_string(ps.stem(word1))
    	final_section_model.append(word2)

    return final_section_model







def format_section(section_prettify):

	flag=0
	total_string = ""
	total_string_final = ""
	step4_list = []
	final_section_list = []

	section_prettify_list = io.StringIO(section_prettify)
	for line in section_prettify_list:

		if "<" not in line:
			total_string = total_string + line

		if "</li" in line or "</p" in line or "</ul" in line:
			# total_string.replace("\n", " ")
			# print(len(total_string))

			
			step2 = ' '.join(total_string.split())


			step3 = textwrap.fill(step2, 64)

			# If the string (step3) has appeared already in the list, 
			# do not write it.

			step4_list.append(step3)

			# print("--- "+str(step3))
			total_string = ""


	# final_section = '\n'.join(final_section_list)

	seen = set()
	result = []
	for item in step4_list:
	    if item not in seen:
	        seen.add(item)
	        final_section_list.append(item)

	return final_section_list

def process_title(title):

	text_list = re.split("[, -!?:]+", title)
	return_list = []

	for text in text_list:
		temp_text = text.lower()
		if temp_text != "":
			return_list.append(clean_string(temp_text))

	return return_list


def match_title_score(initial_title_list, image_address):

	unwanted_word_list = ["recipe", "food", "best", "bbc"]
	title_list = []

	for word in initial_title_list:
		if word not in unwanted_word_list:
			title_list.append(word)

	score = 0.0

	start_index = image_address.find ( ".co" )
	# print("ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
	# print(title_list)
	# print(image_address)
	# print(start_index)

	for text in title_list:
		if text in image_address.lower()[start_index:]:
			score = score + 1.0

	score = score / len(title_list)

	return score




def process_section(section):
    condensed_section_text = [] # Section after getting rid of punctuation
    final_section_text = [] # Section words after stemming is applied
    # Splitting the text into a list of strings
    section_text = section.split()

    # === Editting the page text to have no punctuation and use stemming ====
    # =======================================================================
    # Removing all punctuation from the string
    for word in section_text:
        condensed_section_text.append(word.translate(str.maketrans('', '', string.punctuation)))
    # Stemming the strings to simpler terms
    ps = PorterStemmer()
    for word1 in condensed_section_text:
    	# the clean_string function takes out any non-alphanumeric characters 
    	word2 = clean_string(ps.stem(word1))
    	final_section_text.append(word2)

    return final_section_text


def clean_string(input_string):
	acceptable_characters = ["a","b","c","d","e","f","g","h","i","j",
	"k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
	"1","2","3","4","5","6","7","8","9","0","A","B","C","D","E","F","G",
	"H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W",
	"X","Y","Z"]
	output_string = ""

	for element in input_string:
		for character in acceptable_characters:
			if element == character:
				output_string = output_string + element

	return output_string

def clean_string_no_numbers(input_string):
	acceptable_characters = ["a","b","c","d","e","f","g","h","i","j",
	"k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
	"A","B","C","D","E","F","G",
	"H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W",
	"X","Y","Z"]
	output_string = ""

	for element in input_string:
		for character in acceptable_characters:
			if element == character:
				output_string = output_string + element

	return output_string.lower()



def get_title(soup):

	return_titles = []

	# page = requests.get(web_address)
	# # Create a BeautifulSoup object
	# soup = BeautifulSoup(page.text, 'html.parser')

	title_list = soup.find_all('title')


	for titles in title_list:
		return_titles.append(titles.get_text())

	return return_titles








def generate_section_matrix(soup):

	full_prettify_section_list = []
	full_text_section_list = []

	# ================================================================================

	# PLAN OF ACTION
	# 1) Need to first pull the section list using the "next siblings" function
	# 2) Then need to look at the "prettified" version of the section,
	#    splitting the section further if it encounters any header labels
	# -- NOTE need to save the .get_text() and the .Prettify() of these new
	#    sections.
	# 3) Then format the section, both for the model and for the output


	# # Step 1
	# section_list, section_list_prettify = get_section_list(soup)

	# Step 1
	section_list, section_list_prettify = TEMP_get_section_list(soup)


	# DO NOT see any BS here...
	# for sect in section_list:
	# 	print(sect)


	# for k in range(len(section_list_prettify)):
	# 	print("DEBUGGGGGG")
	# 	print("*******************************************")
	# 	print("*******************************************")
	# 	print("*******************************************")
	# 	print("*******************************************")
	# 	print("*******************************************")
	# 	print("*******************************************")
	# 	print("*******************************************")
	# 	print("")
	# 	print("")
	# 	print("")
	# 	print("")
	# 	print("")
	# 	print(section_list_prettify[k])
	# 	print("---------------------------------")
	# 	print(section_list[k])





	# Need to adjust below here to kame everything work! 
	# Currently this is formatting the "prettified" section,
	# but that is WRONG! the section matrix is already 
	# pretty much formatted, so I don't want to re-format
	# (the wrong way!) the prettified section.
	













	# section_model_matrix = []
	# section_disp_matrix = []

	# # Step 2
	# for primary_section in section_list_prettify:
	# 	formatted_sections_prettify, formatted_sections_text = TEMP_format_section(primary_section)
		
	# 	# Saving both the text version (for the model) and the prettify version (to display
	# 	# to the user).
	# 	full_prettify_section_list = full_prettify_section_list + formatted_sections_prettify
	# 	full_text_section_list = full_text_section_list + formatted_sections_text

	# # Step 3
	# #Formatting the sections for the Model to evaluate
	# TEMP_section_count = 0
	# for temp_section in full_text_section_list:
	# 	processed_section = TEMP_process_section_for_model(temp_section)
	# 	# print("*******************************************")
	# 	# print(processed_section)
	# 	section_model_matrix.append(processed_section)
	# 	TEMP_section_count = TEMP_section_count + 1


	# #Formatting the sections to display to the user
	# for section in full_prettify_section_list:
	# 	processed_section = format_section(section)
	# 	section_disp_matrix.append(processed_section)


	# # for i in range(TEMP_section_count):
	# # 	print("*******************************************")
	# # 	print(section_model_matrix[i])
	# # 	print("")
	# # 	print(section_disp_matrix[i])













	return section_list, section_list_prettify


	# ================================================================================
