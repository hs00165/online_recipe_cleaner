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




def get_section_list(web_address):
	# ========================== Accessing the webpage =============================
	# ==============================================================================
	heading_list = []
	section_list = []
	section_list_prettify = []

	page = requests.get(web_address)

	# Create a BeautifulSoup object
	soup = BeautifulSoup(page.text, 'html.parser')

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





def format_section(section_prettify):

	flag=0
	total_string = ""
	total_string_final = ""
	final_section_list = []

	section_prettify_list = io.StringIO(section_prettify)
	for line in section_prettify_list:

		if "<" not in line:
			total_string = total_string + line

		if "</li" in line or "</p" in line or "</ul>" in line:
			# total_string.replace("\n", " ")
			# print(len(total_string))

			
			step2 = ' '.join(total_string.split())


			step3 = textwrap.fill(step2, 64)

			final_section_list.append(step3)

			# print("--- "+str(step3))
			total_string = ""


	# final_section = '\n'.join(final_section_list)

	return final_section_list





def process_section(section):
    condensed_section_text = [] # Section after getting rid of punctuation
    final_section_text = [] # Section words after stemming is applied
    # Splitting the webpage text into a list of strings
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
	"1","2","3","4","5","6","7","8","9","0"]
	output_string = ""

	for element in input_string:
		for character in acceptable_characters:
			if element == character:
				output_string = output_string + element

	return output_string



