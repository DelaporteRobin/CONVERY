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

from utils.ConvWidget import MultiListView, MultiListItem

colorama.init()


class ConveryNotification:
	def display_message_function(self, message=" ", severity="message", time=True, mute=True):
		#format message
		message=str(message)
		#display notification first
		if (mute == False) or (severity in ["error", "warning"]):
			notify_severity = "information"
			if (severity == "warning") or (severity=="error"):
				notify_severity == severity
			try:
				self.notify(message, timeout=4, severity=notify_severity)
			except Exception as e:
				self.app.notify(message, timeout=4, severity=notify_severity)
		#create format for main notification
		notification_format = ("%s|%s → %s"%(str(datetime.now()), severity.upper(), message))
		#notification_format = notification_format.replace("[", "\[").replace("]", "\]")
		#create the log line for listview
		label_format = Label(notification_format)
		#color label
		if severity in ["warning", "error", "success"]:
			try:
				label_format.styles.color = self.theme_variables[f'{severity}-lighten-1']
			except:
				label_format.styles.color = self.app.theme_variables[f'{severity}-lighten-1']
		try:
			self.listview_log.append(MultiListItem(label_format))
		except AttributeError:
			self.app.listview_log.append(MultiListItem(label_format))
		