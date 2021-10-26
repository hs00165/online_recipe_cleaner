# Online Recipe Cleaner
### Harrison Sims

This web-app is designed to take the web address for a recipe website as input, and return just the ingredients and instructions in an easy-to-read format. The recipe can then be downloaded for future reference.

This works by scraping the website using BeautifulSoup, and splitting it into sections. Each section is then parsed to a naive bayes (NB) model which evaluates the probability of that section either being either the ingredients or instructions. The NB model was trained using sklearn.


