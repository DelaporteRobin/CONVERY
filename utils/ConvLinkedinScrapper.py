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
import traceback

from functools import partial
from typing import  Iterable
from datetime import datetime 
from pyfiglet import Figlet 
from time import sleep
from termcolor import *


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



from textual.suggester import SuggestFromList, Suggester
from textual.app import App, ComposeResult
from textual.widgets import Markdown, MarkdownViewer, DataTable,TextArea, RadioSet, RadioButton, Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option
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




class Modal_PostFormatting(Static):
	CSS_PATH = ["Styles/layout.tcss"]
	def __init__(self, post_content):
		super().__init__()
		self.post_content = post_content

	def compose(self) -> ComposeResult:
		with Vertical(id = "vertical_linkedinpost_container"):
			with Horizontal(id = "horizontal_linkedinpost_container"):
				self.label_linkedinpost_author = Label(self.post_content["POSTACCOUNT"].upper(), id="label_linkedinpost_author")
				yield self.label_linkedinpost_author
				self.label_linkedinpost_author.border_title = "Post author"

				self.label_linkedinpost_date = Label(self.post_content["POSTDATE"], id="label_lnkedinpost_date")
				yield self.label_linkedinpost_date
				self.label_linkedinpost_date.border_title = "Post date"




class ConveryLinkedinScrapperApplication():

	def load_linkedin_post_function(self):
		#try to get the content of the post file
		if self.get_linkedin_log_function() == False:
			self.display_error_function("Impossible to display linkedin scrapping content")
			return
		#get the last post loaded
		last_post = self.linkedin_scrapping_log[list(self.linkedin_scrapping_log.keys())[-1]]
		#self.display_message_function(last_post["POSTCONTENT"][0])

		new_post = Modal_PostFormatting(last_post)
		self.vertical_linkedinpost.mount(new_post)
		self.display_success_function("Mounted")




	def get_linkedin_log_function(self):
		try:
			with open(os.path.join(os.getcwd(), "data/LinkedinScrapping.json"), "r") as linkedin_scrapping_file:
				self.linkedin_scrapping_log = json.load(linkedin_scrapping_file)
		except Exception as e:
			self.display_error_function("Impossible to load Linkedin Scrapping content!")
			return False
		else:
			self.display_success_function("Linkedin scrapping log content loaded successfully!")
			return True