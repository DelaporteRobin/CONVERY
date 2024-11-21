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





class ConveryLinkedinUtility(ConveryNotification):



	def linkedin_login_function(self):



		#create linkedin driver (headless)
		#login with user identifiers
		
		

		driver = webdriver.Chrome()

		chrome_options = Options()
		#chrome_options.add_argument("--headless=new")

		username = self.app.user_settings["UserLinkedinAddress"]
		password = self.app.user_settings["UserLinkedinPassword"]

		
		try:
			driver.get("https://linkedin.com/login")



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


			#driver.fullscreen_window()

			
			



		except Exception as e:
			self.display_error_function("Impossible to login to linkedin page\n%s"%e)
			return False
		else:
			self.display_message_function("Logged in!")
			return driver





	def linkedin_get_studiolist_function(self, studio_name):


		
		#self.selectionlist_linkedin_contact.clear_options()


		driver = self.linkedin_login_function()

		if driver == False:
			print("Impossible to make connection")
			return 

		else:
			#self.display_message_function("Connected...")
			print("connected")
			#driver.fullscreen_window()

		
			input_container = driver.find_element(By.ID, "global-nav-search")
			input_field = driver.find_element(By.CLASS_NAME, "search-global-typeahead__input")


			#search
			input_container.click()
			input_field.send_keys(str(studio_name))
			input_field.send_keys(Keys.ENTER)
			



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
					print("clicked")
					element.click()
					#sleep(2)
					break



			#print("LIST COMPANY BUTTON")

			#wait for page to load
			sleep(2)

			list_company_button = driver.find_elements(By.CLASS_NAME,"app-aware-link")
			"""
			list_company_button = WebDriverWait(driver, 10).until(
			    EC.presence_of_all_elements_located((By.CLASS_NAME, "app-aware-link"))
			)
			"""

			linkedin_studio_list = {}
			for element in list_company_button:
				#get parent of widget
				parent = element.find_element(By.XPATH, "..")
				#print("parent name : [%s]"%parent.tag_name)
				if parent.tag_name == "span":
					if self.letter_verification_function(element.text) == True:
						print(colored("Studio added : %s"%element.text, "green"))
						#print(element.text)
						#print("		destination : %s"%element.get_attribute("href"))
						linkedin_studio_list[element.text] = element.get_attribute



			os.system("pause")
			return linkedin_studio_list
			

			




