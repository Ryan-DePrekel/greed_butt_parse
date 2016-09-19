#Console application to parse Greedbutt.com Binding of Isaac daily highscores
#Usage will be you supply it a Steam Id and it will get overall stats
#Other forms of usage would be to supply it a day and steam ID to get the daily score
#This will be done by parsing the JSON data at the requested page by appending /?json to each URL
# Usage 1: supply args of steam ID and the day you want 0 being most recent 9 being last data available
# Current Usage: python greed_butt_parse.py <steamID> <day_index> if no index if provided then defaults to most recent
# 76561198046935999

import json
import urllib
import sys

json_build = "/?json"


# Helper Function to pull data from greeedbutt.com
def json_reader(url):
	response = urllib.urlopen(url)
	data = json.loads(response.read())
	return data

#This will hold the specific data for a daily. Looks as though the json can only pull the last
# 10 dailies. url is https://greedbutt.com/score/ + hash of the day + /?json
# Date, rank/entries, Stage, Schwag, XXX bonus, lamb bonus, mega bonus, rush, exploration, damage, time, item, hits
class Daily:
	date = None
	rank = 0
	entries = 0
	stage = 0
	schwag = 0
	xxx = 0
	lamb = 0
	mega = 0
	rush = 0
	exploration = 0
	damage = 0
	time = 0
	item = 0
	hits = 0
	percentile = 0.0

	def __init__(self, day_hash):
		self.url = "https://greedbutt.com/score/" + day_hash + json_build
		self.data = json_reader(self.url)

	def get_score(self):
		self.date = self.data['date']
		self.score = self.data['score']
		self.rank = self.data['rank']
		self.entries = self.data['entries']
		self.stage = self.data['details']['stage_bonus']
		self.schwag = self.data['details']['schwag_bonus']
		self.xxx = self.data['details']['xxx_bonus']
		self.lamb = self.data['details']['lamb_bonus']
		self.mega = self.data['details']['megasatan_bonus']
		self.rush = self.data['details']['rush_bonus']
		self.exploration = self.data['details']['exploration_bonus']
		self.damage = self.data['details']['damage_penalty']
		self.time = self.data['details']['time_penalty']
		self.item = self.data['details']['item_penalty']
		self.hits = self.data['details']['hits']
		self.percentile = (float(self.rank) / float(self.entries)) * 100.0

	def display_daily(self):
		#print self.data
		self.get_score()
		print "Date: %s Rank: %d Percentile: %.2f Score: %d" % (self.date, self.rank, self.percentile, self.score)
		print "Stage Bonus: %d Exploration Bonus: %d Schwag Bonus: %d " % (self.stage, self.exploration, self.schwag)
		if self.xxx != 0:
			print "??? bonus: %d" % self.xxx
		elif self.lamb != 0:
			print "Lamb bonus: %d" % self.lamb
		elif self.mega != 0:
			print "Megasatan bonus: %d" % self.mega
		if self.rush != 0:
			print "Rush bonus: %d" % self.rush
		print "Damage Penalty: -%d Time Penalty: -%d Item Penalty: -%d Total Hits: %d" % (self.damage, self.time, self.item, self.hits)

#This will hold the player data requested from greedbutt.com
#Name, Number of runs, Average Rank, Best Rank, Data from daily requested
class Player:
	#Init values
	name = None
	runs = 0
	avg_rank = 0
	best_rank = 0
	daily = None

	#Consume the data for use
	def __init__(self, argv):
		url = "https://greedbutt.com/player/" + argv[1] + json_build
		self.data = json_reader(url)
		if len(argv) == 2:
			self.day_flag = 0
		else:
			self.day_flag = int(argv[2])

	def get_data(self):
		self.name = self.data['player']['name']
		self.runs = self.data['player']['stats']['runs']
		self.avg_rank = self.data['player']['stats']['avg_rank']
		self.best_rank = self.data['player']['stats']['best_rank']
		self.daily = Daily(self.data['player']['history'][self.day_flag]['hash'])

	def display_player(self):
		print "Name: %s   Total Runs: %d   Average Rank: %d  Best Rank:  %d" % (self.name, self.runs, self.avg_rank, self.best_rank)

	def show_stats(self):
		self.daily.display_daily()

if __name__ == "__main__":
	try:
		player = Player(sys.argv)
		player.get_data()
		player.display_player()
		player.show_stats()
	except IndexError as e:
			print "Usage Error: python greed_butt_parse.py <steamID> <day index>"
