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



	def save_attached_files_function(self):
		filename = self.input_attached_filename.value 
		filepath = self.input_attached_filepath.value 

		if (self.letter_verification_function(filename)==False) or (self.letter_verification_function(filepath)==False):
			self.display_message_function("You have to enter both filename and filepath!", "error")
			return
		else:
			if os.path.isfile(filepath)==False:
				self.display_message_function("This filepath isn't valid! File doesn't exists!", "error")
				return
			else:
				try:
					user_attached_files = self.user_settings["UserAttachedFiles"]
				except:
					user_attached_files = {}

				user_attached_files[filename] = filepath

				self.user_settings["UserAttachedFiles"] = user_attached_files
				self.save_user_settings_function()
				self.update_contact_class_function()



	def remove_attached_files_function(self):
		#get index selection in selection list
		try:
			user_attached_files_list = list(self.user_settings["UserAttachedFiles"].keys())
			user_attached_files_dictionnary = self.user_settings["UserAttachedFiles"]
			for index in self.selectionlist_attached_files.selected:
				#get the filename
				user_attached_files_dictionnary.pop(user_attached_files_list[index])
			#save back the dictionnary
			self.user_settings["UserAttachedFiles"] = user_attached_files_dictionnary
			self.save_user_settings_function()
			self.update_contact_class_function()
		except Exception as e:
			self.display_message_function("Impossible to remove attached file from list", "error")
			self.display_message_function(traceback.format_exc(), "error", False)
		else:
			self.display_message_function("Attached file(s) removed","success")





	def save_mail_address_function(self):
		#get the mail address and the key
		#check letter presence
		#save in dictionnary
		new_mail_address = self.input_mail_address.value 
		new_mail_key = self.input_mail_key.value

		if (self.letter_verification_function(new_mail_key)==True) and (self.letter_verification_function(new_mail_address)==True):
			try:
				#get mail data dictionnary
				mail_data = self.user_settings["UserMailData"]
				mail_data[new_mail_address] = new_mail_key

				self.save_user_settings_function()
			except Exception as e:
				self.display_message_function("Impossible to save email address","error")
				self.display_message_function(traceback.format_exc(), "error", False)
			else:
				self.display_message_function("Email address updated", "success")
				#update the interface
				self.update_contact_class_function()
		else:
			self.display_message_function("Mail address or mail key is empty!","error")
			return




	def remove_mail_address_function(self):
		#get the selected mail address
		try:
			mail_address = self.user_mail_address_list[self.listview_mailaddress.index]
		except Exception as e:
			self.display_message_function("Impossible to get selected mail address!","error")
			return
		else:
			#try to remove the key if present in dictionnary
			mail_data = self.user_settings["UserMailData"]
			try:
				mail_data.pop(mail_address)
			except:
				pass 

			#save back
			self.save_user_settings_function()
			#update interface
			self.update_contact_class_function()






	def save_mail_variable_function(self):
		#get variable name and variable value
		var_name = self.input_variablename.value 
		var_value = self.input_variablevalue.value

		if (self.letter_verification_function(var_name)==False) or (self.letter_verification_function(var_value)==False):
			self.display_message_function("You have to enter a value for both variable name and variable value!","error")
			return
		else:
			#get the var dictionnary
			try:
				var_dictionnary = self.user_settings["UserVarDictionnary"]
			except:
				var_dictionnary = {}
			#add the variables to the variables dictionnary
			#update the key if it already exists!
			var_dictionnary[var_name] = var_value
			#save the new dictionnary
			self.user_settings["UserVarDictionnary"] = var_dictionnary
			self.save_user_settings_function()
			self.update_contact_class_function()
			self.display_message_function("Mail variable saved","success")






	def remove_mail_variable_function(self):
		#get selected key
		key_selected = list(self.user_settings["UserVarDictionnary"].keys())[self.listview_variablelist.index]
		#get the var dictionnary
		var_dictionnary = self.user_settings["UserVarDictionnary"]
		#remove the key
		var_dictionnary.pop(key_selected)
		#save the dictionnary
		self.user_settings["UserVarDictionnary"] = var_dictionnary
		self.save_user_settings_function()
		self.update_contact_class_function()
		self.display_message_function("Mail variable removed","success")





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
			self.display_message_function("You have to enter a name, a header, and a valid content for the mail preset", "error")
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
			#self.update_informations_function()
			self.update_contact_class_function()
		else:
			self.display_message_function("A preset with the same name is already registered", "error")



	def load_mail_preset_function(self):
		try:
			with open(os.path.join(os.getcwd(), "data/user/UserSettings.json"), "r") as read_file:
				self.user_settings = json.load(read_file)
		except Exception as e:
			self.display_message_function("Impossible to load mail presets", "error")
			self.display_message_function(traceback.format_exc(), "error", False)
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
			self.display_message_function("Impossible to save preset\n%s"%e, "error")
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
		self.display_message_function("Filtering studio function called","success")
		#get value selection
		contacttype_index_list = (self.selectionlist_contacttype.selected)
		contacttag_index_list = (self.selectionlist_tags.selected)
		contactdelta_index_list = (self.selectionlist_delta.selected)
		contactlocation_index_list = (self.selectionlist_location.selected)
		#create list
		contacttype_list = []
		for index in contacttype_index_list:
			contacttype_list.append(self.kind_list[index])

		contacttag_list = []
		for index in contacttag_index_list:
			contacttag_list.append(self.user_settings["UserTagList"][index])

		contactdelta_list = []
		self.display_message_function(";".join(list(self.user_settings["alertDictionnary"])))
		for index in contactdelta_index_list:
			self.display_message_function(f'{str(index)} : {list(self.user_settings["alertDictionnary"])[index]}')
	
		for index in contactdelta_index_list:
			contactdelta_list.append(list(self.user_settings["alertDictionnary"])[index])

		contactlocation_list = []
		for index in contactlocation_index_list:
			contactlocation_list.append(self.location_list[index])

		self.display_message_function(str(", ".join(contactlocation_list)))

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

				#self.display_message_function(str(selected_studio_index).replace("[", "").replace("]",""))
				for index in selected_studio_index:
					selected_studio_name_list.append(self.list_studiolist_display[index])
					#self.display_message_function(self.list_studiolist_display[index])
			except Exception as e:
				self.display_message_function("Impossible to get studio selection", "error")
				self.display_message_function(traceback.format_exc(), "error",False)
				return
			else:
				pass
			#return

		self.display_message_function("Finding contacts for the following studios:")


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

			#check for the location
			if len(contactlocation_list) != 0:
				studio_location_list = studio_data["CompanyLocation"].upper().split(" ")
				found=False
				for studio_location in studio_location_list:
					if studio_location in contactlocation_list:
						found=True
						break
				if found==False:
					continue


			studio_tags = studio_data["CompanyTags"]
			if len(contacttag_list) > 0:
				if self.checkbox_exclude_tag.value==False:
					found=False
				else:
					found=True

				for tag in studio_tags:
					if tag in contacttag_list:
						if (self.checkbox_exclude_tag.value)==True:
							found=False
							break

						else:
							found=True
							break
			#self.display_message_function("		%s"%studio_name)

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
				self.display_message_function("Impossible to get studio selection","error")
				self.display_message_function(traceback.format_exc(), "error", False)
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




		print(colored("Mail formatting ...", "magenta"))
		print("Trying to gather all required informations...")


		#SETUP THE SERVER
		smtp_server = "smtp.gmail.com"
		port = 587
		#user_address = self.user_settings["UserMailAddress"]
		#get the mail address selected by the user
		try:
			user_address = list(self.user_settings["UserMailData"].keys())[self.listview_mailaddress.index]
		except TypeError:
			print(colored("You have to select the mail address you want to use!", "red"))
			return
		else:
			#get the mail key
			mail_key = self.user_settings["UserMailData"][user_address]




		attached_file_list_index = self.selectionlist_attached_files.selected
		attached_file_list = []

		print(colored("\n\nAttached file list : ", "cyan"))
		for index in attached_file_list_index:
			#get the filename for each index
			filepath = self.user_settings["UserAttachedFiles"][list(self.user_settings["UserAttachedFiles"].keys())[index]]
			if os.path.isfile(filepath)==True:

				if filepath in attached_file_list:
					print(colored("\tSkipped - file already attached : %s"%filepath, "red"))
				else:
					attached_file_list.append(filepath)
					print("\tfile added : %s"%filepath)
			else:
				print(colored("\tSkipped - file doesn't exist : %s"%filepath, "red"))





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
		"""
		attached_file = self.user_settings["UserMailAttached"]
		if os.path.isfile(attached_file)==False:
			print(colored("Attached file doesn't exists!", "red"))
			return
		"""





		
		print(colored("Mail address : ", "cyan"), user_address)
		print(colored("Mail API key : ", "cyan"), mail_key)
		print(colored("Mail header : ", "cyan"), mail_header)
		print(colored("\n\nMail body :\n", "cyan"), mail_body)


		print(colored("\n\nAll contact list:\n", "cyan"))
		for contact_name in self.mail_contact_list:
			print(contact_name)

		while True:
			print(colored("\nAre you sure you want to launch mail sender function?", "cyan"))
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

			print(colored("Server started ... \n%s"%server, "green"))
			#print("User address : %s\nUser Key : %s"%(user_address, mail_key))


			server.login(user_address, mail_key)


			contact_list_length = len(list(self.mail_contact_list.keys()))
			i = 0


			header_proxy = mail_header 
			body_proxy = mail_body



			#BUILD THE MAIL
			for contact_name, contact_data in self.mail_contact_list.items():



				print(colored("[%s / %s] Writing mail to : %s"%(i, contact_list_length, contact_name), "cyan"))

				mail_header = header_proxy
				mail_body = body_proxy

				studio_name = contact_data["studioName"]
				studio_data = self.company_dictionnary[contact_data["studioName"]]

				#to block email sending
				#continue


				#REPLACE VARIABLES IN EMAIL BODY
				#try to replace system variable
				print(colored("\tReplacing system variables..."))
				try:
					mail_header = mail_header.replace("[CONTACTNAME]",contact_data["studioName"])
					mail_body = mail_body.replace("[CONTACTNAME]", contact_data["studioName"])
				except Exception as e:
					print(colored("\t-Error happened : %s"%e, "red"))
				else:
					print(colored("\t-System variables replaced", "green"))


				#try to replace user variables
				#get user variables in user settings
				user_variable_dictionnary = self.user_settings["UserVarDictionnary"]
				print(colored("\tReplacing user variables..."))
				for user_var_name, user_var_value in user_variable_dictionnary.items():
					print("\t-checking [%s] - %s"%(user_var_name, user_var_value))
					try:
						mail_header = mail_header.replace("[%s]"%user_var_name, user_var_value)
						mail_body = mail_body.replace("[%s]"%user_var_name, user_var_value)
					except Exception as e:
						print(colored("\t-Error happened : %s"%e, "red"))
					else:
						pass
				print(colored("\t-User variables replaced","green"))


				"""
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
				"""




				msg = MIMEMultipart()
				msg["From"] = user_address
				msg["To"] = contact_data["contactMail"]
				msg["Subject"] = mail_header 

				content = """
To : %s
"""%(contact_data["contactMail"])

				body = mail_body
				msg.attach(MIMEText(body))

				print("\tAttaching file list...")
				for attached_file in attached_file_list:
					try:
						with open(attached_file, "rb") as attach:
							part = MIMEBase("application", "octet-stream")
							part.set_payload(attach.read())

					except Exception as e:
						print(colored("\t-Impossible to read external file and link it to mail\n%s"%e, "red"))
					else:
						encoders.encode_base64(part)
						part.add_header(
							"Content-Disposition",
							f"attachment; filename = {attached_file}",
						)

						msg.attach(part)
						print(colored("\t-External file attached to mail : %s"%attached_file, "green"))
				

				
				try:
					print("\tExecuting send command ...")
					server.sendmail(user_address, contact_data["contactMail"], msg.as_string())
					
				except Exception as e:
					print(colored("Impossible to send mail\n%s"%e, "red"))
				else:
					
					print(colored("\tMail sent to %s"%(contact_data["contactMail"]), "green"))
					#get date to update user dictionnary (last time contacted)		
					if contact_data["studioName"] in list(self.company_dictionnary.keys()):
						#get today date
						date_value = pendulum.parse(str(datetime.now()))
						#get data
						studio_data = self.company_dictionnary[contact_data["studioName"]]
						studio_data["CompanyDate"] = str(date_value)

						print("\tDate refreshed in user data...\n\n")





					


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
			self.display_message_function("Invalid email address", "error")
		else:
			self.user_settings["UserAddress"] = user_address
			

		if self.letter_verification_function(user_mailkey)==False:
			self.display_message_function("Mail key is empty!")
			
		else:
			self.user_settings["UserMailKey"] = user_mailkey

		#check the connection with demoreel link
		try:
			response = requests.get(user_demolink, timeout=5)
		except:
			self.display_message_function("Invalid DemoReel link!", "error")
		else:
			self.display_message_function("DemoReel link checked")
			self.user_settings["UserDemoReelLink"] = user_demolink

		if self.letter_verification_function(user_demopassword) == False:
			self.user_settings["UserDemoPassword"] = None

		if os.path.isfile(user_resume)==False:
			self.display_message_function("Invalid filepath for Resume!", "error")
			return 
		else:
			self.user_settings["UserMailAttached"] = user_resume










	def generate_with_copilot_function(self): 
		"""
		
		"""






