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
			for key, value in FunfactJSON.items():
				vars(self)[key] = value
		except:
			pass