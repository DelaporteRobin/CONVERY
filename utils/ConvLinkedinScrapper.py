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
				"info":"yellow",
				"danger":"orange3",
			}
		)
		#create the rich console
		self.console = Console(theme=self.rich_theme)




		self.display_title_function()




	def display_title_function(self):
		self.console.log(pyfiglet.figlet_format("CONVERY\nLinkedin Scrapper", font="the_edge"), style="danger")




if __name__ == "__main__":
	LinkedinScrapperApplication()