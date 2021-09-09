# Import the modules
import sys
import random
import requests
import string
from bs4 import BeautifulSoup
import csv
from numpy import genfromtxt
from recipe_scrapers import scrape_me
import re
import io
import textwrap
import matplotlib.pyplot as plt

from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import online_funcs
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
		            section_list.append(sib.text)
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
	return section_list






def get_section_list_test(web_address):
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








# def get_section_list(web_address):
# 	# ========================== Accessing the webpage =============================
# 	# ==============================================================================
# 	heading_list = []
# 	section_list = []

# 	page = requests.get(web_address)

# 	# Create a BeautifulSoup object
# 	soup = BeautifulSoup(''.join(page.text), 'lxml')

# 	html = soup.prettify()

# 	for i in re.split('<h1|<h2|<h3|<h4|< h1|< h2|< h3|< h4',html):
# 		temp_section = ''
# 		temp_soup = BeautifulSoup('<h1'+''.join(i), 'lxml')
# 		# print(temp_soup.get_text().split())
# 		# print("   ")

# 		for word in temp_soup.get_text().split():
# 			temp_section = temp_section + ' ' + word



# 		section_list.append(temp_section)

# 	return section_list



def get_heading_list(web_address):
	# ========================== Accessing the webpage =============================
	# ==============================================================================
	heading_list = []
	section_list = []

	page = requests.get(web_address)

	# Create a BeautifulSoup object
	soup = BeautifulSoup(page.text, 'html.parser')

	# ======= Generating the section lists for each section of the webpage =========
	# ==============================================================================
	target = soup.find_all(["h1", "h2", "h3", "h4"])

	for i in range(len(target)):
	    for sib in target[i].find_next_siblings():
	        if sib.name=="h1" or sib.name=="h2" or sib.name=="h3" or sib.name=="h4" :
	            break
	        else:
	            heading_list.append(target[i].text.strip())
	            section_list.append(sib.text)

	return heading_list


def get_ingredients(web_address):
	# ======= Getting the ingredients list using the recipe_scraper library ========
	# ==============================================================================
	ingredients_list = []
	individual_ingredients_list = []
	condensed_ingredients_list = []
	final_ingredients_list = []

	scraper = scrape_me(web_address)
	ingredients_list = scraper.ingredients()

	# Editting the ingredients list to have no punctuation and use stemming
	# - splitting the ingredients into a list of strings
	for ingredient in ingredients_list:
	    temp_list = ingredient.split()
	    for temp_word in temp_list:
	        individual_ingredients_list.append(temp_word)
	# - Removing all punctuation from the strings
	for word in individual_ingredients_list:
	    condensed_ingredients_list.append(word.translate(str.maketrans('', '', string.punctuation)))
	# - Stemming the strings to simpler terms
	ps = PorterStemmer()
	for word2 in condensed_ingredients_list:
	    final_ingredients_list.append(ps.stem(word2))

	return final_ingredients_list



def get_instructions(web_address):
	# ======= Getting the instructions list using the recipe_scraper library ========
	# ==============================================================================
	instructions_list = []
	individual_instructions_list = []
	condensed_instructions_list = []
	final_instructions_list = []

	scraper = scrape_me(web_address)
	instructions_list = scraper.instructions()

	individual_instructions_list = instructions_list.split()

	for word in individual_instructions_list:
	    condensed_instructions_list.append(word.translate(str.maketrans('', '', string.punctuation)))
	# - Stemming the strings to simpler terms
	ps = PorterStemmer()
	for word2 in condensed_instructions_list:
	    final_instructions_list.append(ps.stem(word2))

	return final_instructions_list







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





def log_vocab(web_address):
	initial_vocab_list = []
	initial_vocab_frequency = []
	page_text = []

	# =======================================================================
	# ==========  Deconstructing webpage and logging vocabulary =============
	# =======================================================================

	# ============= Pulling and processing text from webpage ================
	# =======================================================================
	section_list = get_section_list(web_address)
	heading_list = get_heading_list(web_address)

	for section in section_list:
		processed_section = process_section(section)
		page_text.extend(processed_section)

	final_page_text = [word for word in page_text if not word in stopwords.words('english')]

	# ==================== Pulling the vocabulary log =======================
	# =======================================================================
	with open('../data/vocab_list.csv', 'r', encoding='utf-8-sig') as VocabFile:    
		csvReader = csv.reader(VocabFile)    
		for row in csvReader:        
			initial_vocab_list.append(row[0])
			initial_vocab_frequency.append(int(row[1]))        


	# ========= Appending webpage string list to vocabulary log =============
	# =======================================================================
	vocab_list_count = 0
	page_text_count = 0
	append_to_list = 1

	for i in final_page_text:
		vocab_list_count = 0
		append_to_list = 1

		for j in initial_vocab_list:

			if i == j:
				initial_vocab_frequency[vocab_list_count] += 1
				append_to_list = 0
				break
			vocab_list_count += 1

		if append_to_list == 1:
			initial_vocab_list.append(i)
			initial_vocab_frequency.append(1)  

		page_text_count += 1


	# ======= Writing the new vocabulary log back to the .csv file ==========
	# =======================================================================
	new_vocab_list = list(zip(initial_vocab_list, initial_vocab_frequency))

	with open('../data/vocab_list.csv', 'w', encoding='UTF8', newline='') as NewVocabFile:
		writer = csv.writer(NewVocabFile)
		writer.writerows(new_vocab_list)



def generate_training_example_ingredients(web_address):

	# ========================== Accessing the webpage =============================
	# ==============================================================================
	# section_list, section_list_prettify = get_section_list_test(web_address)
	page = requests.get(web_address)
	soup = BeautifulSoup(page.text, 'html.parser')
	section_list, section_list_prettify = online_funcs.TEMP_get_section_list(soup)

	heading_list = get_heading_list(web_address)

	# ======= Getting the ingredients list using the recipe_scraper library ========
	# ==============================================================================
	final_ingredients_list = get_ingredients(web_address)

	# =========================================================================
	# Looping through each section, extracting the individual words and scoring 
	# them based on their similarity to the recipe_scrapers ingredients list.
	# =========================================================================
	section_count = 0
	sim_score_record_count = 0
	sim_score_record = 0.
	section_matrix = []
	comb_sim_score = []
	section_sub = []

	section_matrix, section_disp_matrix = online_funcs.TEMP_get_section_list(soup)

	for final_section_text in section_matrix:
	    # = Editting the section to have no punctuation, use stemming be form a list =
	    # ============================================================================


		# final_section_text = process_section(section)
		# section_matrix.append(final_section_text)

		# print("DEBUG TEST HELOOOOOOO-----------------------------------------------")
		# print(final_section_text)

	    # Determining the "ingredient similarity score" using two methods, and taking
	    # their product for the final score.
		sim_score1 = match_score(final_section_text, final_ingredients_list, 1)
		sim_score2 = match_score(final_section_text, final_ingredients_list, 2)
	    # print("score1:  "+str(sim_score1)+"    "+str(sim_score1*sim_score2))
	    # print("score2:  "+str(sim_score2))

		comb_sim_score.append(sim_score1*sim_score2)
		if sim_score1*sim_score2 > sim_score_record:
			sim_score_record = sim_score1*sim_score2
			sim_score_record_count = section_count
		section_count += 1

	f = open("../data/wordcloud_text.txt","a+")
    
    

	with open('../data/training_data_ingredients_file.csv', 'a', newline='') as training_data_file:
		csvwriter = csv.writer(training_data_file)
		section_count = 0
		for section in section_matrix:
			if(len(section) >= 5) and len(listToString(section)) < 5000:
				# remove stop words for training data (NOTE this is a slow process...)



				section_temp = [word for word in section if not word in stopwords.words('english')]


				section_sub.insert(0,listToString(section_temp))


				if section_count == sim_score_record_count:
					section_sub.insert(0,web_address)
					section_sub.insert(0,comb_sim_score[section_count])
					section_sub.insert(0,1)
					csvwriter.writerow(section_sub)
					f.write(" ".join(section_disp_matrix[section_count])+" ")
				else:
					section_sub.insert(0,web_address)
					section_sub.insert(0,comb_sim_score[section_count])
					section_sub.insert(0,0)
					csvwriter.writerow(section_sub)
			section_count += 1
			section_sub = []

	f.close()

	print("")
	print("")
	print("")
	print("")
	print("==================="+str(sim_score_record)+"=======================")
	print(final_ingredients_list)
	print("")
	print(section_matrix[sim_score_record_count])
	print("====================================================")








def generate_training_example_instructions(web_address):

	# ========================== Accessing the webpage =============================
	# ==============================================================================
	# section_list, section_list_prettify = get_section_list_test(web_address)
	page = requests.get(web_address)
	soup = BeautifulSoup(page.text, 'html.parser')
	section_list, section_list_prettify = online_funcs.TEMP_get_section_list(soup)

	heading_list = get_heading_list(web_address)

	# ======= Getting the ingredients list using the recipe_scraper library ========
	# ==============================================================================
	final_instructions_list = get_instructions(web_address)
	final_instructions_list = [word for word in final_instructions_list if not word in stopwords.words('english')]


	# =========================================================================
	# Looping through each section, extracting the individual words and scoring 
	# them based on their similarity to the recipe_scrapers ingredients list.
	# =========================================================================
	section_count = 0
	sim_score_record_count = 0
	sim_score_record = 0.
	section_matrix = []
	comb_sim_score = []
	section_sub = []

	section_matrix, section_disp_matrix = online_funcs.TEMP_get_section_list(soup)

	for final_section_text in section_matrix:
	    # = Editting the section to have no punctuation, use stemming be form a list =
	    # ============================================================================
	    # final_section_text = process_section(section)
	    # section_matrix.append(final_section_text)

	    # Determining the "ingredient similarity score" using two methods, and taking
	    # their product for the final score.
	    sim_score1 = match_score(final_section_text, final_instructions_list, 1)
	    sim_score2 = match_score(final_section_text, final_instructions_list, 2)
	    # print("score1:  "+str(sim_score1)+"    "+str(sim_score1*sim_score2))
	    # print("score2:  "+str(sim_score2))

	    comb_sim_score.append(sim_score1*sim_score2)
	    if sim_score1*sim_score2 > sim_score_record:
	        sim_score_record = sim_score1*sim_score2
	        sim_score_record_count = section_count
	    section_count += 1

	with open('../data/training_data_instructions_file.csv', 'a', newline='') as training_data_file:
		csvwriter = csv.writer(training_data_file)
		section_count = 0
		for section in section_matrix:
			if len(section) >= 5 and len(listToString(section)) < 5000:
				# print("TTTTTTTTTTTTTTTTTTTTTTTTT")
				# print(len(section))
				# remove stop words for training data (NOTE this is a slow process...)
				# section_temp = [word for word in section if not word in stopwords.words('english')]

				section_sub.insert(0,listToString(section))

				if section_count == sim_score_record_count:
					section_sub.insert(0,web_address)
					section_sub.insert(0,comb_sim_score[section_count])
					# section_sub.insert(0,len(listToString(section)))
					section_sub.insert(0,1)
					csvwriter.writerow(section_sub)
				else:
					section_sub.insert(0,web_address)
					section_sub.insert(0,comb_sim_score[section_count])
					# section_sub.insert(0,len(listToString(section)))
					section_sub.insert(0,0)
					csvwriter.writerow(section_sub)
			section_count += 1
			section_sub = []


	print("")
	print("")
	print("")
	print("")
	print("==================="+str(sim_score_record)+"=======================")
	print(final_instructions_list)
	print("")
	print(section_matrix[sim_score_record_count])
	print("====================================================")






def word_cloud_list_gen():

	f = open("../data/wordcloud_text.txt","r")

	contents =f.read()

	return contents





def plot_cloud(wordcloud):
	plt.figure(figsize=(40,30))
	plt.imshow(wordcloud)
	plt.axis("off");