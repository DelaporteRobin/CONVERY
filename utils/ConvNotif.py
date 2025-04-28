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
from termcolor import *


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


colorama.init()


class ConveryNotification:
	def display_message_function(self, message, mute=False):
		if mute == False:
			#self.notify(str(message), timeout=4)
			pass

		log_format = self.create_log_format_function(str(message))
		print(log_format)
		
		
		try:
			self.program_log.append(log_format)
		except AttributeError:
			self.app.program_log.append(log_format)

	def display_success_function(self, message, mute=False):
		if mute == False:
			#self.notify(str(message), timeout=4)
			pass

		log_format = self.create_log_format_function(str(message), "SUCCESS")
		
		print(colored(log_format, "green"))
		try:
			self.program_log.append(log_format)
		except AttributeError:
			self.app.program_log.append(log_format)

	def display_warning_function(self, message, mute=False):
		#print(colored(log_format, "yellow"))
		if mute == False:
			self.notify(str(message).replace("[", "\[").replace("]","\]"), timeout=4)

	def display_error_function(self, message, mute=False):
		if mute == False:
			self.notify(str(message).replace("[", "\[").replace("]","\]"), severity="error", timeout=4)
		
		log_format = self.create_log_format_function(str(message), "ERROR")
		print(colored(log_format, "red"))
		try:
			self.program_log.append(log_format)
		except AttributeError:
			self.app.program_log.append(log_format)


	def create_log_format_function(self, message, severity="MESSAGE"):
		log_format = {
			"date":str(datetime.now()),
			"severity":severity,
			"content":str(message.replace("[", "\[").replace("]","\]"))
		}
		
		try:
			self.add_log_line_function(log_format)
		except AttributeError:
			self.app.add_log_line_function(log_format)
		
		return log_format