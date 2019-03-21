from selenium import webdriver
from selenium.webdriver.support.select import Select  # <option> element

import time
import configparser
import re

from english_numbers import is_english_number, get_denary_number


def login(driver):
	config = configparser.ConfigParser()
	config.read('logins.ini')
	hegarty = config['hegartymaths.com']

	driver.get("https://hegartymaths.com/login/learner")

	school_name_el = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/input")
	school_name_el.send_keys(hegarty['school_name'])
	time.sleep(1)
	driver.find_element_by_xpath("/html/body/div[2]/div/div/ul/li[1]").click()

	first_name_el = driver.find_element_by_xpath("/html/body/div[2]/div/div/form/div[1]/div/input[1]")
	first_name_el.send_keys(hegarty['firstname'])

	surname_el = driver.find_element_by_xpath("/html/body/div[2]/div/div/form/div[1]/div/input[2]")
	surname_el.send_keys(hegarty['surname'])

	dob_day_el = Select(driver.find_element_by_id("day"))  # <option> element
	dob_day_el.select_by_visible_text(hegarty['dob_day'])

	dob_month_el = Select(driver.find_element_by_id("month"))
	dob_month_el.select_by_value(hegarty['dob_month'])

	dob_year_el = Select(driver.find_element_by_id("year"))
	dob_year_el.select_by_visible_text(hegarty['dob_year'])

	next_el = driver.find_element_by_xpath("/html/body/div[2]/div/div/form/div[3]/button")
	next_el.click()

	password_el = driver.find_element_by_xpath("/html/body/div[2]/div/div/form/input")
	password_el.send_keys(hegarty['password'])

	login_el = driver.find_element_by_xpath("/html/body/div[2]/div/div/form/button")
	login_el.click()

	time.sleep(5)

	return driver


def solve(question):
	tokens = re.split(',| |\?|\.', question)
	# The filter removes empty strings which could happen if comma precedes a space
	tokens = list(filter(len, tokens))

	number_tokens = []

	for token in tokens:
		if is_english_number(token):
			number_tokens += [token]
		elif token.isdigit():
			number_tokens += [token]

	converted_numbers = []
	for number in number_tokens:
		if is_english_number(number):
			converted_numbers += [get_denary_number(number)]
		else:
			converted_numbers += [int(number)]

	answer = sum(converted_numbers)

	print("="*80)
	print("Original question:  \"" + question + "\"")
	print("Tokens: ", tokens)
	print("Number tokens: ", number_tokens)
	print("Converted numbers: ", converted_numbers)
	print("Final expression: ", " + ".join([str(t) for t in converted_numbers]))
	print("Answer: ", answer)

	return answer


def do_question(driver):
	question_element = driver.find_element_by_xpath("//*[@id=\"content\"]/div[2]/div/div/div[1]/div/div[2]/div/div[2]")
	time.sleep(0.5)
	question_text = question_element.text

	solved_answer = solve(question_text)

	answer_el = driver.find_element_by_xpath("//*[@id=\"content\"]/div[2]/div/div/div[1]/div/div[3]/div/div[3]/div/span/span[1]/textarea")
	answer_el.send_keys(str(solved_answer))

	submit_el = driver.find_element_by_xpath("//*[@id=\"content\"]/div[2]/div/div/div[2]/button[1]")
	submit_el.click()

	time.sleep(0.5)

	next_el = driver.find_element_by_xpath("//*[@id=\"content\"]/div[2]/div/div/div[2]/button")
	next_el.click()
	time.sleep(0.5)

	return driver


def do_quiz(driver):
	print("-"*80)

	driver.get("https://hegartymaths.com/simple-addition-its-meaning")

	do_quiz_button = driver.find_element_by_class_name("Btn__assessment")
	do_quiz_button.click()

	while "summary" not in driver.current_url:
		driver = do_question(driver)

	return driver



DEBUG = True

if __name__ == "__main__":
	if not DEBUG:
		driver = webdriver.Chrome()
		driver.implicitly_wait(30)

		#  Login when logged out after session expired (?)
		while True:
			driver = login(driver)

			while driver.current_url != "https://hegartymaths.com":
				driver = do_quiz(driver)

	else:
		solve("What is 12 more than Three plus twenty?")
		solve("Whats nine plus 10?")
		solve("Two plus two + 9")
		solve("What is the sum of two and three?")
		solve("What is the sum of 2 and 3?")
		solve("Find the sum of 4 and 10.")
