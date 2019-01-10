from random import *
import smtplib
from amazon.api import AmazonAPI

game_spending_limit = 20

import csv

class Player:

	def __init__(self,name, email, wish_list):
		self.name = name
		self.email = email
		self.wish_list = wish_list
		self.other_player = None

def read_csv():
	players = list()
	with open('yea.csv') as csv_file:
	    csv_reader = csv.reader(csv_file, delimiter=',')
	    line_count = 0
	    for row in csv_reader:
	        if line_count == 0:
	            line_count += 1
	        else:
	        	name = row[0]
	        	email = row[1]
	        	wish_list = row[2]
	        	line_count = line_count + 1
	        	temp = Player(name, email, wish_list)
	        	players.append(temp)


	return players

def assign_players(list1):
	temp_list = list1.copy()
	count = 0
	for x in list1:
		random_num = randint(0,len(temp_list) - 1)
		while (x.name == temp_list[random_num].name):
			random_num = randint(0,len(temp_list) - 1)
			# special case prevent infinite loop. if only one person left. 
			if(x.name == temp_list[random_num].name and len(temp_list) == 1):
				rand = randint(0,len(list1)-1)
				if list1[rand].other_player is not None:
					list1[rand].other_player = temp_list[0]
					for x in list1:
						if x.other_player is None:
							x.other_player = list1[rand]
							return list1
					print("hi")
		x.other_player = temp_list[random_num]
		del temp_list[random_num]
		count = count + 1

	return list1

def send_mail(player):
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login("email", "pass")
	wish_list = player.other_player.wish_list.split(" ")
	print(wish_list)
	msg = "Your Pairing is " + player.other_player.name + "! \n " + "Here is his Wish-List: \n" + ' '.join(wish_list)
	server.sendmail("email", player.email , msg)
	server.quit()

def execute_secret_santa(final_list):
	for x in final_list:
		send_mail(x)
	print("\nEmails have been sent")


AMAZON_ACCESS_KEY = ""
AMAZON_SECRET_KEY = ""
AMAZON_ASSOC_TAG = ""



all_players = read_csv()

final_list = assign_players(all_players)
for x in final_list:
	print(x.name)
	print(x.other_player.name)
	print("----------------------")
execute_secret_santa(final_list)


