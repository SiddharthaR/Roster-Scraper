import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.99 Safari/537.36'}

prior_years = ["165", "137", "96", "97", "98", "99", "100"] #Need to programatically genearate this

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

# To print as a table
for name, height in players.items():
    print('{} {}'.format(name, height))
