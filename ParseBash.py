import requests
import json

class ParseBash:
	def __init__(self):
		self.data = {}
		self.data['Country'] = []
		self.alfa()
		self.savepars()

	def perebor(self,words):
		datares = []
		r = requests.get(f'https://api-new.bilet.do/main/suggestFrom/?agency=fsIJdako5sdfsfsfdba1a7e539c5c1cce7293fe6ae09ee6fs45Jdslfn0due6fds72542768dba99cf208d5503469f90fe4&from={words}')
		if not r.json()['errorStatus']:
			nb = 0
			while True:
				try:
					dist = r.json()['pointsFrom'][nb]['SuggestPoint']
					myDict = {f"{dist['localityName']}": dist}
					datares.append(myDict)
					nb += 1
				except:
					break
		return datares
				

	def alfa(self):
		alf = ["а", "б", "в", "г", "д", "е", "ё", "ж", "з", "и", "й", "к", "л", "м", "н","о", "п", "р", "с", "т", "у", "ф", "х", "ц", "ч", "ш", "щ", "ъ", "ы", "ь", "э", "ю", "я"]
		for i in range(len(alf)):
			for j in range(len(alf)):
				self.data['Country'].extend(self.perebor(f'{alf[i]}{alf[j]}'))

	def savepars(self):
		with open('data.txt', 'w') as outfile:
			json.dump(self.data, outfile, ensure_ascii=False)