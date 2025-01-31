import time 
import re
import dns.resolver
import webbrowser
import pendulum
import pyperclip 
import pyfiglet
import unidecode
import re
import os
import Levenshtein

from functools import partial
from typing import  Iterable
from termcolor import *


from textual.suggester import SuggestFromList, Suggester
from textual.app import App, ComposeResult
from textual.widgets import ContentSwitcher, Markdown, MarkdownViewer, DataTable,TextArea, RadioSet, RadioButton, Input, Log, Rule, Collapsible, Checkbox, SelectionList, LoadingIndicator, DataTable, Sparkline, DirectoryTree, Rule, Label, Button, Static, ListView, ListItem, OptionList, Header, SelectionList, Footer, Markdown, TabbedContent, TabPane, Input, DirectoryTree, Select, Tabs
from textual.widgets.option_list import Option, Separator
from textual.widgets.selection_list import Selection
from textual.validation import Function, Number
from textual.screen import Screen, ModalScreen
from textual import events
from textual.containers import ScrollableContainer, Grid, Horizontal, Vertical, Container, VerticalScroll
from textual import on, work

from textual_datepicker import DateSelect, DatePicker

from rich.text import Text 

from datetime import datetime
from pyfiglet import Figlet
from time import sleep

import threading
import json
import colorama




from utils.ConvWidget import MultiListView, MultiListItem
from utils.ConvUser import ConveryUserUtility
from utils.ConvMail import ConveryMailUtility
from utils.ConvUtility import ConveryUtility
from utils.ConvNotif import ConveryNotification
from utils.ConvLinkedin import ConveryLinkedinUtility





# EXTENDED CLASS OF TEXTUAL WITH ADDITIONNAL FEATURES
class ExtendedTextArea(TextArea):
	"""A subclass of TextArea with parenthesis-closing functionality."""

	def _on_key(self, event: events.Key) -> None:
		if event.key == "enter":
			self.insert("\n-")
			#self.move_cursor_relative(columns=-1)
			event.prevent_default()






class ModalConveryScreenUser(ModalScreen, ConveryNotification, ConveryUtility, ConveryUserUtility):


	CSS_PATH = ["styles/layout.tcss"]


	def __init__(self):


		#self.display_message_function(path)


		super().__init__()
	

	def compose(self) -> ComposeResult:

		with VerticalScroll(id="modal_usersettings_vertical_container"):


			self.input_usersettingsjob = Input(placeholder = "What is your job", id="input_usersettingsjob")
			yield self.input_usersettingsjob
		
			self.input_usersettingsskills = Input(placeholder = "What are your skills", id="input_usersettingsskills")
			yield self.input_usersettingsskills

			

			self.textarea_usersettings = ExtendedTextArea(id="textarea_usersettings")
			yield self.textarea_usersettings
			
			

			yield Rule(line_style="double")

			with Horizontal(id="modal_usersettings_horizontal_container"):
				yield Button("Save", variant="primary", id="modal_usersettings_button_save", classes="darken_button primary_button")
				yield Button("Quit", variant="error", id="modal_usersettings_button_quit", classes="darken_button error_button")


	def on_button_pressed(self, event: Button.Pressed) -> None:
		#if event.button.id == "test":
		#	self.display_message_function(self.query("#modal_newcontactname"))

		if event.button.id == "modal_usersettings_button_quit":
			self.app.pop_screen()

		if event.button.id == "modal_usersettings_button_save":
			content = self.textarea_usersettings.text
			splited_content = content.split("-")

			#for line in splited_content:
			#	self.app.display_message_function(line)
			self.app.user_settings["UserPromptDetails"] = splited_content
			if self.letter_verification_function(self.input_usersettingsskills.value) == True:
				self.app.user_settings["UserSkillSearched"] = self.input_usersettingsskills.value.split("/")

			if self.letter_verification_function(self.input_usersettingsjob.value)==True:
				self.app.user_settings["UserJobSearched"] = self.input_usersettingsjob.value

			self.save_user_settings_function()


	def on_mount(self) -> None:
		#apply user settings in the text area
		#self.display_message_function(self.app.user_settings)
		content = self.app.user_settings["UserPromptDetails"]
		
		#self.app.display_message_function(type(content))


		for line in content:
			if self.letter_verification_function(line)==True:
				#self.app.display_message_function("-%s"%line)
				self.textarea_usersettings.insert("-%s"%line)

		try:
			self.input_usersettingsskills.value = "/".join(self.app.user_settings["UserSkillSearched"])
			self.input_usersettingsjob.value = self.app.user_settings["UserJobSearched"]
		except:
			pass














class Modal_Contact(Static):
	

	def __init__(self, kind = "MEMBER", name="", mail="", website=""):

		super().__init__()

		#self.app.display_message_function("%s ; %s ; %s"%(name, mail, website))
		self.kind = kind
		self.contact_name = name 
		self.website = website
		self.mail = mail 



		self.kind_list = ["MEMBER", "JOB", "GENERAL"]
		

		

		#self.app.display_message_function(name)


	def compose(self) -> ComposeResult:
		

		with Horizontal(id="modal_newcontact_container"):
			self.modal_newcontacttype = Select.from_values(self.kind_list, id = "modal_newcontacttype")
			self.modal_newcontactname = Input(placeholder="Name", value = self.contact_name, type="text", id="modal_newcontactname")
			self.modal_newcontactmail = Input(placeholder="Mail", value = self.mail, type="text", id="modal_newcontactmail")
			self.modal_newcontactwebsite = Input(placeholder="Website", value=self.website, type="text", id="modal_newcontactwebsite")

			yield self.modal_newcontacttype
			yield self.modal_newcontactname
			yield self.modal_newcontactmail
			yield self.modal_newcontactwebsite

			self.modal_newcontacttype.value = self.kind










class ModalConveryScreenContact(ModalScreen, ConveryUtility, ConveryUserUtility, ConveryNotification): 




	CSS_PATH = ["Styles/layout.tcss"]

	def __init__(self, mode, studio=None):
		super().__init__()
		self.mode = mode
		self.studio = studio
		self.date = str(datetime.now())
		self.app.display_message_function("%s ; %s"%(mode, studio))

	

	def compose(self) -> ComposeResult:
		self.app.company_dictionnary
		#self.display_message_function = app.display_message_function
		#self.display_error_function = app.display_error_function

		with VerticalScroll(id="modal_createcontact_container"):
			
			self.newcompany_name = Input(placeholder="Company name", type="text", id="modal_newcompanyname")
			self.newcompany_location = Input(placeholder="Company location", type="text", id="modal_newcompanylocation")
			self.newcompany_website = Input(placeholder="Company website", type="text", id="modal_newcompany_website")
			self.newcompany_linkedin = Input(placeholder = "Linkedin account", type="text", id="modal_newcompany_linkedin")
			
			self.newcompany_tags = Input(placeholder="TAGS / KEYWORDS", type="text", id="modal_newcompany_tags", suggester=SuggestFromList(self.app.tag_list, case_sensitive=False))
			

			self.newcompany_details = ExtendedTextArea(id="modal_newcompany_details")
			self.newcompany_details.border_title = "Company details"

			self.newcompany_answer = Select( [("Yes",1), ("No", 2), ("No answer",3), ("Other",4)], id="modal_newcompany_answer")
			self.newcompany_otheranswer = TextArea(id="modal_newcompany_otheranswer", disabled=True)
			self.newcompany_otheranswer.border_title = "Other answer / Details"



			yield self.newcompany_name
			yield self.newcompany_location
			yield self.newcompany_website
			yield self.newcompany_linkedin
			yield self.newcompany_tags
			#yield Button("Last time company was reached", id="modal_newcompany_datebutton")

			self.newcompany_contacted_checkbox = Checkbox("I have already contacted the company", id="modal_contacted_checkbox")
			self.newcompany_contacted_checkbox.value = False
			yield self.newcompany_contacted_checkbox
			with Collapsible(title = "Last time company was reached : ", id="modal_collapsible_dateselector"):
				
				self.modal_dateselect = DateSelect(placeholder="please select",format=str(pendulum.parse(str(datetime.now()))),picker_mount="#modal_collapsible_dateselector",date=pendulum.parse(str(datetime.now())), id="modal_date")
				yield self.modal_dateselect


				   
				
			yield self.newcompany_details
			yield self.newcompany_answer

			
			yield self.newcompany_otheranswer


			with Horizontal(id="modal_addcontact_container"):
				yield Button("Add contact", id="modal_addcontacttolist_button", classes="darken_button primary_button")
				yield Button("Remove contact", id="modal_removecontactfromlist_button", classes="darken_button error_button")
			
			self.newcompany_contactlist_container = ScrollableContainer(id="modal_newcompany_contactlist")
			yield self.newcompany_contactlist_container



			yield Rule(line_style="double")

			with Horizontal(id="modal_horizontal_container"):
				if self.mode == "create":
					yield Button("Create", variant="primary", id="modal_create_contact_button", classes="darken_button primary_button")
				else:
					yield Button("Save", variant="primary", id="modal_create_contact_button", classes="darken_button primary_button")
				yield Button("Quit", variant="error", id="modal_cancel_contact_button", classes="darken_button error_button")




		"""
		if (self.focused.id == "modal_newcompany_tags") and (event.key == "space"):
			self.newcompany_tags.value = "%s; "%self.newcompany_tags.value
		"""
		


	

	def on_mount(self) -> None:
		#IF IN EDIT MODE LOAD THE DICTIONNARY OF THE SELECTED COMPANY
		#AND UPDATE THE PAGE
		if self.mode == "edit":
			self.load_company_data_function(Modal_Contact)

		if self.mode == "create":
			self.query_one("#modal_collapsible_dateselector").disabled = True
			new_contact = Modal_Contact()
			self.newcompany_contactlist_container.mount(new_contact)



	def on_checkbox_changed(self, event: Checkbox.Changed) -> None:
		if event.checkbox.id == "modal_contacted_checkbox":
			self.query_one("#modal_collapsible_dateselector").disabled = not self.newcompany_contacted_checkbox.value



	





	def on_date_picker_selected(self, event: DatePicker.Selected) -> None:
		self.date = event.date
		
		if datetime.strptime(self.date.to_date_string(), "%Y-%m-%d") > datetime.now():
			self.display_error_function("This date is in the futur!")
			return
		widget = self.query_one("#modal_collapsible_dateselector").title = "Last time company was reached : %s"%pendulum.parse(str(self.date))
		#self.display_message_function("UPDATED")


		
			


	def on_button_pressed(self, event: Button.Pressed) -> None:
		#if event.button.id == "test":
		#	self.display_message_function(self.query("#modal_newcontactname"))
	

		if event.button.id == "quit":
			self.app.exit()

		elif event.button.id == "modal_cancel_contact_button":
			self.app.pop_screen()

		elif event.button.id == "modal_newcompany_datebutton":
			date = self.app.push_screen(POST_DateSelector())
			#self.display_message_function(date)

		elif event.button.id == "modal_addcontacttolist_button":
			new_contact = Modal_Contact()
			#self.display_message_function(new_contact)
			self.newcompany_contactlist_container.mount(new_contact)

		elif event.button.id == "modal_removecontactfromlist_button":
			#get children 
			children_list = self.query("Modal_Contact")
			#self.display_message_function(children_list)
			if children_list:
				children_list.last().remove()

		elif event.button.id == "modal_create_contact_button":
			self.add_company_function()


	
	def on_select_changed(self, event: Select.Changed) -> None:
		if event.select.id == "modal_newcompany_answer":
			value = self.query_one("#modal_newcompany_answer").value

			if value == 4:
				self.newcompany_otheranswer.disabled=False
			else:
				self.newcompany_otheranswer.disabled=True












class SuggestFromList(Suggester):



	def __init__(self, suggestions= Iterable[str], *, case_sensitive: bool=True) -> None:
		super().__init__(case_sensitive=case_sensitive)

		self._suggestions = list(suggestions)
		self._for_comparison = (
			self._suggestions
			if self.case_sensitive
			else [suggestion.casefold() for suggestion in self._suggestions]
		)


	async def get_suggestion(self, value: str) -> str | None:
		"""Gets a completion from the given possibilities.

		Args:
			value: The current value.

		Returns:
			A valid completion suggestion or `None`.
		"""

		#get the word to check and suggestion
		first_values = value.split(";")
		del first_values[-1]
		last_value = value.split(";")[-1]

		for idx, suggestion in enumerate(self._for_comparison):
			if suggestion.startswith(last_value):
				if len(first_values) != 0:
					return "%s;%s"%(";".join(first_values),self._suggestions[idx])
				else:
					return self._suggestions[idx]

		"""
		for idx, suggestion in enumerate(self._for_comparison):
			#self.display_message_function(idx)
			if suggestion.startswith(value):
				return self._suggestions[idx]
		return None
		"""
















class ModalConveryScreenLinkedin(ModalScreen, ConveryLinkedinUtility, ConveryNotification, ConveryUserUtility):
	CSS_PATH = ["Styles/layout.tcss"]

	def __init__(self):

		#self.driver = None 
		self.linkedin_studiolist = {}
		self.member_list = {}
		self.studio_name = self.app.list_studiolist_display[self.app.listview_studiolist.index]
		super().__init__()


	def compose(self) -> ComposeResult:
		with VerticalScroll(id="modal_linkedin_container"):
			with ContentSwitcher(id = "modal_linkedin_content_switcher", initial="modal_get_linkedin_container"):

				with Vertical(id = "modal_get_contact_container"):
					yield Label("Linkedin Member")
					self.listview_linkedin_member = MultiListView(id = "modal_list_linkedin_contact")
					yield self.listview_linkedin_member
					#self.selectionlist_linkedin_member = SelectionList(id="modal_list_linkedin_member")
					#yield self.selectionlist_linkedin_member

					yield Button("ADD LINKEDIN CONTACT", id = "modal_button_add_linkedin_contact")


				with Vertical(id = "modal_get_linkedin_container"):
					yield Label("Linkedin Studio")
					self.listview_linkedin_account = ListView(id="modal_list_linkedin_studio")

					yield self.listview_linkedin_account

					yield Button("Validate Linkedin Account", id="modal_button_linkedin_account")
					

				


			yield Button("Quit", id = "modal_getcontact_quit", classes="error_button")



	def on_mount(self) -> None:
		#get studio selection
		
		#self.display_message_function(studio_name)

	

		studio_data = self.app.company_dictionnary[self.studio_name]

		#self.display_message_function("EXECUTE")

		
		#GET THE LINKEDIN CONTACT
		if (type(studio_data["CompanyLinkedin"]) == str) and (self.letter_verification_function(studio_data["CompanyLinkedin"]) == True):
			self.display_success_function("Linkedin account detected")
			self.query_one("#modal_linkedin_content_switcher").current = "modal_get_contact_container"


			self.search_for_user_function(studio_data["CompanyLinkedin"])
				

		#GET A LIST OF LINKEDIN ACCOUNT MATCHING WITH THE STUDIO NAME?
		else:
			self.display_warning_function("Impossible to detect linkedin account for this studio")
			self.display_message_function("Trying to find linkedin studio accounts")
			#CREATE A DRIVER
			self.display_message_function(self.studio_name)
			with self.app.suspend():
				self.linkedin_studiolist = self.linkedin_get_studiolist_function(self.studio_name)

			if type(self.linkedin_studiolist) != dict:
				self.display_error_function("Impossible to find matching studio on linkedin!")
				return
			else:
				#clean selection list
				#self.optionlist_linkedin_contact.clear_options()
				#add new options
				#self.optionlist_linkedin_contact.add_options(list(linkedin_studiolist.keys()))

				self.listview_linkedin_account.clear()
				for key, value in self.linkedin_studiolist.items():
					self.listview_linkedin_account.append(ListItem(Label("%s | %s"%(key, value))))





	def on_key(self, event:events.Key) -> None:
		if (event.key == "enter") and (self.focused.id == "modal_list_linkedin_contact"):
			children_item = self.listview_linkedin_member.children[self.listview_linkedin_member.index]
			children_item.highlight_item(children_item)




			


		
				





	def on_button_pressed(self, event: Button.Pressed) -> None:
		if event.button.id == "modal_getcontact_quit":
			self.app.pop_screen()

		if event.button.id == "modal_button_linkedin_account":
			#get the name of the studio selected and update the linkedin profile in company data
			try:
				#studio_name = self.app.list_studiolist_display[self.app.listview_studiolist.index]

				#get the index
				index = self.listview_linkedin_account.index
				account_name_selected = list(self.linkedin_studiolist.keys())[index]
				account_link_selected = (self.linkedin_studiolist[account_name_selected])

				#update the dictionnary
				studio_data = self.app.company_dictionnary[self.studio_name]
				studio_data["CompanyLinkedin"] = account_link_selected
				self.app.company_dictionnary[self.studio_name] = studio_data

				#save the dictionnary
				self.app.save_company_dictionnary_function()
				self.app.update_informations_function()


				#call the get linkedin user function
				self.search_for_user_function(account_link_selected)

				
			except Exception as e:
				self.display_error_function(str(e))
			else:
				self.display_success_function("Linkedin account updated in Company Data")


		if event.button.id == "modal_button_add_linkedin_contact":
			#create the new member dictionnary
			new_member_dictionnary = {}
			#get the current studio selected
			#studio_name = self.app.list_studiolist_display[self.app.listview_studiolist.index]

			for index in self.listview_linkedin_member.index_list:
				#get contact data for this index
				member_name = list(self.member_list.keys())[index]
				member_data = self.member_list[list(self.member_list.keys())[index]]

				if member_data["mail"] == None:
					member_data["mail"] = ""

				new_member_dictionnary[member_name] = {
					"mail":member_data["mail"],
					"website":member_data["link"]
				}

			#get data about this studio
			studio_data = self.app.company_dictionnary[self.studio_name]
			#get contact data
			studio_contact_data = studio_data["CompanyContact"]
			studio_member_data = studio_contact_data["MEMBER"]
			studio_member_data.update(new_member_dictionnary)

			#rebuild the dictionnary
			studio_contact_data["MEMBER"] = studio_member_data
			studio_data["CompanyContact"] = studio_contact_data
			self.app.company_dictionnary[self.studio_name] = studio_data

			#save the new company dictionnary
			self.app.save_company_dictionnary_function()
			self.app.update_informations_function()

			self.display_success_function("New contact informations updated")






	def search_for_user_function(self, studio_account):
		self.member_list.clear()
		with self.app.suspend():
			self.member_list = self.get_linkedin_user_function(self.studio_name, studio_account)
			
		
		if type(self.member_list) == dict:
			#change display
			self.query_one("#modal_linkedin_content_switcher").current = "modal_get_contact_container"

			#clean the selectionlist
			#self.selectionlist_linkedin_member.clear_options()
			self.listview_linkedin_member.clear()
			
			selection_item_list = []
			i=0
			for member_name, member_data in self.member_list.items():
				#selection_item_list.append(("%s : %s\n%s"%(member_name, member_data["position"], member_data["link"]),i))
				label = Label("\n%s : %s\n%s\n%s"%(member_name, member_data["position"], member_data["link"], str(member_data["mail"])))
				self.listview_linkedin_member.append(MultiListItem(label))
				i+=1

			#self.listview_linkedin_member.extend(selection_item_list)
			#self.selectionlist_linkedin_member.add_options(selection_item_list)

			
			
			





