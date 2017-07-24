import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'}

prior_years = ["165", "137", "96", "97", "98", "99", "100"] #Need to programatically generate this

players = {}

for year in prior_years:
	url = "http://www.rolltide.com/roster.aspx?roster=%s&path=wvball" %(year)
	response = requests.get(url, headers = headers)
	parser = BeautifulSoup(response.content, 'html.parser')
	player_details = parser.select(".sidearm-roster-player-pertinents")

	for i in player_details:
		players_names = i.select(".sidearm-roster-player-name")[0]
		players_heights = i.select(".sidearm-roster-player-position")[0]
		try:
			players[str(players_names.select("a")[0].text)] = str(players_heights.select("span")[1].text)
		except:
			players[str(players_names.select("a")[0].text)] = "No Height Found"
			pass

#Filter out no height players
players = {name: height for name, height in players.items() if height != "No Height Found"}

#Converting height to inches float
for name, height in players.items():
	feet = height.split("'")[0]
	if len(feet) > 1:
		inch = feet[1:]
		feet = float(feet[0])
		inches = float(inch + "." + height.split("'")[1].translate(None, "\""))
	else: 
		feet = float(feet)
		inches = float(height.split("'")[1].translate(None, "\""))

	players[name] = feet*12 + inches

	# To print as a table
def playerRoster():
	for name, height in players.items():
		print('{} {}'.format(name, height))

def maxHeight():
	maxHeight = 0.0
	tallestPlayer = ""
	for name, height in players.items():
		if height > maxHeight:
			maxHeight = height
			tallestPlayer = name
	return tallestPlayer + " " + str(maxHeight)

def avgHeight():
	totalHeight = 0.0
	counter = 0
	for name, height in players.items():
		totalHeight += height
		counter +=1
	return str(round(totalHeight/counter, 2)) + " " + "inches"

#User Requestable Data
user_input = raw_input("What would you like to know? ")
if user_input == "maxheight":
	print maxHeight()
if user_input == "roster":
	print playerRoster()
if user_input == "avg":
	print avgHeight()


