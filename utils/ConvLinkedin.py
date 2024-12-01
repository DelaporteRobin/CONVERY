import config
import subprocess
import sys
import os
import ctypes
import copy
import time 
import re
import dns.resolver
import webbrowser
import pendulum
import pyperclip 
import pyfiglet
import unidecode
import re
import Levenshtein
import threading
import json
import colorama

from functools import partial
from typing import  Iterable
from datetime import datetime 
from pyfiglet import Figlet 
from time import sleep
from termcolor import *


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



from textual.suggester import SuggestFromList, Suggester
from textual.app import App, ComposeResult
from textual.widgets import Markdown, MarkdownViewer, DataTable,TextArea, RadioSet, RadioButton, Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.validation import Function, Number
from textual.screen import Screen, ModalScreen
from textual import events
from textual.containers import ScrollableContainer, Grid, Horizontal, Vertical, Container, VerticalScroll
from textual import on, work
from textual_datepicker import DateSelect, DatePicker




from utils.ConvUser import ConveryUserUtility
from utils.ConvUtility import ConveryUtility 
from utils.ConvNotif import ConveryNotification





class ConveryLinkedinUtility(ConveryNotification, ConveryUtility):



	def linkedin_login_function(self, link = None):

		driver = webdriver.Chrome()

		chrome_options = Options()
		#chrome_options.add_argument("--headless=new")

		username = self.app.user_settings["UserLinkedinAddress"]
		password = self.app.user_settings["UserLinkedinPassword"]

		
		try:
			driver.get(link)



			#TRY TO LOAD COOKIES FOR LINKEDIN??
			try:
				with open("C:/Program Files/@RCHIVE/DATA/USER/linkedin_cookies.json", "r") as read_file:
					cookies = json.load(read_file)

					for cookie in cookies:
						driver.add_cookie(cookie)

					driver.refresh()
			except Exception as e:
				self.display_error_function("Impossible to load cookies\n%s"%e)
				

				#TRY ORDINARY CONNECTION 
				username_field = driver.find_element(By.ID, "username")
				password_field = driver.find_element(By.ID, "password")

				username_field.send_keys(username)
				password_field.send_keys(password)
				password_field.send_keys(Keys.RETURN)

			else:
				self.display_message_function("Cookies loaded on linkedin session")
				#self.display_message_function("Session refreshed ...")


		except Exception as e:
			self.display_error_function("Impossible to login to linkedin page\n%s"%e)
			return False
		else:
			self.display_success_function("Logged in!")
			return driver






















	def linkedin_get_studiolist_function(self, studio_name):
		driver = self.linkedin_login_function("https://linkedin.com/login")

		if driver == False:
			self.display_error_function("Impossible to make connection")
			return 

		else:
			#self.display_message_function("Connected...")
			self.display_success_function("Driver created")
			#driver.fullscreen_window()

		
			input_container = driver.find_element(By.ID, "global-nav-search")
			input_field = driver.find_element(By.CLASS_NAME, "search-global-typeahead__input")


			#search
			try:
				input_container.click()
				input_field.send_keys(str(studio_name))
				input_field.send_keys(Keys.ENTER)
			except Exception as e:
				self.display_error_function("Impossible to search studio")
				#print(colored("Impossible to search\n%s"%e, "red"))
			else:
				self.display_success_function("Studio typed in searchbar")
				#print(colored("Studio searched", "green"))



			#apply full screen to display button
			driver.fullscreen_window()
			#wait for answer
			sleep(2)

			#result_button = driver.find_elements(By.CLASS_NAME, "search-navigation-panel__button")
			#result_button = driver.find_elements(By.CLASS_NAME, "artdeco-pill")
			#result_button = driver.find_elements(By.CLASS_NAME, "search-reusables__filter-pill-button")
			result_button = WebDriverWait(driver, 10).until(
			    EC.presence_of_all_elements_located((By.CLASS_NAME, "search-reusables__filter-pill-button"))
			)

			#print(result_button)
			for element in result_button:
				if element.text == "Entreprises":
					print(colored("Found company page", "cyan"))
					element.click()
					#sleep(2)
					break

			#print("LIST COMPANY BUTTON")

			#wait for page to load
			sleep(2)
			linkedin_studio_list = {}
			#list_company_button = driver.find_elements(By.CLASS_NAME,"app-aware-link")
			#list_company_link = driver.find_elements(By.XPATH, '//a[@data-test-app-aware-link]')

			#AKA l'expression du démon
			ul_element = WebDriverWait(driver, 5).until(
			    EC.visibility_of_element_located((By.XPATH, '//ul[parent::div[contains(@class, "pv0") and contains(@class, "ph0") and contains(@class, "mb2") and contains(@class, "artdeco-card")]]'))
			)
			#ul_element = driver.find_element(By.XPATH, '//ul[parent::div[contains(@class, "pv0") and contains(@class, "ph0") and contains(@class, "mb2") and contains(@class, "artdeco-card")]]')
			#get all list items contained in list link
			li_list = ul_element.find_elements(By.TAG_NAME, "li")
			for li in li_list:
				#get all links contained in the list
				a_elements = li.find_elements(By.TAG_NAME, "a")

				if a_elements:
					#check if link contain letters, and has a span as parent
					for a in a_elements:
						a_parent = a.find_element(By.XPATH, "..")

						if (self.letter_verification_function(a.text)==True) and (a_parent.tag_name == "span"):
							#print("%s : %s"%(a.text, a.get_attribute("href")))
							#add the link to the link dictionnary
							linkedin_studio_list[a.text] = a.get_attribute("href")


	
			#os.system("pause")
			return linkedin_studio_list
			

			









	def get_linkedin_user_function(self, studio_name, studio_account):
		driver = self.linkedin_login_function(studio_account)
		if driver == False:
			self.display_error_function("Impossible to make connection")
			return 
		else:
			self.display_success_function("Driver created")


			driver.maximize_window()
			sleep(2)


			self.display_message_function("TRYING TO SEARCH FOR CONTACTS!")

			

			#try to click on the "Personnes" button
			member_button = driver.find_elements(By.CLASS_NAME, "org-page-navigation__item-anchor")[-1]
			member_button.click()

			#member_profile_container_list = driver.find_elements(By.CLASS_NAME, "org-people-profile-card__profile_info")
			sleep(2)
			

			#scroll to the bottom
			last_height = driver.execute_script("return document.body.scrollHeight")

			while True:
			    # Faire défiler jusqu'en bas
			    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			    
			    # Attendre que la page charge le contenu dynamique (si applicable)
			    time.sleep(0.5)
			    
			    # Obtenir la nouvelle hauteur de la page
			    new_height = driver.execute_script("return document.body.scrollHeight")
			    
			    # Si la hauteur n'a pas changé, arrêter
			    if new_height == last_height:
			        print("Fin de la page atteinte.")
			        break
			    
			    # Mettre à jour la hauteur pour la prochaine itération
			    last_height = new_height
			#driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
			
			#member_name_div_list = driver.find_elements(By.CLASS_NAME,"org-people-profile-card__profile-title")
			member_name_container_list = driver.find_elements(By.CLASS_NAME, "artdeco-entity-lockup__title")
			#build name list from container 
			member_name_list = []
			for member_container in member_name_container_list:
				try:
					#check parent
					parent = member_container.find_element(By.XPATH, "..")
					child = member_container.find_element(By.XPATH, "./*")
					if (parent.tag_name == "div") and ("artdeco-entity-lockup__content" in parent.get_attribute("class").split()):
						if child.tag_name == "a":	
							self.display_message_function("Contact found --> %s"%member_container.text)
							member_name_list.append(member_container)
				except Exception as e:
					self.display_error_function("Error while searching for contact")
					#self.display_error_function(e)
					continue


			member_position_div_list = driver.find_elements(By.CLASS_NAME, "artdeco-entity-lockup__subtitle")
			member_position_image_list = driver.find_elements(By.CLASS_NAME, "artdeco-entity-lockup__image--type-circle")
			#member_link_container = driver.find_element(By.CLASS_NAME, "link-without-visited-state")
			



			
			member_list = {}
			for i in range(len(member_name_list)):

				#find the link contained 
				link = member_position_image_list[i].find_element(By.TAG_NAME, "a").get_attribute("href")
				#print("%s : %s [%s]"%(member_name_div_list[i].text, member_position_div_list[i].text, link))

				member_list[member_name_list[i].text] = {
					"link":link,
					"position":member_position_div_list[i].text
				}

			self.display_success_function("TASK DONE")
			sleep(2)
			return member_list
			




		
		return None
