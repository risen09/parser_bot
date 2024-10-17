import json
import requests


class BashRoute:
	
	def __init__(self,A1name, B1name, dateAB):
		self.A1name = A1name
		self.B1name = B1name
		self.dateAB = dateAB
		self.RouteRes = []
		self.src = "https://api-new.bilet.do/trips/getTrips"
		self.vendor = "f94f507c-9d17-11e5-9452-001c422ccb08"
		self.A1key = ""
		self.B1key = ""
		self.SaveRoute()		


	def KeyWay(self,data,city):
		route = set()
		for i in data['Country']:
			try: 
				route.add(i[f"{city}"]['pointId'])
			except:
				continue

		return list(route)

	def RoutePrint(self,data):
		route = []
		route.append(f"Рейс - {data['routeNum']}")
		route.append(f"Маршрут - {data['routeName']}")
		route.append(f"Отправление - {data['departureTime']} : Прибытие - {data['arrivalTime']}")
		route.append(f"Стоимость - {data['fare']} {data['currency']}")
		self.RouteRes.append(route)

			

	def WayRoute(self,Route1, Route2, date):
		for i in Route1:
			for j in Route2:
				r = requests.get(f'{self.src}?date={date}&from={i}&to={j}&vendor={self.vendor}')
				if not r.json()['errorStatus']:
					dataway = r.json()['trips']
					self.RouteRes.append(f"Рейсы из {dataway[0]['departureName']} до {dataway[0]['destinationName']} 6 апреля")
					for i in range(len(dataway)):
						self.RoutePrint(dataway[i])

	def WayResult(self):
		return self.RouteRes

	def SaveRoute(self):
		with open('data.txt') as json_file:
			data = json.load(json_file)
			self.A1key = self.KeyWay(data, self.A1name)
			self.B1key = self.KeyWay(data, self.B1name)
			self.WayRoute(self.A1key, self.B1key, self.dateAB)
			self.WayResult()




# r = requests.get(f'{}?date=2023-04-06&from={A1[0]}&to={B1[0]}&vendor=f94f507c-9d17-11e5-9452-001c422ccb08')
# print(r.json())

    
    # for p in data['Country']:
    #     print('Name: ' + p['name'])
    #     print('Website: ' + p['website'])
    #     print('From: ' + p['from'])
    #     print('')