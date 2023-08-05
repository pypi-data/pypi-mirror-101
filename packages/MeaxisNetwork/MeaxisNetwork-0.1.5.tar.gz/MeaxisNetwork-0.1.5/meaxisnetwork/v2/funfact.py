import requests
import json

class Funfact():
	def __init__(self):

		'''

		Gets a random funfact from the API.

		'''


		self.FunfactObject = requests.get("https://api.meaxisnetwork.net/v2/funfact")
		try:
			FunfactJSON = self.FunfactObject.json()
			self.author = FunfactJSON["author"]
			self.id = FunfactJSON["id"]
			self.funfact = FunfactJSON["text"]
		except:
			pass