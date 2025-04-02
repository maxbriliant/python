#!/usr/bin/python
import random



def main():

	class dice():
		def __init__(self):
		
			self.top = 6
		
		def roll(self):
			self.top = random.randint(1,6)
		
		def __str__(self):
			return str(self.top)
		def __repr__(self):
			return str(self.top)

	dice1 = dice()
	dice2 = dice()
	dice3 = dice()
	dice4 = dice()
	dice5 = dice()
	dice6 = dice()

	
	cup = [dice1, dice2, dice3, dice4, dice5, dice6]

	def roll(cup):
		for i in range(len(cup)):
			cup[i].roll()

	roll(cup)
	print(cup)



main()