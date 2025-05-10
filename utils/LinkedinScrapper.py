"""
Python script to scrap linkedin content
open linkedin and log in with cookies or user credentials

get a keyword list to search in each post
for each post
	check if keywords are in the content

	true:
		try to get important datas on the post (date / link...)
		check if date if mathing with timestamp :)
		save the post
"""

import os
import colorama
import csv
import requests
import traceback
import json
import pyperclip
import pyfiglet
import rich

import argparse
import re

from rich.console import Console
from rich.theme import Theme
from rich.traceback import install

from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
from termcolor import *
from time import sleep

from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


colorama.init()




class LinkedinScrapperApplication:
	def __init__(self):
		

		#create the theme for rich
		self.rich_theme = Theme(
			{
				"general":"dark_violet",
				"info":"yellow",
				"warning":"orange3",
				"error":"red3",
				"success":"chartreuse1",
			}
		)
		#create the rich console
		self.console = Console(theme=self.rich_theme)
		#install(show_locals=True)



		#GATHER INFORMATIONS FOR PROGRAM
		self.MAXIMUM_ITERATION = 500
		self.DATECHECKING = False
		self.DATELIMIT = 30
		self.COOKIES = None
		self.COOKIESPATH = os.path.join(os.getcwd(), "data/user/linkedin_cookies.json")
		self.LINK = "https://linkedin.com/login"
		self.KEYWORDLIST = ["hire","hiring", "lighting", "shading", "lookdev", "lighter", "recrute", "recruting", "houdini", "modeling"]
		self.POST_DICTIONNARY = {}
		#try to load the previous dictionnary
		self.complete_keyword_list_function()
		self.load_scrapping_dictionnary_function()



		self.display_title_function()
		

		try:
			self.console.log("Trying to create webdriver", style="info")
			#INIT THE WEBDRIVER
			#DEFINE CHROME OPTIONS
			chrome_options = Options()
			#chrome_options.add_argument("--headless")  # Activer le mode sans tête
			chrome_options.add_argument("--disable-gpu")  # Désactiver le GPU (utile pour Windows)
			chrome_options.add_argument("--no-sandbox")  # Option pour environnements Linux
			chrome_options.add_argument("--disable-dev-shm-usage")  # Résoudre les problèmes mémoire sous Docker/Linux
			chrome_options.add_argument("--window-size=1920,1080")  # Résolution standard pour éviter certains bugs UI
			chrome_options.add_argument("--enable-unsafe-swiftshader")

			self.driver = webdriver.Chrome(options = chrome_options)
			self.driver.get(self.LINK)

			self.wait_long = WebDriverWait(self.driver, 10)
		except Exception as e:
			self.console.log("Impossible to create webdriver", "error")
			self.console.log(traceback.format_exc(), "error")
		else:
			self.console.log("Trying to get user cookies in %s"%self.COOKIESPATH, style="info")



			if self.load_user_cookies_function()==False:
				exit()
			else:
				self.read_linkedin_loop_function()





	def display_title_function(self):
		self.console.log(pyfiglet.figlet_format("CONVERY\nLinkedin Scrapper", font="the_edge"), style="general")

	def load_user_cookies_function(self):
		try:
			#get cookies
			with open(self.COOKIESPATH, "r") as read_file:
				cookies=json.load(read_file)

				for cookie in cookies:
					#print("loading cookie")
					self.driver.add_cookie(cookie)

				self.driver.refresh()
		except Exception as e:
			self.console.log("Impossible to load cookies", style="error")
			self.console.log(traceback.format_exc(), style="error")
			return False
		else:
			self.console.log("User cookies loaded", style="success")
			return True

	def get_post_id(self,url):
		regex = r"activity-([0-9]+)"
		match = re.search(regex, url)
		if match:
			return match.group(1)
		return None


	def extract_unix_timestamp(self,post_id):
		as_binary = format(int(post_id), "064b")
		first42_chars = as_binary[:42]
		timestamp = int(first42_chars, 2)
		return timestamp


	def unix_timestamp_to_human_date(self,timestamp):
		date_object = datetime.utcfromtimestamp(timestamp / 1000)
		human_date_format = date_object.strftime("%a, %d %b %Y %H:%M:%S (UTC)")
		return human_date_format


	def get_date(self,url):
		post_id = self.get_post_id(url)
		if post_id:
			unix_timestamp = self.extract_unix_timestamp(post_id)
			human_date_format = self.unix_timestamp_to_human_date(unix_timestamp)
			return human_date_format
		return None

	def complete_keyword_list_function(self):
		self.console.log("Updating keyword list...", style="general")
		list_keywordlist = self.KEYWORDLIST.copy()
		list_final_keywordlist = []

		for keyword in list_keywordlist:

			if keyword not in list_final_keywordlist:
				list_final_keywordlist.append(keyword)
			#capitalize
			if keyword.capitalize() not in list_final_keywordlist:
				list_final_keywordlist.append(keyword.capitalize())
			#UPPER
			if keyword.upper() not in list_final_keywordlist:
				list_final_keywordlist.append(keyword.upper())
			#lower
			if keyword.lower() not in list_final_keywordlist:
				list_final_keywordlist.aappend(keyword.lower())

		self.KEYWORDLIST = list_final_keywordlist
		self.console.log("Updated...", style="success")
		self.console.log(self.KEYWORDLIST)



	def convert_date_function(self,date):
		return datetime.strptime(str(date).replace(" (UTC)", ""), "%a, %d %b %Y %H:%M:%S")


	def save_post_dictionnary_function(self):
		try:
			with open(os.path.join(os.getcwd(), "data/LinkedinScrapping.json"), "w") as save_file:
				json.dump(self.POST_DICTIONNARY, save_file, indent=4)
		except Exception as e:
			self.console.log("Impossible to save dictionnary", style="error")
			self.console.log(traceback.format_exc(), style="error")
		else:
			self.console.log("Dictionnary updated", style="success")


	def load_scrapping_dictionnary_function(self):
		try:
			with open(os.path.join(os.getcwd(), "data/LinkedinScrapping.json"), "r") as read_file:
				self.POST_DICTIONNARY = json.load(read_file)
		except Exception as e:
			self.console.log("Impossible to load dictionnary", style="error")
			self.console.log("Dictionnary reinitialized", style="error")
		else:
			self.console.log("Dictionnary loaded successfully", style="success")


	def read_linkedin_loop_function(self):


		#get the current page height
		last_height = self.driver.execute_script("return document.body.scrollHeight")
		i = 0
		while True:
			self.console.log("Current iteration count : %s"%i)
			if i == self.MAXIMUM_ITERATION:
				i=0
				self.driver.refresh()
				sleep(5)
				print("\n\n")
				self.console.log("REFRESH PAGE", style="warning")
				print("\n\n")
			#scroll to the bottom of the page
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			sleep(2)  # attendre le chargement des nouveaux éléments

			#WAIT FOR THE CONTENT OF THE PAGE
			self.wait_long.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.feed-shared-update-v2")))
			#get the content of the page
			list_post = self.driver.find_elements(By.CSS_SELECTOR, "div.feed-shared-update-v2")
			list_button = self.driver.find_elements(By.CSS_SELECTOR, 'button.feed-shared-control-menu__trigger.artdeco-button.artdeco-button--tertiary.artdeco-button--muted.artdeco-button--1.artdeco-button--circle.artdeco-dropdown__trigger.artdeco-dropdown__trigger--placement-bottom.ember-view')


			#GO THROUGH EACH POST IN THE PAGE
			for i in range(len(list_post)):
				print("\n\n")
				post = list_post[i]

				post_title = post.find_elements(By.CSS_SELECTOR, "span[aria-hidden='true']")[0]
				post_text = post.find_elements(By.CSS_SELECTOR, "span[dir='ltr']")
				#check if the post contain shared content
				#fEumavdWlUhgOAFgnottJ	yRnrnDZKCtEkmr feed-shared-update-v2__update-content-wrapper artdeco-card
				post_shared = post.find_elements(By.CSS_SELECTOR, "div.feed-shared-update-v2__update-content-wrapper")
				post_shared_text = None
		
				if len(post_shared) != 0:
					self.console.log("SHARED POST DETECTED", style="warning")
					post_shared = post_shared[0]
					#try to find the text contained inside of the post_shared variable
					post_shared_text = post_shared.find_elements(By.CSS_SELECTOR, "span[dir='ltr']")
					for i in range(len(post_shared_text)):
						post_shared_text[i] = post_shared_text[i].text

					post_text_shared_combined = "\n".join(post_shared_text)

				#DISPLAY POST TEXT
				self.console.log("Global post content", style="warning")
				for i in range(len(post_text)):
					print("\n\n")
					element_list = post_text[i].text.splitlines()
					post_text_id = post_text[i].get_attribute("class")
					if (len(element_list)==2) and (element_list[0] == element_list[1]):
						element_list.pop(1)

					element_joined = "\n".join(element_list)
					post_text[i] = element_joined
					self.console.log("%s : %s"%(post_text[i], post_text_id))

				post_text_combined = "\n".join(post_text)

				#CHECK IF KEYWORDS ARE IN THE POST TEXT COMBINED
				found=False
				counter = 0
				counter_list = []
				for keyword in self.KEYWORDLIST:
					if keyword in post_text_combined:
						found=True
						counter+=1
						counter_list.append(keyword)

				if found==False:
					self.console.log("No keyword in the current post", style="error")
					self.console.log("Post skipped", style="error")
					
				else:
					self.console.log("KEYWORD FOUND IN POST", style="success")
					self.console.log("Keyword found counter : %s/%s"%(counter, len(self.KEYWORDLIST)))
					self.console.log("Keyword found : %s"%counter_list)
					#if the post was shared
					#try to clean the content by removing the shared content from the original post text
					"""
					if post_shared_text != None:
						self.console.log("Trying to clean the post text", style="warning")
						post_cleaned_text = post_text_combined.replace(post_text_shared_combined, "").strip()
						print(post_cleaned_text)
					"""

					#TRY TO GET THE POST LINK
					try:
						self.console.log("Trying to get the post link", style="info")
						post_button = WebDriverWait(post, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.feed-shared-control-menu__trigger')))
						ActionChains(self.driver).move_to_element(post_button).perform()
						WebDriverWait(self.driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.feed-shared-control-menu__trigger')))
						post_button.click()

						post_div = post.find_element(By.CSS_SELECTOR, 'div.feed-shared-control-menu__content')
						menu_option = WebDriverWait(self.driver, 8).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'feed-shared-control-menu__content')]//div[@role='button']")))
						
						menu_option[1].click()
						post_link = pyperclip.paste()
					except Exception as e:
						self.console.log("Impossible to get post link", style="error")
						self.console.log(traceback.format_exc(), style="error")
					else:
						self.console.log("Post link retrieved", style="success")
						self.console.log(post_link, style="success")


						#GET POST DATE
						post_date = self.get_date(post_link)
						if self.DATECHECKING==True:
							if post_date != None:
								self.console.log("Date detected : %s"%post_date, style="success")

								#CONVERT THE DATE
								post_date_converted = self.convert_date_function(post_date)
								self.console.log("Date converted : %s"%post_date_converted)

								#CHECK IF DATE IS BEFORE TIMESTAMP VALUE
								#from the current date!
								#get the current date
								current_date = datetime.now()
								delta = current_date - post_date_converted 
								self.console.log("DATE DELTA : %s"%delta, style="warning")
								if (delta <= timedelta(days=self.DATELIMIT)):

									#UPDATE THE DICTIONNARY
									if str(post_date_converted) not in list(self.POST_DICTIONNARY.keys()):
										self.POST_DICTIONNARY[str(post_date_converted)] = {
											"POSTACCOUNT": post_title.text,
											"POSTCONTENT":post_text,
											"POSTLINK":post_link,
											"POSTDATE":str(post_date_converted),
											"POSTKEYWORDS":counter_list
										}
										self.save_post_dictionnary_function()
								else:
									self.console.log("TIME LIMIT REACHED", style="danger")
									self.console.log("Saving skipped", style="danger")

							else:
								self.console.log("Impossible to get date", style="error")
						else:
							self.POST_DICTIONNARY[str(datetime.now())] = {
								"POSTACCOUNT": post_title.text,
								"POSTCONTENT":post_text,
								"POSTLINK":post_link,
								"POSTDATE":str(datetime.now()),
								"POSTKEYWORDS":counter_list
							}
							self.save_post_dictionnary_function()

								
			

			#refresh the page height
			new_height = self.driver.execute_script("return document.body.scrollHeight")
			last_height = new_height


			i+=1

			#sleep(1)





if __name__ == "__main__":
	LinkedinScrapperApplication()