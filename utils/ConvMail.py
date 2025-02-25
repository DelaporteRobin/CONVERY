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
from termcolor import *

import smtplib
import requests

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders




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



#init colorama
colorama.init()











class ConveryMailUtility():

	def create_mail_preset_function(self):
		#get the content in the field
		preset_name = self.input_presetname.value
		preset_content = self.textarea_mail.text
		#get the content for the header
		preset_header = self.input_mail_header.value

		if "UserMailPreset" not in self.user_settings:
			self.user_settings["UserMailPreset"] = {}
			self.save_user_settings_function()
			return

		if (self.letter_verification_function(preset_name) == False) or (self.letter_verification_function(preset_content)==False) or (self.letter_verification_function(preset_header)==False):
			self.display_error_function("You have to enter a name, a header, and a valid content for the mail preset")
			return



		#check if the preset is not already registered in the dictionnary
		
		
		if preset_name not in list(self.user_settings["UserMailPreset"].keys()):
			#self.user_preset[preset_name] = preset_content
			preset_list = self.user_settings["UserMailPreset"]
			preset_list[preset_name] = {
				"HEADER":preset_header,
				"CONTENT":preset_content
				}
			self.user_settings["UserMailPreset"] = preset_list
			self.save_mail_preset_function()
			self.update_informations_function()
		else:
			self.display_error_function("A preset with the same name is already registered")



	def load_mail_preset_function(self):
		try:
			with open(os.path.join(os.getcwd(), "data/user/UserSettings.json"), "r") as read_file:
				self.user_settings = json.load(read_file)
		except Exception as e:
			self.display_error_function("Impossible to load mail presets\n%s"%e)
		else:
			#self.display_message_function("Presets loaded")
			#self.display_message_function(self.user_preset)
			pass


	def save_mail_preset_function(self):
		os.makedirs(os.path.join(os.getcwd(), "data/user"), exist_ok=True)
		try:
			with open(os.path.join(os.getcwd(), "data/user/UserSettings.json"), "w") as save_file:
				json.dump(self.user_settings, save_file, indent=4)
		except Exception as e:
			self.display_error_function("Impossible to save preset\n%s"%e)
		else:
			self.display_message_function("Preset saved")










	#check if email address is valid by syntax or domain?
	def check_address_function(self, content):
		pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

		if re.match(pattern, content):
			domain = content.split("@")[1]

			try:
				dns.resolver.resolve(domain, "MX")
				return True

			except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
				return False


		return False












	def get_contact_from_filter_function(self, from_studio=False):
		self.display_success_function("Filtering studio function called")
		#get value selection
		contacttype_index_list = (self.selectionlist_contacttype.selected)
		contacttag_index_list = (self.selectionlist_tags.selected)
		contactdelta_index_list = (self.selectionlist_delta.selected)
		#create list
		contacttype_list = []
		for index in contacttype_index_list:
			contacttype_list.append(self.kind_list[index])

		contacttag_list = []
		for index in contacttag_index_list:
			contacttag_list.append(self.user_settings["UserTagList"][index])

		contactdelta_list = []
		for index in contactdelta_index_list:
			contactdelta_list.append(list(self.user_settings["alertDictionnary"])[index])


		studio_list_contacttime = []

		if "JustContacted" in contactdelta_list:
			studio_list_contacttime.extend(self.no_alert_list)
		if "RecentContact" in contactdelta_list:
			studio_list_contacttime.extend(self.short_alert_list)
		if "LatelyContact" in contactdelta_list:
			studio_list_contacttime.extend(self.medium_alert_list)
		if "PastContact" in contactdelta_list:
			studio_list_contacttime.extend(self.long_alert_list)
		if "NotContacted" in contactdelta_list:
			studio_list_contacttime.extend(self.not_contacted_list)


		selected_studio_name_list = []
		if from_studio == True:

			try:
				#get the list of the studio selected
				
				selected_studio_index = self.listview_studiolist.index_list
				#self.display_message_function(selected_studio_index)
				for index in selected_studio_index:
					selected_studio_name_list.append(self.list_studiolist_display[index])
					#self.display_message_function(self.list_studiolist_display[index])
			except Exception as e:
				self.display_error_function("Impossible to get studio selection")
				self.display_error_function(traceback.format_exc())
				return
			else:
				pass
			#return


		contact_list = {}
		#self.display_message_function(selected_studio_name_list)
		for studio_name, studio_data in self.company_dictionnary.items():

			#self.display_message_function("%s : %s"%(from_studio, studio_name not in selected_studio_name_list))
			if (from_studio==True) and (studio_name not in selected_studio_name_list):
				continue

			if len(studio_list_contacttime) != 0:
				if studio_name not in studio_list_contacttime:
					continue
			#TAGS CONDITIONS
			#	-> if the tag list isn't empty -> check for tags
			#	-> if one of the studio tag is in the tag list

			studio_tags = studio_data["CompanyTags"]
			if len(contacttag_list) > 0:
				found=False

				for tag in studio_tags:
					if tag in contacttag_list:
						found=True
						break


			if (len(contacttag_list) == 0) or (found==True):
				for contact_type, contact_data in studio_data["CompanyContact"].items():

					if contact_type in contacttype_list:
						for c_name, c_data in contact_data.items():
							if self.letter_verification_function(c_data["mail"])==True:
								#contact_list.append(c_data["mail"].replace(" ", ""))
								contact_list["%s; %s"%(studio_name, c_data["mail"])] = {
									"studioName":studio_name,
									"contactName":c_name,
									"contactMail":c_data["mail"]
								}



		self.mail_contact_list = contact_list
		self.optionlist_contact.clear_options()
		self.optionlist_contact.add_options(list(contact_list.keys()))


			


	def test_get_contact_from_filter_function(self, from_studio=False):
		#get value from select fields
		contacttype_index_list = (self.selectionlist_contacttype.selected)
		contacttag_index_list = (self.selectionlist_tags.selected)
		contactdelta_index_list = (self.selectionlist_delta.selected)

		contacttype_list = []
		for index in contacttype_index_list:
			contacttype_list.append(self.kind_list[index])

		contacttag_list = []
		for index in contacttag_index_list:
			contacttag_list.append(self.user_settings["UserTagList"][index])

		contactdelta_list = []
		for index in contactdelta_index_list:
			contactdelta_list.append(list(self.user_settings["alertDictionnary"])[index])



		delta_studio_list = []


		if "RecentContact" in contactdelta_list:
			delta_studio_list.extend(self.short_alert_list)
		if "LatelyContact" in contactdelta_list:
			delta_studio_list.extend(self.medium_alert_list)
		if "PastContact" in contactdelta_list:
			delta_studio_list.extend(self.long_alert_list)
		if "NotContacted" in contactdelta_list:
			delta_studio_list.extend(self.not_contacted_list)


		#self.display_message_function(delta_studio_list)

		#self.display_message_function(contacttype_list)
		#self.display_message_function(contacttag_list)

		#create the list even if the button is not pressed
		selected_studio_name_list = []
		if from_studio == True:

			try:
				#get the list of the studio selected
				
				selected_studio_index = self.listview_studiolist.index_list
				#self.display_message_function(selected_studio_index)
				for index in selected_studio_index:
					selected_studio_name_list.append(self.list_studiolist_display[index])
					#self.display_message_function(self.list_studiolist_display[index])
			except Exception as e:
				self.display_error_function("Impossible to get studio selection")
				self.display_error_function(traceback.format_exc())
				return
			else:
				pass
			#return


		contact_list = {}
		#self.display_message_function(selected_studio_name_list)
		for studio_name, studio_data in self.company_dictionnary.items():

			#self.display_message_function("%s : %s"%(from_studio, studio_name not in selected_studio_name_list))
			if (from_studio==True) and (studio_name not in selected_studio_name_list):
				continue

			if len(delta_studio_list) != 0:
				if studio_name not in delta_studio_list:
					continue
			#TAGS CONDITIONS
			#	-> if the tag list isn't empty -> check for tags
			#	-> if one of the studio tag is in the tag list

			studio_tags = studio_data["CompanyTags"]
			if len(contacttag_list) > 0:
				found=False

				for tag in studio_tags:
					if tag in contacttag_list:
						found=True
						break


			if (len(contacttag_list) == 0) or (found==True):
				for contact_type, contact_data in studio_data["CompanyContact"].items():

					if contact_type in contacttype_list:
						for c_name, c_data in contact_data.items():
							if self.letter_verification_function(c_data["mail"])==True:
								#contact_list.append(c_data["mail"].replace(" ", ""))
								contact_list["%s; %s"%(studio_name, c_data["mail"])] = {
									"studioName":studio_name,
									"contactName":c_name,
									"contactMail":c_data["mail"]
								}



		self.mail_contact_list = contact_list
		self.optionlist_contact.clear_options()
		self.optionlist_contact.add_options(list(contact_list.keys()))








	def remove_studio_with_tag_function(self):
		#get the tag selection in the selectionlist
		contacttag_index_list = (self.selectionlist_tags.selected)
		contacttag_list = []
		for index in contacttag_index_list:
			contacttag_list.append(self.user_settings["UserTagList"][index])
		
		#get the list of studios with this tag in the actual mail contact list
		cleaned_contact_list = {}
		for contact_studio, contact_studio_data in self.mail_contact_list.items():
			contact_studio_name = contact_studio_data["studioName"]
			#get the tag data about this studio
			contact_studio_tag = self.company_dictionnary[contact_studio_name]["CompanyTags"]
			
			for tag in contacttag_list:
				if tag not in contact_studio_tag:
					if contact_studio not in cleaned_contact_list:
						cleaned_contact_list[contact_studio] = contact_studio_data


		self.mail_contact_list = cleaned_contact_list
		#replace values in optionlist
		self.optionlist_contact.clear_options()
		#replace the self.list
		self.optionlist_contact.add_options(list(self.mail_contact_list.keys()))














	def send_mail_function(self):
		os.system("cls")
		print(colored("\n\n\n%s"%pyfiglet.figlet_format("MAIL PORTAL", font="the_edge"), "cyan"))

		#GET THE MAIL KEY
		try:
			with open("data/user/mail_key.dll", "r") as load_key:
				mail_key = load_key.read()
		except Exception as e:
			print(colored("Impossible to load key\n%s"%e, "red"))
			return
		else:
			print(colored("Key loaded", "green"))


		#SETUP THE SERVER
		smtp_server = "smtp.gmail.com"
		port = 587
		user_address = self.user_settings["UserMailAddress"]

		#GET THE MAIL CONTENT 
		mail_header = self.input_mail_header.value
		mail_body = self.textarea_mail.text

		if self.letter_verification_function(mail_header)==False or self.letter_verification_function(mail_body)==False:
			print(colored("MAIL BODY OR MAIL HEADER IS EMPTY!", "red"))
			os.system("pause")
			return

		if len(list(self.mail_contact_list.keys()))==0:
			print(colored("Contact list is empty!", "red"))
			os.system("pause")
			return

		#GET THE MAIL ATTACHED FILES
		attached_file = self.user_settings["UserMailAttached"]
		if os.path.isfile(attached_file)==False:
			print(colored("Attached file doesn't exists!", "red"))
			return




		#DISPLAY FINAL CHOICE TO THE USER BEFORE SENDING THE MAIL
		print(colored("Mail formatting ...", "cyan"))
		print(colored("Your address : ", "cyan"), user_address)
		print(colored("Mail header : ", "cyan"), mail_header)
		print(colored("Mail body :\n", "cyan"), mail_body)


		print(colored("All contact list:\n", "cyan"))
		for contact_name in self.mail_contact_list:
			print(contact_name)
		print("\n\n")

		while True:
			print(colored("Are you sure you want to launch mail sender function?", "cyan"))
			user = input(colored("Y / N ", "magenta"))

			if user == "Y":
				break
			elif user == "N":
				return
			else:
				continue

		
		#SEND LOOP
		try:
			server = smtplib.SMTP(smtp_server, port)
			server.starttls()

			print("Server started ... \n%s"%server)
			print("User address : %s\nUser Key : %s"%(user_address, mail_key))


			server.login(user_address, mail_key)


			contact_list_length = len(list(self.mail_contact_list.keys()))
			i = 0


			header_proxy = mail_header 
			body_proxy = mail_body



			#BUILD THE MAIL
			for contact_name, contact_data in self.mail_contact_list.items():


				mail_header = header_proxy
				mail_body = body_proxy

				studio_name = contact_data["studioName"]
				studio_data = self.company_dictionnary[contact_data["studioName"]]

				#to block email sending
				#continue


				#REPLACE VARIABLES IN EMAIL BODY
				if ("[STUDIONAME]" in mail_header) or ("[STUDIONAME]" in mail_body):
					print("Studioname replaced in mail...")
					if contact_data["studioName"] in list(self.company_dictionnary.keys()):
						mail_header = mail_header.replace("[STUDIONAME]", contact_data["studioName"])
						mail_body = mail_body.replace("[STUDIONAME]", contact_data["studioName"])
					else:
						print(colored("Studio skipped because impossible to replace variables!", "red"))
						continue

				if ("[DEMO_LINK]" in mail_header) or ("[DEMO_LINK]" in mail_body):
					print("DemoLink replaced in mail...")
					mail_header = mail_header.replace("[DEMO_LINK]", str(self.user_settings["UserDemoReelLink"]))
					mail_body = mail_body.replace("[DEMO_LINK]", str(self.user_settings["UserDemoReelLink"]))

				if ("[DEMO_PASSWORD]" in mail_header) or ("[DEMO_PASSWORD]" in mail_body):
					print("DemoPassword replaced in mail...")
					mail_header = mail_header.replace("[DEMO_PASSWORD]", str(self.user_settings["UserDemoReelPassword"]))
					mail_body = mail_body.replace("[DEMO_PASSWORD]", str(self.user_settings["UserDemoReelPassword"]))




				msg = MIMEMultipart()
				msg["From"] = user_address
				msg["To"] = contact_data["contactMail"]
				msg["Subject"] = mail_header 


				print(colored("[%s / %s] NEW MAIL CREATED"%(i, contact_list_length), "cyan"))
				content = """
To : %s
"""%(contact_data["contactMail"])

				body = mail_body
				msg.attach(MIMEText(body))

				try:
					with open(attached_file, "rb") as attach:
						part = MIMEBase("application", "octet-stream")
						part.set_payload(attach.read())

				except Exception as e:
					print(colored("Impossible to read external file and link it to mail\n%s"%e, "red"))
				else:
					encoders.encode_base64(part)
					part.add_header(
						"Content-Disposition",
						f"attachment; filename = {attached_file}",
					)

					msg.attach(part)
					print(colored("External file attached to mail : %s"%attached_file))

				try:
					server.sendmail(user_address, contact_data["contactMail"], msg.as_string())
				except Exception as e:
					print(colored("Impossible to send mail\n%s"%e, "red"))
				else:
					

					#get date to update user dictionnary (last time contacted)		
					if contact_data["studioName"] in list(self.company_dictionnary.keys()):
						#get today date
						date_value = pendulum.parse(str(datetime.now()))
						#get data
						studio_data = self.company_dictionnary[contact_data["studioName"]]
						studio_data["CompanyDate"] = str(date_value)

						print("Date refreshed in user data...")





					print(colored("MAIL SENT : %s\n\n"%contact_data["contactMail"], "green"))


					#update the value of the date in the studio settings dictionnary
					#studio_data["CompanyDate"] = (datetime.now(timezone.utc)).isoformat()
					#self.company_dictionnary[studio_name] = studio_data

				i+=1



			server.quit()
		except Exception as e:
			print(colored("Impossible to connect to server\n%s"%e, "red"))
		else:
			print(colored("TASK DONE", "cyan"))
		










	def check_user_informations_function(self):
		#get all informations in textfield
		user_address = self.input_useraddress.value
		user_mailkey = self.input_mailkey.value
		user_demolink = self.input_demolink.value 
		user_demopassword = self.input_demopassword.value 
		user_resume = self.input_resume.value

		if self.check_address_function(user_address)==False:
			self.display_error_function("Invalid email address")
		else:
			self.user_settings["UserAddress"] = user_address
			

		if self.letter_verification_function(user_mailkey)==False:
			self.display_error_function("Mail key is empty!")
			
		else:
			self.user_settings["UserMailKey"] = user_mailkey

		#check the connection with demoreel link
		try:
			response = requests.get(user_demolink, timeout=5)
		except:
			self.display_error_function("Invalid DemoReel link!")
		else:
			self.display_message_function("DemoReel link checked")
			self.user_settings["UserDemoReelLink"] = user_demolink

		if self.letter_verification_function(user_demopassword) == False:
			self.user_settings["UserDemoPassword"] = None

		if os.path.isfile(user_resume)==False:
			self.display_error_function("Invalid filepath for Resume!")
			return 
		else:
			self.user_settings["UserMailAttached"] = user_resume










	def generate_with_copilot_function(self): 
		"""
		
		"""






