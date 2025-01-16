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
from utils.ConvMail import ConveryMailUtility
from utils.ConvUtility import ConveryUtility
from utils.ConvNotif import ConveryNotification
from utils.ConvWidget import MultiListView, MultiListItem






class ConveryGUIUtils(ConveryUserUtility):

	def update_informations_function(self):
		#LOAD ALL INFORMATIONS CONTAINED IN USER SETTINGS FILES
		self.listview_studiolist.clear()
		self.listview_mailpreset.clear()
		self.textarea_prompt.clear()

		self.load_company_dictionnary_function()
		self.load_mail_preset_function()
		self.load_user_settings_function()




		self.input_mailkey.value = str(self.user_settings["UserMailKey"])
		self.input_useraddress.value = str(self.user_settings["UserMailAddress"])
		self.input_demolink.value = str(self.user_settings["UserDemoReelLink"])
		self.input_demopassword.value = str(self.user_settings["UserDemoReelPassword"])
		self.input_resume.value = str(self.user_settings["UserMailAttached"])


		if ((self.user_settings["UserLinkedinAddress"])!=None) and (self.letter_verification_function(self.user_settings["UserLinkedinAddress"])):
			self.input_linkedin_username.value = self.user_settings["UserLinkedinAddress"]
		if ((self.user_settings["UserLinkedinPassword"])!=None) and (self.letter_verification_function(self.user_settings["UserLinkedinPassword"])):
			self.input_linkedin_password.value = self.user_settings["UserLinkedinPassword"]





		#create the studio suggest list for mail contact
		self.studio_suggest_list.clear()
		self.studio_suggest_list = list(self.company_dictionnary.keys())
		self.input_mailcontact.suggester=SuggestFromList(self.studio_suggest_list, case_sensitive=False)

		self.listview_contactlist.clear()
		for suggest in self.studio_suggest_list:
			self.listview_contactlist.append(MultiListItem(Label(suggest)))





		#CREATE THE CONTACT LIST
		"""
		for studio_name, studio_data in self.company_dictionnary.items():
			for contact_name, contact_data in studio_data["CompanyContact"].items():
				if self.letter_verification_function(contact_data["mail"])==True:
					self.contact_list[contact_data["mail"]] = {
						"studioName":studio_name,
						"studioContactName":contact_name
						}
		for contact_addres, contact_data in self.contact_list.items():
			label = Label("[ %s ] - %s"%(contact_addres, contact_data["studioName"]))
			self.listview_contactlist.append(ListItem(label)) 
		"""







		if "CopilotPrompt" in self.user_preset:
			self.textarea_prompt.insert(self.user_preset["CopilotPrompt"])


		if "mailPreset" in self.user_preset:
			preset_list = list(self.user_preset["mailPreset"].keys())

			for preset in preset_list:
				self.listview_mailpreset.append(MultiListItem(Label(preset)))




		self.list_studiolist = list(self.company_dictionnary.keys())
		self.list_studiolist_filtered = []

		for studio in self.list_studiolist:
			self.list_studiolist_filtered.append(unidecode.unidecode(studio.lower()))

		self.list_studiolist_display = []
		#self.list_studiolist_filtered = []



		
		#NOT BY PRIORITY ORDER
		if self.user_settings["companyDisplayMode"] != 2:
			try:
				self.display_message_function("Display mode selected : NOT PRIORITY ORDER")
				if self.user_settings["companyDisplayMode"] != 2:


					self.list_studiolist_display = list(self.company_dictionnary.keys())

					#BY ALPHABETIC ORDER
					if  (self.user_settings["companyDisplayMode"] == 0):
						self.list_studiolist_display.sort(key = str.lower)
			except KeyError:
				pass





		#BY PRIORITY ORDER
		else:	
			self.display_message_function("Display mode selected : PRIORITY ORDER")

			self.not_contacted_list.clear()
			self.no_alert_list.clear()
			self.short_alert_list.clear()
			self.medium_alert_list.clear()
			self.long_alert_list.clear()
			

			self.highlight_studio_list.clear()


			for studio_name, studio_data in self.company_dictionnary.items():

				#check the highlight list
				#check tag in studio_data 
				




				if ("CompanyDate" not in studio_data) or (studio_data["CompanyDate"] == None):
					self.not_contacted_list.append(studio_name)

				else:
					date = self.company_dictionnary[studio_name]["CompanyDate"]

					if type(date) == str:
						date = pendulum.parse(date).to_date_string()
						date = datetime.strptime(date, "%Y-%m-%d")

					delta = (datetime.now() - date).days
					average_month_day = 365.25 / 12
					delta_month = int(delta / average_month_day)
					delta_week = int(delta / 7)



					"""
					if delta_week >= self.user_settings["alertDictionnary"]["PastContact"]["Delta"]:
						long_alert_list.append(studio_name)

					if (delta_week >= self.user_settings["alertDictionnary"]["LatelyContact"]["Delta"]) and (delta_week < self.user_settings["alertDictionnary"]["PastContact"]["Delta"]):
						medium_alert_list.append(studio_name)

					if (delta_week >= self.user_settings["alertDictionnary"]["RecentContact"]["Delta"]) and (delta_week < self.user_settings["alertDictionnary"]["LatelyContact"]["Delta"]):
						short_alert_list.append(studio_name)

					else:
						no_alert_list.append(studio_name)
					"""



					#CREATION OF ALERT LIST
					alert_data = self.user_settings["alertDictionnary"]

					if delta_week < alert_data["RecentContact"]["Delta"]:
						self.no_alert_list.append(studio_name)

					elif (delta_week >= alert_data["RecentContact"]["Delta"]) and (delta_week < alert_data["LatelyContact"]["Delta"]):
						self.short_alert_list.append(studio_name)

					elif (delta_week >= alert_data["LatelyContact"]["Delta"]) and (delta_week < alert_data["PastContact"]["Delta"]):
						self.medium_alert_list.append(studio_name)

					else:
						self.long_alert_list.append(studio_name)

					



			#concatenate all list
			self.list_studiolist_display = self.long_alert_list + self.medium_alert_list + self.short_alert_list + self.no_alert_list + self.not_contacted_list


		self.update_studiolist_view()











	def update_studiolist_view(self):


		#update the tag list
		self.tag_list.clear()

		#update all the tag list in the view with the usertaglist
		#which is supposed to be correctly updated!!
		user_tag_list = self.user_settings["UserTagList"]
		self.selectionlist_tags.clear_options()
		self.selectionlist_tags_settings.clear_options()

		for i in range(len(user_tag_list)):
			self.selectionlist_tags.add_option((user_tag_list[i], i))
			self.selectionlist_tags_settings.add_option((user_tag_list[i], i))


		#FOR EACH STUDIO IN THE STUDIO LIST ADD IT TO THE LIST WITH THE RIGHT COLOR
		for studio in self.list_studiolist_display:



			#UPDATE THE FILTERED STUDIO LIST 
			#remove unwanted informations from studio
			#remove capital letters / accents
			#self.list_studiolist_filtered.append(unidecode.unidecode(studio).lower())
			#self.display_message_function(self.list_studiolist_filtered[-1])




			#get tag list in company dictionnary
			studio_tags = self.company_dictionnary[studio]["CompanyTags"]

			#self.selectionlist_tags.clear_options()
			#self.selectionlist_tags_settings.clear_options()

			
			for tag in studio_tags:
				if tag not in self.tag_list:
					if self.letter_verification_function(tag)==True:
						self.tag_list.append(tag)


			"""
			for i in range(len(self.tag_list)):
				self.selectionlist_tags.add_option((self.tag_list[i], i))
				self.selectionlist_tags_settings.add_option((self.tag_list[i], i))
			"""






			studio_data = self.company_dictionnary[studio]

			label = Label(studio)

			self.listview_studiolist.append(MultiListItem(label))




			#HIGHLIGHT TAGGED STUDIOS
			for tag in studio_tags:
				if tag in self.highlight_tag_list:


					label.styles.background = self.user_settings["colorDictionnary"]["HighlightColor"]


			#CHECK FOR COLORS
			if ("CompanyDate" not in studio_data) or (studio_data["CompanyDate"] == None):
				#label.styles.color = self.color_dictionnary[self.color_theme]["notContacted"]
				label.classes = "label_primary"
			else:
				date = self.company_dictionnary[studio]["CompanyDate"]

				if type(date) == str:
					date = pendulum.parse(date).to_date_string()
					date = datetime.strptime(date, "%Y-%m-%d")

				delta = (datetime.now() - date).days
				average_month_day = 365.25 / 12
				delta_month = int(delta / average_month_day)
				delta_week = int(delta / 7)




				alert_data = self.user_settings["alertDictionnary"]
					
				if delta_week < alert_data["RecentContact"]["Delta"]:
					pass

				elif (delta_week >= alert_data["RecentContact"]["Delta"]) and (delta_week < alert_data["LatelyContact"]["Delta"]):
					label.styles.color = self.user_settings["alertDictionnary"]["RecentContact"]["Color"]

				elif (delta_week >= alert_data["LatelyContact"]["Delta"]) and (delta_week < alert_data["PastContact"]["Delta"]):
					label.styles.color = self.user_settings["alertDictionnary"]["LatelyContact"]["Color"]

				else:
					label.styles.color = self.user_settings["alertDictionnary"]["PastContact"]["Color"]

					
				

				

			#app.refresh_css()
		#update the tag list in searchbar
		self.input_tag_lobby.suggester=SuggestFromList(self.tag_list, case_sensitive=False)









	def add_log_line_function(self, log):
		#self.listview_log.append(ListItem(Label(str(log["content"]))))

		label_format = Label("|%s| %s : %s"%(log["severity"].upper(), log["date"], log["content"]))
		self.listview_log.append(MultiListItem(label_format))
		
		#adapt the color of the label using the severity
		if log["severity"] != "MESSAGE":
			label_format.styles.color = self.user_settings["colorDictionnary"][log["severity"]]
















	def generate_markdown_function(self, company_name, company_data):
		markdown = """
# Company name : __%s__

- Company location : %s
"""%(company_name, company_data["CompanyLocation"])


		try:
			if self.letter_verification_function(company_data["CompanyDetails"])==True:
				#try to split the list of elements
				markdown+= "\n# More informations about the company\n"
				details_list = company_data["CompanyDetails"].split("-")

				for detail in details_list:
					if self.letter_verification_function(detail)==True:
						markdown += "- %s\n"%detail
		except:
			pass

		
		if company_data["CompanyAnswer"] not in [True, False, None]:
			markdown += """

> [!WARNING]
> Answer is different : %s
"""%(company_data["CompanyAnswer"])
		
		elif company_data["CompanyAnswer"] == True:
			markdown += """
> [!IMPORTANT]
> The company said Yes
"""
		elif company_data["CompanyAnswer"] == False:
			markdown += """
> [!ERROR]
> The company said No
"""
		else:
			markdown += """
No answer from the company
"""
		


		#CONTACT PART
		markdown += """
Website of the company : [%s](%s)
"""%(company_name, company_data["CompanyWebsite"])


		if "CompanyDate" in company_data:
			markdown += "Last time the studio was contacted : %s\n\n"%company_data["CompanyDate"]
			#get the time difference with today
			today = datetime.now()
			date = company_data["CompanyDate"]

			if date != None:
				if type(date) == str:
					date = pendulum.parse(date).to_date_string()
					date = datetime.strptime(date, "%Y-%m-%d")
				

				delta = (today - date).days
				if delta > 7:
					markdown += "\nIt was %s week(s) ago" % int(delta/7)
				else:
					markdown += "\nIt was %s day(s) ago" % delta

				#self.display_message_function((today - date).days)
			

		markdown += """
## Contact from the company 
"""
		if company_data["CompanyContact"] != {}:
			for contact_type, contact in company_data["CompanyContact"].items():
				
				if contact != {}:
					markdown += "CONTACT - %s\n"%contact_type
					for c_name, c_data in contact.items():
						markdown+="""
%s\n
- mail : %s\n
- website : %s\n
"""%(c_name,c_data["mail"], c_data["website"])
				
		else:
			markdown += """
> [!WARNING]
> No contact from that company!
"""


		

		return markdown


