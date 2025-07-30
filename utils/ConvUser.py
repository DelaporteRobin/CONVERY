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
import validators
import traceback
import dropbox
import requests

from functools import partial
from typing import  Iterable
from datetime import datetime, timedelta
from pyfiglet import Figlet 
from tabulate import tabulate
from whenever import *
from dropbox.exceptions import ApiError, AuthError, BadInputError
from io import BytesIO


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

from utils.ConvWidget import MultiListItem, MultiListView






class ConveryUserUtility():

###############################################################################################
#MANAGE TAGS
###############################################################################################
	def create_tag_function(self):
		#get the content of the input field
		tag_name = self.input_create_tag.value
		if self.letter_verification_function(tag_name)==True:
			#check if the tag name already exists
			if tag_name not in self.user_settings["UserTagList"]:
				#add the tag to the tag list
				self.tag_list = self.user_settings["UserTagList"]
				self.tag_list.append(tag_name)
				self.user_settings["UserTagList"] = self.tag_list

				#update the tag suggester?
				self.tag_suggester = MultiWordSuggester(self.tag_list, case_sensitive=False)

				self.save_user_settings_function()
				self.display_message_function("Tag successfully created", "success")
				return True
			else:
				self.display_message_function("This tag is already existing", "error")
				return False
		else:
			self.display_message_function("You have to enter a valid tag name", "error")
			return False



	def add_tag_to_selection_function(self):
		#get the tag selection
		selected_tag_list = self.selectionlist_tags_settings.selected
		if type(selected_tag_list) == int:
			selected_tag_list = [selected_tag_list]
		#get the studio selection
		selected_studio_list = self.listview_studiolist.index_list

		#self.display_message_function(self.listview_studiolist.index_list)
		#return

		#studio_name_list = list(self.company_dictionnary.keys())

		#create the tag list
		tag_list = []
		for index in selected_tag_list:
			tag_list.append(self.user_settings["UserTagList"][index])

		for studio_index in selected_studio_list:
			studio_name = self.list_studiolist_display[studio_index]
			studio_data = self.company_dictionnary[studio_name]

			for tag in tag_list:
				if tag not in studio_data["CompanyTags"]:
					self.display_message_function("Tag added to studio tag list")
					studio_data["CompanyTags"].append(tag)

			self.company_dictionnary[studio_name] = studio_data
			self.save_company_dictionnary_function()

			self.display_message_function("Tag saved for studio : %s"%studio_name, "success")
		"""
		for selected_studio_index in selected_studio_list:
			studio_data = self.company_dictionnary[studio_name_list[selected_studio_index]]
			studio_tag_list = studio_data["CompanyTags"]

			for tag in tag_list:
				studio_tag_list.append(tag)

			studio_data["CompanyTags"] = studio_tag_list
			self.company_dictionnary[studio_name_list[selected_studio_index]] = studio_data

		self.save_company_dictionnary_function()
		"""
		



	#def delete_tag_function(self):
	#	tag_index_list = 

###############################################################################################
#MANAGER USER SETTINGS
###############################################################################################
	def save_user_settings_function(self):
		#os.makedirs("C:/Program Files/@RCHIVE/Data/User/", exist_ok=True)
		os.makedirs(os.path.join(os.getcwd(), "data/user"), exist_ok=True)
		try:
			with open(os.path.join(os.getcwd(), "data/user/UserSettings.json"), "w") as save_file:
				json.dump(self.app.user_settings, save_file, indent=4)
		except Exception as e:
			self.app.display_message_function("Impossible to save user settings\n%s"%e, "error")
			return
		else:
			self.app.display_message_function("User settings saved", "success")

	def load_user_settings_function(self):
		try:
			with open(os.path.join(os.getcwd(), "data/user/UserSettings.json"), "r") as read_file:
				self.app.user_settings = json.load(read_file)
		except Exception as e:
			self.display_message_function("Impossible to load user settings!", "error")
			#self.display_error_function("Impossible to load user settings")
		else:
			self.display_message_function("User settings loaded", "success")
			pass


###############################################################################################
#MANAGER COMPANY DICTIONNARY
###############################################################################################


	def create_company_class_function(self):
		#get the name in the textfield
		new_class_name = self.input_classname.value 
		#check if there is letter in the name
		if self.letter_verification_function(new_class_name)!=True:
			self.display_message_function("You must define a valid name for the new contact class!","error")
			return
		else:
			#check if the class is already in the class list
			if new_class_name in list(self.company_class_dictionnary.keys()):
				self.display_message_function("This name is already used by an other contact class!","error")
				return
			else:
				#create the new dictionnary
				self.company_class_dictionnary[new_class_name] = {}
				#save the dictionnary
				value = self.save_company_dictionnary_function()

				if value == True:
					#update the list in the lobby
					self.update_contact_class_function()
				else:
					self.display_message_function("Impossible to save the new contat dictionnary in file!","error")



	def save_company_dictionnary_function(self):
		#get the current class selected
		#replace the dictionnary in it
		#save the new dictionnary for this class
		#self.app.current_class_selected = list(self.app.company_class_dictionnary.keys())[self.app.listview_contacttype.index]
		#update the dictionnary



		os.makedirs(os.path.join(os.getcwd(), "data/user"), exist_ok=True)
		try:

			with open(os.path.join(os.getcwd(), "data/user/UserCompanyData.json"), "w") as save_file:
				json.dump(self.app.company_class_dictionnary, save_file, indent=4)

		
		except Exception as e:
			self.display_message_function("Impossible to save dictionnary\n%s"%e, "error")
			return False
		else:
			self.display_message_function("Dictionnary saved", "success")
			return True





	def load_company_dictionnary_function(self):
		#COMMON FOLDER LOCATION FOR USER SETTINGS IS C:/Program Files
		try:
			with open(os.path.join(os.getcwd(), "data/user/UserCompanyData.json"), "r") as read_file:
				self.app.company_dictionnary = json.load(read_file)
		except Exception as e:
			pass
			#self.display_error_function("Impossible to load company dictionnary\n%s"%e)
		else:
			self.display_message_function("Company dictionnary loaded", "success")
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

		user_tag_list = self.app.user_settings["UserTagList"]
		for tag in tags_value:
			if tag not in user_tag_list:
				user_tag_list.append(tag)
		self.app.user_settings["UserTagList"]



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
			self.display_message_function("Error trying to get contact informations", "error")
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
				self.display_message_function("That company is already registered in the dictionnary", "error")
			else:
				#create the new key in the dictionnary
				self.app.company_dictionnary[self.query_one("#modal_newcompanyname").value] = company_informations
				#update the class dictionnary and save it
				#get the current class selected
				self.app.company_class_dictionnary[self.app.current_class_selected] = self.app.company_dictionnary

				value = self.save_company_dictionnary_function()
				self.save_user_settings_function()
				#update the value in interface
				self.app.update_informations_function()






	def delete_company_function(self):
		#studio = list(self.company_dictionnary.keys())[self.listview_studiolist.index]
		studio = self.list_studiolist_display[self.listview_studiolist.index]
		try:
			del self.company_dictionnary[studio]
		except:
			self.display_message_function("Impossible to remove studio", "error")
			return
		else:
			self.display_message_function("Studio removed", "success")
			self.save_company_dictionnary_function()
			self.update_informations_function()




	def load_company_class_function(self):
		try:
			with open("data/user/UserCompanyData.json", "r") as read_file:
				self.app.company_class_dictionnary = json.load(read_file)
		except Exception as e:
			self.display_error_function("Impossible to load company data!\n%s", "error")
		else:
			self.display_message_function("Contact data file opened!", "success")


	def load_company_data_function(self, Modal_Contact):
		self.display_message_function(self.studio)
		try:
			studio_data = self.app.company_dictionnary[self.studio]
		except:
			self.display_error_function("Impossible to get studio data", "error")
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
					self.query_one("#modal_collapsible_dateselector").disabled=False
					self.query_one("#modal_collapsible_dateselector").title = studio_data["CompanyDate"]

					#update the value of the date in the date picker
					#try to cover the date conversion
					try:
						converted_date = datetime.strptime(studio_data["CompanyDate"], "%Y-%m-%dT%H:%M:%S.%f%z")
					except ValueError:
						converted_date = datetime.strptime(studio_data["CompanyDate"], "%Y-%m-%d")
					#date object
					date_object = Date.from_py_date(converted_date)
					#set the date in the date picker
					self.modal_dateselect.date = date_object

			"""
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
			"""
					



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


	def save_contact_table_function(self):

		#create table
		data = [
			["LOCATION", "STUDIO NAME", "WEBSITE", "LINKEDIN", "CONTACT"]
		]


		location_dictionnary = {}

		for studio_name, studio_data in self.company_dictionnary.items():

			contact_str = ""

			for contact_genre, contact_data in studio_data["CompanyContact"].items():
				if contact_data != {}:
					contact_str += "%s\n"%contact_genre.upper()
					for contact_name, contact_coordinate in contact_data.items():
						contact_str+= """
	- %s:
		mail : %s
		website : %s
"""%(contact_name, contact_coordinate["mail"], contact_coordinate["website"])

			#data.append( [studio_data["CompanyLocation"].upper(), studio_name, studio_data["CompanyWebsite"], studio_data["CompanyLinkedin"], contact_str] )
			location_list = studio_data["CompanyLocation"].upper().split("/")
			for location in location_list:
				if self.letter_verification_function(location)==True:
					if location not in location_dictionnary:
						self.display_message_function("New location detected : %s"%location)
						location_dictionnary[location] = [[location, studio_name, studio_data["CompanyWebsite"], studio_data["CompanyLinkedin"], contact_str] ]
					else:
						load = location_dictionnary[studio_data["CompanyLocation"].upper()]
						load.append([location, studio_name, studio_data["CompanyWebsite"], studio_data["CompanyLinkedin"], contact_str] )
						location_dictionnary[location] = load 
		self.display_message_function("location dictionnary created", "success")


		


		for location, location_data in location_dictionnary.items():
			self.display_message_function("All studios added for that location : %s"%location)
			for row in location_data:
				data.append(row) 



		#create html content
		html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<title>Tableau des Studios</title>
	<style>
		/* Général */
		body {
			font-family: 'Arial', sans-serif;
			background-color: #f4f4f4;
			color: #333;
			margin: 0;
			padding: 0;
		}

		h1 {
			text-align: center;
			margin: 20px 0;
			color: #2c3e50;
		}

		/* Tableau */
		table {
			width: 100%;
			border-collapse: collapse;
			margin: 20px 0;
		}

		th, td {
			padding: 12px;
			text-align: left;
			vertical-align: top;
		}

		th {
			background-color: #2c3e50;
			color: #fff;
			font-size: 1.1em;
		}

		td {
			background-color: #fff;
			border: 1px solid #ddd;
		}

		tr:nth-child(even) td {
			background-color: #f9f9f9;
		}

		tr:hover {
			background-color: #f1f1f1;
		}

		/* Liens */
		a {
			color: #2980b9;
			text-decoration: none;
			transition: color 0.3s ease;
		}

		a:hover {
			color: #3498db;
		}

		/* Texte et préformatage */
		pre {
			white-space: pre-wrap;
			word-wrap: break-word;
			margin: 0;
		}

	</style>
</head>
<table border='1'>
"""
		
		for i in range(len(data)):
			if i == 0:
				html_content += self.save_html_row_function(data[i], "th")
			else:
				html_content += self.save_html_row_function(data[i], "td")

		html_content += "</table>\n"
		self.display_message_function("Table .html created", "success")

		table_text = tabulate(data, headers="firstrow", tablefmt="grid")
		self.display_message_function("Table .txt created", "success")


		filename = os.path.join(os.getcwd(), "CompanyData_Export.txt")
		filename_html = os.path.join(os.getcwd(), "CompanyData_Export.html")

		with open(filename, "w", encoding="utf-8") as file:
			file.write(table_text)

		with open(filename_html, "w", encoding="utf-8") as file_html:
			file_html.write(html_content)



		self.display_message_function("All files saved : [ %s ] [ %s ]"%(filename, filename_html), "success")






	def save_html_row_function(self, row_list, tag):
		html_output = "\t<tr>\n"

		for row_item in row_list:

			row_item = str(row_item)
			if "\n" in row_item:
				row_item = row_item.replace("\n", "<br>")

			#replace link in html
			splited_content = row_item.split(" ")
			for i in range(len(splited_content)):
				if self.check_for_url_function(splited_content[i]) == True:
					#self.display_success_function("URL DETECTED")
					splited_content[i] = "<a href='%s'>%s</a>"%(splited_content[i],splited_content[i])
			#final assemble
			row_item = " ".join(splited_content)

			html_output += "<%s><pre>%s</pre></%s>\n"%(tag,row_item,tag)


		html_output+="\t</tr>\n"
		return html_output



	def check_for_url_function(self, content):
		return validators.url(content)



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

		self.display_message_function("Location dictionnary created", "success")

		
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

		self.display_message_function("Contact sheet saved successfully", "success")



		"""
		final_path = "CompanyDictionnary_SAVE.html"
		convert_result = self.convert_md_to_html_function(final_markdown, final_path)
		if convert_result == True:
			self.display_success_function("Markdown converted into .html and saved")
		else:
			self.display_error_function(str(convert_result))
		"""

	#check if contact list is on website
	#	yes → download contact list and compare
	#	no → load contact list on website
	def dropbox_check_function(self):
		if "UserDropboxToken" not in self.user_settings:
			self.display_message_function("Token is not saved in user settings!", "error")
			return
		else:
			value=False
			try:
				self.dbx = dropbox.Dropbox(self.user_settings["UserDropboxToken"])

				#get the content on dropbox
				content = self.dbx.files_list_folder(path="")
				
				self.dropbox_contactlist_path = "Convery_UserCompanyData.json"
				for item in content.entries:
					
					self.display_message_function("%s;%s : %s"%(item.name,self.dropbox_contactlist_path,item.name==self.dropbox_contactlist_path))
					if (item.name == self.dropbox_contactlist_path):
						self.display_message_function("File found...", "success")
						value=True
						break
					"""
					self.display_message_function("%s : %s"%(item.name, "Convery_UserCompanyData.json"))
					if item.name == "Convery_UserCompanyData.json"==True:
						self.display_success_function("File found...")
						value=True
						break
					"""
		

				if value==True:
					self.display_message_function("Contact list detected on dropbox", "success")
					self.dropbox_compare_contact_function()
				else:
					self.display_message_function("Contact list not detected on dropbox", "error")
					self.dropbox_transfer_contact_function()


			except AuthError as e:
				if e.error.is_expired_access_token():
					self.display_message_function("Invalid token, impossible to connect to dropbox!", "error")
					return
				elif e.error.is_missing_scope():
					self.display_message_function("Missing permissions to perform this action on dropbox!", "error")
					return
				else:
					self.display_message_function("Invalid authentication on dropbox", "error")
					return
			else:
				self.display_message_function("Content retrieved from dropbox", "success")

	def dropbox_transfer_contact_function(self):
		if os.path.isfile("data/user/UserCompanyData.json")==False:
			self.display_message_function("Contact list file doesn't exists")
			return
		else:
			source_file = os.path.join(os.getcwd(), "data/user/UserCompanyData.json")
			destination_file = "/Convery_UserCompanyData.json"

			try:
				with open(source_file,"rb") as transfer_file:
					self.dbx.files_upload(transfer_file.read(), destination_file, mode=dropbox.files.WriteMode.overwrite)
				self.display_message_function("Contact list uploaded on dropbox", "success")
			except Exception as e:
				self.display_message_function("Error happened while transfering contact list on dropbox", "error")
				self.display_message_function(e)

	def dropbox_compare_contact_function(self):
		try:
			metadata, response = self.dbx.files_download("/%s"%self.dropbox_contactlist_path)
			self.dropbox_contactlist = json.load(BytesIO(response.content))

			self.display_message_function("Contact list loaded from dropbox", "success")
			self.display_message_function(len(list(self.dropbox_contactlist.keys())))

		
		except Exception as e:
			self.display_message_function("Failed to load data from contact list", "error")
			self.display_message_function(e, "error")
		else:
			"""
			CHECK THE CONTENT OF BOTH CONTACT LIST AND COMPARE
			- go through local dictionnary
				- check if all cat are present
				- for each contact check if it is in the other dictionnary
					if yes --> pass
					if not --> add it
			"""
			self.display_message_function("UPDATE LOCAL CONTACT LIST...")
			for contact_class, contact_dictionnary in self.dropbox_contactlist.items():
				self.display_message_function(f"  Checking class {contact_class}")
				if contact_class not in list(self.company_class_dictionnary.keys()):
					self.company_class_dictionnary[contact_class] = contact_dictionnary
					self.display_message_function(f"  Contact class added → {contact_class}")
				else:
					#go through each contact of the contact class and check if it is in the 
					for contact_name, contact_data in contact_dictionnary.items():
						if contact_name not in list(self.company_class_dictionnary[contact_class].keys()):
							self.company_class_dictionnary[contact_class][contact_name] = contact_data
							self.display_message_function(f"    Contact added → {contact_name}")
				
			self.display_message_function("UPDATE DROPBOX CONTACT LIST...")
			for contact_class, contact_dictionnary in self.company_class_dictionnary.items():
				self.display_message_function(f'  Checking class {contact_class}')
				if contact_class not in list(self.dropbox_contactlist.keys()):
					self.dropbox_contactlist[contact_class] = contact_dictionnary
					self.display_message_function(f"  Contact class added → {contact_class}")
				else:
					for contact_name, contact_data in contact_dictionnary.items():
						if contact_name not in list(self.dropbox_contactlist[contact_class].keys()):
							self.dropbox_contactlist[contact_class][contact_name] = contact_data
							self.display_message_function(f'    Contact added → {contact_name}')
			self.display_message_function("All dictionnary updated...", "success")
			self.save_company_dictionnary_function()
			#convert the dropbox dictionnary into a json object
			dropbox_contactlist_converted = json.dumps(self.dropbox_contactlist, indent=4, ensure_ascii=False)
			#upload the new file on dropbox
			try:
				self.dbx.files_upload(dropbox_contactlist_converted.encode("utf-8"),"/Convery_UserCompanyData.json",mode=dropbox.files.WriteMode.overwrite)
				self.display_message_function("New contact list uploaded on dropbox", "success")
			except Exception as e:
				self.display_message_function(f'Impossible to upload contact list on dropbox\n{traceback.format_exc()}', "error")


	def dropbox_get_authentification_url_function(self, appkey=None, appsecret=None):
		#try to get authentification url from dropbox
		try:
			self.auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(appkey,appsecret,token_access_type="offline")
			authorize_url = self.auth_flow.start()
			self.app.display_message_function("URL RETRIEVED : %s"%authorize_url, "success")
			return authorize_url
		except Exception as e:
			self.app.display_error_function("Error happened while trying to get authentification URL")
			self.app.display_error_function(traceback.format_exc())
			return False

	def dropbox_get_tokens_function(self,auth_code=None):
		#get tokens from the access code 
		if self.auth_flow == None:
			self.app.display_error_function("You need to get url and enter code before trying to get tokens")
			return
		else:
			#try to retrieve tokens
			try:
				exchange = self.auth_flow.finish(auth_code)
				self.app.user_settings["UserDropboxAccessToken"] = exchange.access_token  
				self.app.user_settings["UserDropboxRefreshToken"] = exchange.refresh_token,
				self.app.user_settings["UserDropboxTokenExpiration"] = (datetime.now() + timedelta(hours=4)).isoformat()
				#save user settings
				self.app.save_user_settings_function()
			except Exception as e:
				self.app.display_error_function("Impossible to exchange tokens")
				self.app.display_error_function(traceback.format_exc())
			else:
				#test connections with tokens
				try:
					dbx = dropbox.Dropbox(exchange.access_token)
					account = dbx.users_get_current_account()
					self.display_message_function("Connected to dropbox service as : %s"%account.name.display_name, "success")
					return True
				except Exception as e:
					self.app.display_error_function("Impossible to connect with access token")
					self.app.display_error_function(traceback.format_exc())
					return False
	def dropbox_connection_function(self):
		#check if values are saved in dictionnary
		if ("UserDropboxAccessToken" not in self.user_settings) or ("UserDropboxRefreshToken" not in self.user_settings):
			self.display_message_function("You have to launch authentification process once, \nbefore being able to connect with Dropbox services", "error")
			return
		else:
			expire = datetime.fromisoformat(self.user_settings["UserDropboxTokenExpiration"])
			#token needs to be refreshed
			if (datetime.now() >= (expire-timedelta(minutes=10)))==True:

				#token doesn't need to be updated <=> can login
				refresh_url = "https://api.dropboxapi.com/oauth2/token"
				data = {
					"grant_type":"refresh_token",
					"refresh_token":self.user_settings["UserDropboxRefreshToken"],
					"client_id":self.user_settings["UserDropboxKey"],
					"client_secret":self.user_settings["UserDropboxSecret"]
				}
				response=requests.post(refresh_url,data=data)
				result = response.json()
				if "access_token" in result:
					new_access_token=result["access_token"]
					new_refresh_token=result.get("refresh_token",self.user_settings["UserDropboxRefreshToken"])

					self.user_settings["UserDropboxAccessToken"]=new_access_token
					self.user_settings["UserDropboxRefreshToken"]=new_refresh_token
					self.user_settings["UserDropboxTokenExpiration"] = (datetime.now() + timedelta(hours=4)).isoformat()
					self.save_user_settings_function()
					#self.display_success_function("Token refreshed successfully")
					self.display_message_function(f"Token refreshed successfully\nNew access token : {new_access_token}\nNew refresh token : {new_refresh_token}", "success")
				else:
					self.display_message_function("Error while trying to refresh tokens", "error")
					self.display_message_function(result)	
		
			#self.display_message_function("Tokens doesn't need to be refreshed")
			#launch connection with dropbox
			try:
				self.dbx = dropbox.Dropbox(self.user_settings["UserDropboxAccessToken"])
				account = self.dbx.users_get_current_account()
				self.display_message_function(f"Connected to dropbox : {account.name.display_name}", "success")
			except Exception as e:
				self.display_message_function("Impossible to connect to dropbox\n%s"%traceback.format_exc(), "error")

			#check if the config file is on dropbox
			content = self.dbx.files_list_folder(path="")
			value=False
			self.dropbox_contactlist_path = "Convery_UserCompanyData.json"
			for item in content.entries:
				
				self.display_message_function("%s;%s : %s"%(item.name,self.dropbox_contactlist_path,item.name==self.dropbox_contactlist_path))
				if (item.name == self.dropbox_contactlist_path):
					self.display_message_function("File found...", "success")
					value=True
					break
			#contact list is not on dropbox
			#need to load it on website
			if value==False:
				self.display_message_function("Contact list not detected on dropbox")
				self.dropbox_transfer_contact_function()
			else:
				self.display_message_function("Contact list detected on dropbox")
				self.dropbox_compare_contact_function()









