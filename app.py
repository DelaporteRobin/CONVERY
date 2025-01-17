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
from textual.reactive import reactive
from textual.await_complete import AwaitComplete



from utils.ConvGuiUtility import ConveryGUIUtils
from utils.ConvNotif import ConveryNotification
from utils.ConvUtility import ConveryUtility
from utils.ConvMail import ConveryMailUtility


#import theme file
from styles.theme_file import *


from config import STYLES_PATH, ASCII_FONT, THEME


#import modal screens
from modal import ModalConveryScreenUser
from modal import ModalConveryScreenContact
from modal import ModalConveryScreenLinkedin

from utils.ConvWidget import MultiListView, MultiListItem







#prerequired element to launch the program (variables)
#mail api key is modified in the settings by the user
#copilot need a variable defined with the key
#linkedin cookies needs to be stored in a file











class ConveryApp(App, ConveryGUIUtils, ConveryUtility, ConveryNotification, ConveryMailUtility):
	CSS_PATH = ["styles/layout.tcss"]


	def __init__(self):
		super().__init__()
		#load main argument of the app

		self.company_dictionnary = {}
		self.contact_list = {}


		self.program_log = []
		self.old_log = []

		self.studio_suggest_list = []
		self.mail_contact_list = {}


		self.kind_list = ["MEMBER", "JOB", "GENERAL"]
		self.tag_list = []

		self.highlight_tag_list = []
		self.highlight_studio_list = []


		self.not_contacted_list = []
		self.no_alert_list = []
		self.short_alert_list = []
		self.medium_alert_list = []
		self.long_alert_list = []




		#self.user_preset = {}

		self.list_studiolist_display = []

		self.font_title = ASCII_FONT

		self.color_theme = THEME



		#create an empty user settings dictionnary in case it is impossible to load
		#the user settings file
		self.user_settings = {
			"colorTheme":"DarkTheme",
			"companyDisplayMode":1,
			"colorDictionnary": {
				"HighlightColor": "#6d76ba",
				"ERROR": "#ff3a3a",
				"SUCCESS": "#6fcc5c",
			},
			"alertDictionnary": {
				"RecentContact": {
					"Color": "#fff03a",
					"Delta": 3,
				},
				"LatelyContact": {
					"Color": "#ff7c3a",
					"Delta": 5,
				},
				"PastContact": {
					"Color": "#ff3a3a",
					"Delta": 7,
				},
				"NotContacted": {
					"Color":"#ffffff"
				},
			
			},
			"UserPromptDetails":[],
			"UserSkillSearched":[],
			"UserJobSearched":"",
			"UserMailAddress":"archive-user-test@maildomain.com",
			"UserMailAttached":"c:/users/username/folder1/folder2/user_resume.pdf",
			"UserMailKey":"xxxx xxxx xxxx xxxx",
			"UserDemoReelLink":"https://youtube.com/DemoReelLink",
			"UserDemoReelPassword":None,
			"UserLinkedinAddress":None,
			"UserLinkedinPassword":None,
			"UserTagList":[],
			"UsermailPreset": {}
		}



		#temporary color dictionnary
		self.color_dictionnary = {
			"Dark_Theme": {
				"NotContacted": "white",
				"RecentContact": "#e59818",
				"LatelyContact": "#e55a1a",
				"PastContact": "#d81b57",
			}
		}



		print("hello world")














	#MAIN INTERFACE BUILD
	def compose(self) -> ComposeResult:

		yield Header(show_clock=True)
		


		with Horizontal(id="main_horizontal_container"):
			#with Vertical(id = "main_title_container"):

				


				#with Horizontal(id = "main_left_center_container_horizontal"):
			with Vertical(id = "main_left_container"):
				yield Label(pyfiglet.figlet_format("convery",font=self.font_title, width=200), id="label_title")
				
				

				with Vertical(id="left_vertical_container"):

					
					with Grid(id = "left_horizontal_option_bar"):
		
						
						yield Button("USER INFOS", id="button_userinfos", classes="button_bar")
						yield Button("ADD CONTACT", id="button_addcontact", classes="button_bar")
						yield Button("EDIT CONTACT", id="button_editcontact", classes="button_bar")
						yield Button("DELETE CONTACT", id="button_deletecontact", variant="error", classes="error_button button_bar")
						

					

				



					self.input_studiolist_searchbar = Input(placeholder = "Studio name...", id = "input_studiolist_searchbar")
					yield self.input_studiolist_searchbar

					self.listview_studiolist = MultiListView(id="listview_studiolist")
					self.listview_studiolist.border_title = "Studio list"
					yield self.listview_studiolist

				with Horizontal(id="left_bottom_container"):
					yield Button("Get contact from studio", id="button_get_contact_from_studios")
					yield Button("Save contact sheet", id="button_save_contact_sheet")
				#self.datatable_studiolist = DataTable(id = "datatable_studiolist")
				#yield self.datatable_studiolist



			
			with VerticalScroll(id="main_center_container"):
				with Collapsible(id = "collapsible_studiolist_settings", title="COMPANY LIST SETTINGS"):
					with ScrollableContainer(id = "scrollable_studiolist_settings"):
						
						with RadioSet(id = r"adioset_studiolist_settings"):
							yield RadioButton("By alphabetic order")
							yield RadioButton("By chronologic order")
							yield RadioButton("By priority order")

						yield Rule(line_style="double")

						with Horizontal(id = "horizontal_create_tag_container"):
							self.input_create_tag = Input(placeholder = "Tag name", id="input_create_tag")
							yield self.input_create_tag 

							yield Button("Create tag", id="button_create_tag", classes="error_button")

						self.selectionlist_tags_settings = SelectionList(id = "selectionlist_tags_settings")
						yield self.selectionlist_tags_settings

						with Horizontal(id = "horizontal_tag_container"):
							#yield Button("Remove tags", id="button_remove_tag")
							yield Button("Highlight", id="button_highlight_tag")
							yield Button("Add to selection", id = "button_add_tag_to_selection")
							yield Button("REMOVE", id="button_remove_tag", classes="error_button")

				self.input_tag_lobby = Input(placeholder="TAG LIST", id="input_tag_lobby", suggester=SuggestFromList(self.tag_list, case_sensitive=False))
				yield self.input_tag_lobby 

				#with Horizontal(id = "right_horizontal_container"):
				with Vertical(id="right_vertical_container1"):
					self.markdown_studio = Markdown("Hello World", id="markdown_lobby")
					yield self.markdown_studio


			with Vertical(id = "main_right_container"):
				with TabbedContent(id="main_righttab_container"):

					with TabPane("Log"):
						#self.listview_log = ListView(id="listview_log")
						self.listview_log = MultiListView(id = "listview_log")
						yield self.listview_log
						#self.log_mainpage = Log(id="log_mainpage")
						#yield self.log_mainpage


					with TabPane("Mail editor"):
						with Horizontal(id="main_righthorizontal_container"):
							with Vertical(id="right_mailpreset_container"):
								self.input_presetname = Input(placeholder="Mail preset name", id="input_presetname")
								yield self.input_presetname
								yield Button("Create preset", id="button_createpreset", classes="button_preset")
								yield Button("Save preset", id="button_savepreset", classes="button_preset")
								yield Button("Delete preset", id="button_deletepreset", classes="button_preset")
								yield Button("Use copilot", id="button_usecopilot", classes="primary_button button_preset")

								yield Rule()

								yield Button("Copy content", id="button_copycontent", classes="button_preset")

								self.listview_mailpreset = ListView(id="listview_mailpreset")
								yield self.listview_mailpreset
								self.listview_mailpreset.border_title = "Preset list"
							
							with Vertical(id="right_mailtext_container"):
								
								


								with Collapsible(title="Contact list", id="collapsible_mail_contact_list"):
							


									with ScrollableContainer(id = "scrollable_mail_contact_list"):

										self.input_mailcontact = Input(placeholder="Mail contact list", id="input_mailcontact", suggester=SuggestFromList(self.studio_suggest_list, case_sensitive=False))
										yield self.input_mailcontact

										with Horizontal(id = "mail_contact_horizontal_container"):
											with Vertical(id = "mail_contact_left_column"):
												self.selectionlist_contacttype = SelectionList(id = "selectionlist_contacttype")
												self.selectionlist_tags = SelectionList(id = "selectionlist_tags")
												self.selectionlist_delta = SelectionList(id = "selectionlist_delta")

										
												yield self.selectionlist_contacttype
												yield self.selectionlist_delta
												yield self.selectionlist_tags

										

												yield Button("LOAD CONTACT", id = "button_filter_add_contact")
												yield Button("Add selected studio", id="button_add_contact_from_studio")
												yield Button("Remove studio with selected tag", id = "button_remove_studio_with_tag")
												yield Button("CLEAR CONTACT", id = "button_clear_contact", classes="error_button")


											with Vertical(id = "mail_contact_right_column"):
												self.optionlist_contact = OptionList(id = "optionlist_contact")
												self.optionlist_contact.border_title = "Mail contact list"
												yield self.optionlist_contact
				


								yield Rule()

								

								self.input_mail_header = Input(placeholder="Mail header", id="input_mail_header")
								self.textarea_mail = TextArea(id="textarea_mail")

								yield self.input_mail_header
								yield self.textarea_mail
								self.textarea_mail.border_title = "Mail"

								with Horizontal(id="mail_action_horizontal_container"):
									yield Button("SEND MAIL", id="button_send_mail", classes="error_button")



					



					with TabPane("User Settings"):
						with Vertical(id = "main_settings_container"):
							with Collapsible(title="Copilot settings", id="right_mailprompt_collapsible"):
								self.textarea_prompt = TextArea(id="textarea_prompt")
								yield self.textarea_prompt
								self.textarea_prompt.border_title = "Copilot prompt"



								with Horizontal(id="right_mailtext_horizontal"):
									yield Button("Save copilot prompt", id="button_saveprompt")

							yield Rule()


							yield Label("Mail settings")
							self.input_mailkey = Input(placeholder="Mail key", id="input_mail_key")
							self.input_useraddress = Input(placeholder="User email address", id = "input_useraddress")
							self.input_demolink = Input(placeholder="DemoReel link", id = "input_demolink")
							self.input_demopassword = Input(placeholder = "DemoReel password", id="input_demopassword")
							self.input_resume = Input(placeholder="Resume filepath", id="input_resume")

							yield self.input_mailkey
							yield self.input_useraddress
							yield self.input_demolink
							yield self.input_resume


							yield Rule()

							yield Label("Linkedin Settings")
							self.input_linkedin_username = Input(placeholder = "Linkedin Email", id="input_linkedin_username")
							self.input_linkedin_password = Input(placeholder = "Linkedin Password", id="input_linkedin_password")
							yield self.input_linkedin_username
							yield self.input_linkedin_password




					with TabPane("Mail watcher"):
						self.listview_contactlist = ListView(id = "listview_contactlist")
						yield self.listview_contactlist













	def on_mount(self) -> None:
		#register and apply all theme in theme python file
		for theme in theme_registry:
			self.register_theme(theme)
		#apply the theme specified in config file
		self.theme = THEME



		self.display_message_function("update")
		
		for i in range(len(self.user_settings["alertDictionnary"])):
			self.selectionlist_delta.add_option(( list(self.user_settings["alertDictionnary"].keys())[i], i))

		for i in range(len(self.kind_list)):
			self.selectionlist_contacttype.add_option((self.kind_list[i], i))


		#launch log reading thread
		#self.listen_thread = threading.Thread(target=self.read_log_function, args=(), daemon=True)
		#self.listen_thread.start()
		#self.read_log_function()

		#self.program_log.append("hello world")

		
		self.update_informations_function()
		





	"""
	def read_log_function(self):
		while True:
			#self.program_log.append("hello world")
			if self.program_log != self.old_log:
				self.notify("detected changes", timeout=2)
				try:
					self.call_from_thread(self.add_logline_function)
				except Exception as e:
					pass
				else:

					#update the old log dictionnary
					self.old_log = copy.copy(self.program_log)
			sleep(2)



	def add_logline_function(self):
		#get the last item of the log and get the seveity of it
		#format the message
		#depending of the severity of the log item change the color
		try:
			log_item = self.program_log[-1]

			log_format = "[ %s ] - %s - %s"%(log_item["severity"], log_item["date"], log_item["content"])
			label = Label(log_format)
			self.listview_log.append(ListItem(label))
			self.notify(log_item["severity"], timeout=2)
			if log_item["severity"] == "SUCCESS":
				label.styles.color = self.user_settings["colorDictionnary"]["SuccessColor"]
			elif log_item["severity"] == "ERROR":
				label.styles.color = self.user_settings["colorDictionnary"]["ErrorColor"]
			else:
				label.styles.color = "white"


		except Exception as e:
			self.notify(str(e), timeout=3)
	"""







	def on_input_changed(self, event: Input.Changed) -> None:
		#EVENT FOR THE SEARCHBAR
		#call the searchbar system function
		if event.input.id == "input_studiolist_searchbar":
			#get the value of the searchbar at that moment
			#self.display_message_function(self.input_studiolist_searchbar.value)
			self.searchbar_function(self.input_studiolist_searchbar.value)


	def on_input_submitted(self, event: Input.Submitted) -> None:


		if event.input.id in ["input_useraddress", "input_mailkey", "input_demolink", "input_demopassword", "input_resume"]:
			#get all informations in fields
			#check all informations
			
			#self.notify("hello world",severity="error",timeout = 3)
			#self.display_error_function("NOTIFICATION")
			
			self.check_user_informations_function()
			self.save_user_settings_function()

			self.display_success_function("Informations saved!")


		if event.input.id == "input_tag_lobby":
			#get the studio selected
			#get the list of tags

			#replace the studio tags in dictionnary
			#call the update function
			studio_name = list(self.company_dictionnary.keys())[self.listview_studiolist.index]
			studio_data = self.company_dictionnary[list(self.company_dictionnary.keys())[self.listview_studiolist.index]]

			tag_list = (self.input_tag_lobby.value).lower().split(";")
			studio_data["CompanyTags"] = tag_list

			self.company_dictionnary[studio_name] = studio_data 
			self.save_company_dictionnary_function()
			self.update_informations_function()




		if event.input.id == "input_mailcontact":
			#get the value of the input field
			#check if the name is in the studio list
			#otherwise check if it is an email addres
			if self.letter_verification_function(self.input_mailcontact.value)!=True:
				self.display_error_function("You have to enter a studio name or email addres!")
				return
			else:

				contact_list = {}

				contacttype_index_list = (self.selectionlist_contacttype.selected)
				contacttype_list = []

				for index in contacttype_index_list:
					contacttype_list.append(self.kind_list[index])

				self.display_message_function(contacttype_list)
				"""
				if self.input_mailcontact.value not in list(self.company_dictionnary.keys()):
					if (self.check_addres_function(self.input_mailcontact.value)) != True:
						self.display_error_function("This is not a valid studio name or email addres!")
						return 
				
				if self.input_mailcontact.value in list(self.mail_contact_list).keys():
					self.display_error_function("Contact already in list!")
					return 

				self.mail_contact_list.append(self.input_mailcontact.value)
				self.optionlist_contact.add_option(self.input_mailcontact.value)
				self.display_message_function("Contact added to list")
				"""

				#CHECK THE CATEGORY OF CONTACT SELECTED
				#GET THE LIST OF CONTACT FOR THIS STUDIO ANND ADD ONLY CONTACT THAT ARE MATCHING
				
				#check if it is a studio
				if self.input_mailcontact.value in list(self.company_dictionnary.keys()):
					studio_contact_data = self.company_dictionnary[self.input_mailcontact.value]["CompanyContact"]

					
					for contact_type, contact_data in studio_contact_data.items():
						
						
						if len(contacttype_list) > 0:
							#self.display_message_function("CHECKER HUH")
							for c_name, c_data in contact_data.items():
								if self.letter_verification_function(c_data["mail"])==True:
									if contact_type in contacttype_list:
										contact_list["[%s] %s"%(self.input_mailcontact.value, c_data["mail"])] = {
											"studioName":self.input_mailcontact.value,
											"contactName":c_name,
											"contactMail":c_data["mail"]
										}
						else:
							for c_name, c_data in contact_data.items():
								if self.letter_verification_function(c_data["mail"])==True:
									contact_list["[%s] %s"%(self.input_mailcontact.value, c_data["mail"])] = {
										"studioName":self.input_mailcontact.value,
										"contactName":c_name,
										"contactMail":c_data["mail"]
									}
				#check if it is an email addres
				elif self.check_address_function(self.input_mailcontact.value)==True:
					contact_list[self.input_mailcontact.value] = {
						"studioName":None,
						"contactMail":self.input_mailcontact.value
					}
				else:
					self.display_error_function("Contact isn't a valid studio name or email addres!")
					return




	

				
				self.mail_contact_list.update(contact_list)

				self.optionlist_contact.clear_options()
				self.optionlist_contact.add_options(list(self.mail_contact_list.keys()))









	def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
		if event.option_list.id == "optionlist_contact":
			
			#get the index of the selected item
			#remove it from the list
			#refresh the option list
			index = (self.optionlist_contact.highlighted)
			key = list(self.mail_contact_list.keys())[index]

			self.mail_contact_list.pop(key, None)

			self.optionlist_contact.clear_options()
			self.optionlist_contact.add_options(self.mail_contact_list)


						





			
	def on_key(self, event:events.Key) -> None:
		if (event.key == "enter") and (self.focused.id == "listview_studiolist"):
			children_item = self.listview_studiolist.children[self.listview_studiolist.index]
			children_item.highlight_item(children_item)

			#self.display_message_function(self.listview_studiolist.index_list)


	def on_radio_set_changed(self, event:RadioSet.Changed) -> None:
		if event.radio_set.id == "radioset_studiolist_settings":
			#get index
			index = event.index
			self.user_settings["companyDisplayMode"] = index
			self.save_user_settings_function()
			self.update_informations_function()


	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "button_remove_studio_with_tag":
			self.remove_studio_with_tag_function()

		if event.button.id == "button_add_contact_from_studio":
			self.get_contact_from_filter_function(True)

		if event.button.id == "button_create_tag":
			#create a tag from the lobby
			#and add it to the list of tag create
			#needs to store this list somewhere???
			value = self.create_tag_function()
			if value == True:
				self.update_informations_function()

		if event.button.id == "button_add_tag_to_selection":
			self.add_tag_to_selection_function()


		if event.button.id == "button_get_contact_from_studios":
			#self.push_screen(POST_GetContact())
			self.push_screen(ModalConveryScreenLinkedin())

		if event.button.id == "button_highlight_tag":
			self.highlight_tag_list.clear()
			index_list = self.selectionlist_tags_settings.selected
			tag_list = []
			for index in index_list:
				self.highlight_tag_list.append(self.user_settings["UserTagList"][index])

			self.update_informations_function()


		if event.button.id == "button_save_contact_sheet":
			#self.save_contact_sheet_function()
			
			self.save_contact_table_function()

		if event.button.id == "button_erase_tag":
			self.highlight_tag_list.clear()

			self.delete_tag_function()
			self.update_informations_function()




		if event.button.id == "button_remove_tag":
			#get the selection in selection list
			index_list = self.selectionlist_tags_settings.selected
			tag_list = []

			self.display_message_function(index_list)
			self.display_message_function(self.tag_list)
			for index in index_list:
				try:
					#self.display_message_function(self.tag_list[index])
					#tag_list.append(self.tag_list[index])
					tag_list.append(self.user_settings["UserTagList"][index])
				except Exception as e:
					self.display_error_function(traceback.format_exc())
					pass

			for studio_name, studio_data in self.company_dictionnary.items():
				studio_tag = studio_data["CompanyTags"]
				for tag in tag_list:
					try:
						studio_tag.remove(tag)
					except ValueError:
						pass

				studio_data["CompanyTags"] = studio_tag 

				self.company_dictionnary[studio_name] = studio_data

			#update user settings
			user_tag_list = self.user_settings["UserTagList"]
			for tag in tag_list:
				user_tag_list.remove(tag)
			self.user_settings["UserTagList"] = user_tag_list

			self.save_user_settings_function()
			self.save_company_dictionnary_function()
			self.update_informations_function()
			

		if event.button.id == "button_send_mail":

			with self.suspend():
				self.send_mail_function()

			#save user settings
			self.save_company_dictionnary_function()
			#refresh informations
			self.update_informations_function()

			

		if event.button.id == "button_filter_add_contact":
			self.get_contact_from_filter_function()


		if event.button.id == "button_createpreset":
			self.create_mail_preset_function()


		if event.button.id == "button_saveprompt":
			content = self.textarea_prompt.text 
			#self.display_message_function(content)

			
			self.user_preset["CopilotPrompt"] = content

			self.save_mail_preset_function()


		if event.button.id == "button_usecopilot":
			#self.display_message_function(self.company)
			generate = self.generate_with_copilot_function()

		if event.button.id == "button_deletepreset":
			index = self.listview_mailpreset.index
			
			try:
				preset_dictionnary = self.user_settings["UserMailPreset"]
				preset_list = list(preset_dictionnary.keys())
				preset_dictionnary.pop(preset_list[index])
				self.user_settings["UserMailPreset"] = preset_dictionnary
			except Exception as e:
				self.display_error_function("Impossible to remove from dictionnary!\n%s"%e)
				return
			else:
				pass

			self.save_user_settings_function()

			self.listview_mailpreset.remove_items([index])


		if event.button.id == "button_copycontent":
			if self.letter_verification_function(self.textarea_mail.selected_text)==True:
				pyperclip.copy(self.textarea_mail.selected_text)
			else:
				pyperclip.copy(self.textarea_mail.text)
			self.display_success_function("Content copied")
			


		if event.button.id == "button_addcontact":
			
			#self.display_message_function(value)
			#self.push_screen(POST_AddContact("create"))
			self.push_screen(ModalConveryScreenContact("create"))


		if event.button.id == "button_userinfos":
			#self.display_message_function("pushing screen")
			self.push_screen(ModalConveryScreenUser())

		if event.button.id == "button_deletecontact":
			

			self.delete_company_function()



		if event.button.id == "button_savepreset":
			#get the content of the list selection
			#get the content of the text
			#replace in the dictionnary and save the new dictionnary
			index = self.listview_mailpreset.index
			preset_list = self.user_settings["UserMailPreset"]
			preset_name = list(preset_list.keys())[index]

			new_preset_content = self.textarea_mail.text 
			new_preset_header = self.input_mail_header.value

			preset_list[preset_name] = {
				"HEADER": new_preset_header,
				"CONTENT": new_preset_content,
				}
			self.user_settings["UserMailPreset"]
			#self.save_mail_preset_function()
			self.save_user_settings_function()
			self.update_informations_function()



		if event.button.id == "button_editcontact":

			#studio = list(self.company_dictionnary.keys())[self.query_one("#datatable_studiolist").cursor_coordinate[1]]
			#value = self.company_dictionnary[list(self.company_dictionnary.keys())[(self.query_one("#datatable_studiolist").cursor_coordinate[1])]]
			#get the selection

			try:
				#studio = list(self.company_dictionnary.keys())[self.listview_studiolist.index]
				studio = self.list_studiolist_display[self.listview_studiolist.index]

				self.push_screen(ModalConveryScreenContact("edit", studio))
			except TypeError:
				self.display_error_function("No studio selected")
				
			#self.update_informations_function()






















	def on_markdown_link_clicked(self, event: Markdown.LinkClicked) -> None:
		link = event.href

		#check if email or internet addres
		
		#email_regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
		#url_regex = r'^(https?://)?(www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(/.*)?$'
		


		#remove the beginning of the link copied if it starts with mailto:
		if link.startswith("mailto:"):
			link = link.replace("mailto:", "")

		pyperclip.copy(link)
		self.display_success_function("Link copied in clipboard\n%s"%link)


		
		"""

		#test the dns check
		if re.match(url_regex, link):
			#self.display_message_function("website addres")
			#open the link in a webbrower
			
			#OPEN THE WEBBROWSER WITH THE LINK
			#webbrowser.open(link)

			#COPY THE LINK IN THE CLIPBOARD
			pyperclip.copy(link)
			self.display_message_function("Link copied in clipboard\n%s"%link)
		else:
			try:
				domain = link.split("@")[1]
				dns.resolver.resolve(domain, "MX")
			except Exception as e:
				self.display_error_function("Link not recognized\n%s"%e)
			else:
				self.display_message_function("Email addres")
		"""

		



	def on_list_view_selected(self, event: ListView.Selected) -> None:
		if event.list_view.id == "listview_studiolist":
			#check the content in the selection by getting the studio name
			index = self.listview_studiolist.index
			#get the content of the dictionnary
			#and fill the markdown viewer with the company informations
			
			#company_name = list(self.company_dictionnary.keys())[index]
			company_name = self.list_studiolist_display[index]
			company_data = self.company_dictionnary[company_name]
			
			markdown = self.generate_markdown_function(company_name, company_data)

			self.markdown_studio.update(markdown)


			#load the content of tag list for this studio
			tag_list = ";".join(company_data["CompanyTags"])
			self.input_tag_lobby.value = tag_list


		if event.list_view.id == "listview_mailpreset":

			#clear the content of the text area
			#and fill it with the content of that mail preset if possible
			index = self.listview_mailpreset.index
			preset_name = list(self.user_settings["UserMailPreset"].keys())[index]
			preset_header = self.user_settings["UserMailPreset"][preset_name]["HEADER"]
			preset_content = self.user_settings["UserMailPreset"][preset_name]["CONTENT"]

			

			#self.display_message_function(preset_name)
			#self.display_message_function(self.user_preset["mailPreset"])
			try:
				self.input_mail_header.value = str(preset_header)
				self.textarea_mail.clear()
				self.textarea_mail.insert(self.user_settings["UserMailPreset"][preset_name]["CONTENT"],(0,0))
			except Exception as e:
				self.display_error_function("Impossible to display mail preset content : %s"%e)
				self.display_error_function(traceback.format_exc())
				pass








	def searchbar_function(self, content):

		if self.letter_verification_function(content) == True:
			#remove all capital letter and accent in the content
			content = unidecode.unidecode(content.lower())
			#self.display_message_function(content)



			self.list_studiolist_display = []



			for i in range(len(self.list_studiolist_filtered)):

				studio_name = self.list_studiolist[i]
				studio_filtered = self.list_studiolist_filtered[i]


				if content in studio_filtered:
					self.list_studiolist_display.append(studio_name)
				else:
					distance = Levenshtein.distance(content, studio_filtered)
					length = max(len(content), len(studio_filtered))
					similitude = ((length - distance) / length) * 100

					if similitude > 70:
						self.list_studiolist_display.append(studio_name)


			#self.list_studiolist_display = self.searchbar_studio_list
			self.listview_studiolist.clear()
			self.update_studiolist_view()




		else:
			#append to the studiolist the studiolist
			self.update_informations_function()































#check if admin function
def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False



if __name__ == "__main__":
	#check if the program is launched as admin
	if is_admin():
		print("Admin rights checked")
		app = ConveryApp()
		app.run()
	else:
		print("Asking for admin rights...")

		ctypes.windll.shell32.ShellExecuteW(
			None, "runas", sys.executable, " ".join(sys.argv), None, 1
		)
