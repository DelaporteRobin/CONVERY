import os




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



