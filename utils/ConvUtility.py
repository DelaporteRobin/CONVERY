import os

import markdown



class ConveryUtility():
	def say_hello(self):
		print("hello")


	def letter_verification_function(self, text):
		letter = "abcdefghijklmnopqrstuvwxyz"
		capital = letter.upper()
		figure = "0123456789"

		list_letter = list(letter)
		list_capital = list(capital)
		list_figure = list(figure)


		list_text = list(text)
		if len(list_text) == 0:
			return False 
		else:
			for i in range(len(list_text)):
				if (list_text[i] in list_letter) or (list_text[i] in list_capital) or (list_text[i] in list_figure):
					return True 
			return False




	def convert_md_to_html_function(self, content, filename):
		try:
			#html convert
			html_content = markdown.markdown(content)
			#html saving
			with open(filename, "w", encoding="utf-8") as save_html:
				save_html.write(html_content)
			
		except Exception as e:
			return e 
		else:
			return True




