import random

class dice():
	def __init__(self):
	
		self.top = 6
		self.cup = []

	def roll(self):
		self.top = random.randint(1,6)
	
	def __str__(self):
		return str(self.top)
	def __repr__(self):
		return str(self.top)
	def makeCup(self):

		dice1 = dice()
		dice2 = dice()
		dice3 = dice()
		dice4 = dice()
		dice5 = dice()
		dice6 = dice()

		self.cup = [dice1, dice2, dice3, dice4, dice5, dice6]
		return self.cup

	def roll(self):
		for i in range(len(self.cup)):
			self.cup[i].roll()



