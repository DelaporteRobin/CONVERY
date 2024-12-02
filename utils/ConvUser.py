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
import markdown

from functools import partial
from typing import  Iterable
from datetime import datetime 
from pyfiglet import Figlet 



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






class ConveryUserUtility():

###############################################################################################
#MANAGER USER SETTINGS
###############################################################################################
	def save_user_settings_function(self):
		os.makedirs("C:/Program Files/@RCHIVE/Data/User/", exist_ok=True)
		try:
			with open("C:/Program Files/@RCHIVE/Data/user/UserSettings.json", "w") as save_file:
				json.dump(self.app.user_settings, save_file, indent=4)
		except Exception as e:
			self.app.display_error_function("Impossible to save user settings\n%s"%e)
			return
		else:
			self.app.display_success_function("User settings saved")




	def load_user_settings_function(self):
		try:
			with open("C:/Program Files/@RCHIVE/Data/user/UserSettings.json", "r") as read_file:
				self.app.user_settings = json.load(read_file)
		except Exception as e:
			self.display_error_function("Impossible to load user settings\n%s"%e)
		else:
			self.display_success_function("User settings loaded")
			pass












###############################################################################################
#MANAGER COMPANY DICTIONNARY
###############################################################################################



	def save_company_dictionnary_function(self):
		os.makedirs("C:/Program Files/@RCHIVE/Data/User/", exist_ok=True)
		try:

			with open(os.path.join(os.getcwd(), "C:/Program Files/@RCHIVE/Data/User/UserCompanyData.json"), "w") as save_file:
				json.dump(self.app.company_dictionnary, save_file, indent=4)

		
		except Exception as e:
			self.display_error_function("Impossible to save dictionnary\n%s"%e)
			return False
		else:
			self.display_success_function("Dictionnary saved")
			return True





	def load_company_dictionnary_function(self):
		#COMMON FOLDER LOCATION FOR USER SETTINGS IS C:/Program Files
		try:
			with open(os.path.join("C:/Program Files/@RCHIVE/Data/User/UserCompanyData.json"), "r") as read_file:
				self.app.company_dictionnary = json.load(read_file)
		except Exception as e:
			self.display_error_function("Impossible to load company dictionnary\n%s"%e)
		else:
			self.display_success_function("Company dictionnary loaded")
			#self.display_message_function(self.app.company_dictionnary)
			pass
		"""
		try:	
			with open(os.path.join(os.getcwd(), "Data/User/UserCompanyData.json"), "r") as read_file:
				self.app.company_dictionnary = json.load(read_file)
		
		except Exception as e:
			self.display_error_function("Impossible to load company dictionnary\n%s"%e)
		else:
			#self.display_message_function("Company dictionnary loaded")
			pass
		"""





	def add_company_function(self):
		#self.display_message_function(self.date)
		#get informations
		company_informations = {
			#"CompanyName":self.query_one("#modal_newcompanyname").value,
			"CompanyLocation":self.query_one("#modal_newcompanylocation").value,
			"CompanyWebsite":self.query_one("#modal_newcompany_website").value,
			"CompanyLinkedin":self.query_one("#modal_newcompany_linkedin").value,
			"CompanyAnswer":None,
			"CompanyContact":None,
			"CompanyDetails":self.newcompany_details.text,
			"CompanyDate":None,
			"CompanyTags":[],
		}


		#get tags and split content
		tags_value = self.newcompany_tags.value.replace(" ", "").split(";")
		company_informations["CompanyTags"] = tags_value


		#DATE MODICATION
		date_value = self.modal_dateselect.date
		#self.display_message_function(date_value)

		if self.newcompany_contacted_checkbox.value == True:
			company_informations["CompanyDate"] = str(date_value)
		"""
		if checkbox == True and date == None --> self.date
		if checkbox == False --> None
		if checbox == True and date != None --> get date value
		"""
		"""
		if self.newcompany_contacted_checkbox.value == True:
			if company_informations["CompanyDate"]==None:
				company_informations["CompanyDate"] = str(self.date)
		"""


		if self.query_one("#modal_newcompany_answer").value == 1:
			company_informations["CompanyAnswer"] = True
		elif self.query_one("#modal_newcompany_answer").value == 2:
			company_informations["CompanyAnswer"] = False
		elif self.query_one("#modal_newcompany_answer").value == 3:
			company_informations["CompanyAnswer"] = None
		else:
			company_informations["CompanyAnswer"] = self.query_one("#modal_newcompany_otheranswer").text

		contact_type_list = self.query("#modal_newcontacttype")
		contact_name_list = self.query("#modal_newcontactname")
		contact_mail_list = self.query("#modal_newcontactmail")
		contact_website_list = self.query("#modal_newcontactwebsite")


		if len(contact_name_list) != len(contact_mail_list):
			self.display_error_function("Error trying to get contact informations")
			return
		else:

			general_dictionnary = {}
			job_dictionnary = {}
			member_dictionnary = {}
			

			for i in range(len(contact_type_list)):
				#self.display_message_function(contact_type_list[i].value)

				dictionnary = {
					"mail": contact_mail_list[i].value,
					"website": contact_website_list[i].value
				}

				if contact_type_list[i].value == "GENERAL":
					general_dictionnary[contact_name_list[i].value] = dictionnary 
				elif contact_type_list[i].value == "MEMBER":
					member_dictionnary[contact_name_list[i].value] = dictionnary
				elif contact_type_list[i].value == "JOB":
					job_dictionnary[contact_name_list[i].value] = dictionnary
				else:
					pass



			contact_dictionnary = {
				"GENERAL": general_dictionnary,
				"JOB": job_dictionnary,
				"MEMBER":member_dictionnary
			}


			#replace the value in the company dictionnary
			company_informations["CompanyContact"] = contact_dictionnary


			#replace the value in the company dictionnary and save the new dictionnary
			if (self.mode != "edit") and (self.query_one("#modal_newcompanyname").value in self.app.company_dictionnary):
				self.display_error_function("That company is already registered in the dictionnary")
			else:
				self.app.company_dictionnary[self.query_one("#modal_newcompanyname").value] = company_informations
				value = self.save_company_dictionnary_function()
				#update the value in interface
				self.app.update_informations_function()




	def delete_company_function(self):
		#studio = list(self.company_dictionnary.keys())[self.listview_studiolist.index]
		studio = self.list_studiolist_display[self.listview_studiolist.index]
		try:
			del self.company_dictionnary[studio]
		except:
			self.display_error_function("Impossible to remove studio")
			return
		else:
			self.display_success_function("Studio removed")
			self.save_company_dictionnary_function()
			self.update_informations_function()







	def load_company_data_function(self, Modal_Contact):
		self.display_message_function(self.studio)
		try:
			studio_data = self.app.company_dictionnary[self.studio]
		except:
			self.display_error_function("Impossible to get studio data")
		else:
			self.newcompany_name.value = self.studio 
			self.newcompany_location.value = studio_data["CompanyLocation"]
			self.newcompany_website.value = studio_data["CompanyWebsite"]
			self.newcompany_tags.value = ";".join(studio_data["CompanyTags"])

			if (studio_data["CompanyLinkedin"] != None) and (self.letter_verification_function(studio_data["CompanyLinkedin"]) == True):
				self.newcompany_linkedin.value = studio_data["CompanyLinkedin"]

			try:
				if self.letter_verification_function(studio_data["CompanyDetails"]) == False:
					self.newcompany_details.insert("-")
				else:
					self.newcompany_details.text = studio_data["CompanyDetails"]
			except:
				self.newcompany_details.insert("-")

			#self.display_message_function(studio_data)
			if "CompanyDate" in studio_data:
				if studio_data["CompanyDate"] != None:
					self.newcompany_contacted_checkbox.value = True
					self.query_one("#modal_collapsible_dateselector").disabled = False
					self.query_one("#modal_collapsible_dateselector").title = studio_data["CompanyDate"]

					if type(studio_data["CompanyDate"]) == str:
						self.modal_dateselect.date = pendulum.parse(studio_data["CompanyDate"])
					else:
						self.modal_dateselect.date = studio_data["CompanyDate"]
				else:
					self.newcompany_contacted_checkbox.value = False
					
					self.query_one("#modal_collapsible_dateselector").title = ""
					self.query_one("#modal_collapsible_dateselector").disabled = True
			else:
				self.newcompany_contacted_checkbox.value = False
					
				self.query_one("#modal_collapsible_dateselector").title = "Last time company was reached :"
				self.query_one("#modal_collapsible_dateselector").disabled = True
					



			if studio_data["CompanyAnswer"] == True:
				self.newcompany_answer.value = 1
			elif studio_data["CompanyAnswer"] == False:
				self.newcompany_answer.value = 2
			elif studio_data["CompanyAnswer"] == None:
				self.newcompany_answer.value = 3
			else:
				self.newcompany_otheranswer.disabled=False
				self.newcompany_answer.value = 4
				self.newcompany_otheranswer.text = studio_data["CompanyAnswer"]


			#LOAD CONTACTS IN PAGE
			"""
			if studio_data["CompanyContact"] != None:
				for i in range(len(list(studio_data["CompanyContact"].keys()))):

					#self.display_message_function(i)
					contact_name = list(studio_data["CompanyContact"].keys())[i]
					contact_mail = studio_data["CompanyContact"][contact_name]["mail"]
					contact_website = studio_data["CompanyContact"][contact_name]["website"]

					#self.display_message_function(contact_name)
					new_contact = Modal_Contact("JOB", contact_name, contact_mail, contact_website)
					self.newcompany_contactlist_container.mount(new_contact)
			"""
			if studio_data["CompanyContact"] != None:
				for contact_type, contact in studio_data["CompanyContact"].items():
					for c_name, c_data in contact.items():

						contact_name = c_name
						contact_mail = c_data["mail"]
						contact_website = c_data["website"]

						new_contact = Modal_Contact(contact_type, contact_name, contact_mail, contact_website)
						self.newcompany_contactlist_container.mount(new_contact)









	def save_contact_sheet_function(self):
		#get data from the company dictionnary
		#self.display_message_function(list(self.company_dictionnary.keys()))	



		"""
		formatting for one studio ex

		location
			studio_name
				studio website : 
				studio linkedin :
				studio contact:
					contact_type
						contact_name:
							mail:
							website:
					contact_type
						contact_name
							mail 
							website
		"""		

		#location list
		self.display_message_function("Classing studios by location...")
		#self.display_message_function("Creating markdown for studios")

		location_dictionnary = {}
		for studio_name, studio_data in self.company_dictionnary.items():

			studio_markdown = f"""
### %s
- Studio Website : %s
- Studio Linkedin : %s
- Studio contact list:
"""%(studio_name.upper(),studio_data["CompanyWebsite"], studio_data["CompanyLinkedin"])
			
			for contact_type, contact_list in studio_data["CompanyContact"].items():

				if contact_list != {}:
					studio_markdown+=f"""
	##### %s
"""%(contact_type)

					for c_name, c_data in contact_list.items():
						studio_markdown+=f"""
		- %s
"""%c_name
						if self.letter_verification_function(c_data["mail"])==True:
							studio_markdown+=f"""
			%s
"""%c_data["mail"]
						if self.letter_verification_function(c_data["website"])==True:
							studio_markdown+=f"""
			%s
"""%c_data["website"]

			
			#get location of the studio
			#and create the location dictionnary
			studio_location_list = studio_data["CompanyLocation"].upper().split("/")


			for studio_location in studio_location_list:
				if self.letter_verification_function(studio_location)==True:
					if studio_location not in location_dictionnary:
						location_dictionnary[studio_location] = [
							(studio_name, studio_markdown)
						]
					else:
						#get the dictionnary from the current location of the studio
						studio_loc_dictionnary = location_dictionnary[studio_location]
						studio_loc_dictionnary.append( (studio_name, studio_markdown) )
						location_dictionnary[studio_location] = studio_loc_dictionnary

		self.display_success_function("Location dictionnary created")

		
		final_markdown = ""
		for location, studio_data in location_dictionnary.items():
			self.display_message_function("Location detected : %s"%location, True)
			final_markdown += "\n## [%s]\n"%location

			for studio in studio_data:
				final_markdown+=studio[1]


		with open("test.md", "w", encoding="utf-8") as save_file:
			save_file.write(final_markdown)

		input_file = "test.md"  # Remplacez par le chemin de votre fichier
		output_file = "output.html"

		with open(input_file, "r", encoding="utf-8") as md_file:
		    markdown_content = md_file.read()

		# Convertir le Markdown en HTML
		html_content = markdown.markdown(markdown_content, extensions=["extra", "tables", "sane_lists"])

		# Envelopper dans une structure HTML de base
		html_output = f"""
		<!DOCTYPE html>
		<html lang="en">
		<head>
		    <meta charset="UTF-8">
		    <meta name="viewport" content="width=device-width, initial-scale=1.0">
		    <title>Markdown to HTML</title>
		</head>
		<body>
		{html_content}
		</body>
		</html>
		"""

		# Sauvegarder dans un fichier HTML
		with open(output_file, "w", encoding="utf-8") as html_file:
		    html_file.write(html_output)

		#print(f"Conversion terminée ! Le fichier HTML est sauvegardé sous : {output_file}")

		self.display_success_function("saved")



		"""
		final_path = "CompanyDictionnary_SAVE.html"
		convert_result = self.convert_md_to_html_function(final_markdown, final_path)
		if convert_result == True:
			self.display_success_function("Markdown converted into .html and saved")
		else:
			self.display_error_function(str(convert_result))
		"""







