import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import random

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
keepers = []
pairs = []
gameStarted = False

def refresh_labels():
	label0.set_text(" ")
	label1.set_text(" ")
	label2.set_text(" ")
	label3.set_text(" ")
	label4.set_text(" ")
	label5.set_text(" ")

def roll(cup):
	for i in range(len(cup)):
		cup[i].roll()
	keepers = []
	refresh_labels()

def keep(cup, pos):
	keepers.append(int(str(cup[pos])))
	#del cup[pos]

def reset_dice():
	keepers = []
	cup = [dice1, dice2, dice3, dice4, dice5, dice6]
	refresh_buttons()
	current_label = []
	gameStarted = False

def refresh_buttons():
	if len(cup) >= 1:
		button0.set_label(str(cup[0]))
		if len(cup) >= 2:
			button1.set_label(str(cup[1]))
			if len(cup) >= 3:
				button2.set_label(str(cup[2]))
				if len(cup) >= 4:
					button3.set_label(str(cup[3]))
					if len(cup) >= 5:
						button4.set_label(str(cup[4]))
						if len(cup) == 6:
							button5.set_label(str(cup[5]))
	if len(cup) < 6:
		reset_button(button5)
	if len(cup) < 5:
		reset_button(button4)
	if len(cup) < 4:
		reset_button(button3)
	if len(cup) < 3:
		reset_button(button2)
	if len(cup) < 2:
		reset_button(button1)
	if len(cup) < 1:
		reset_button(button0)

def reset_button(GtkButton):
	GtkButton.set_label(" ")

def increment_current_label():
	if leftover_labels != []: 
		current_label.append(leftover_labels.pop(0))
def reset_current_label():
	current_label = [label0]
	leftover_labels = [label1, label2, label3, label4, label5]

class Handler:
	def on_window_main_destroy(self, *args):
		Gtk.main_quit()

	def on_button_roll_clicked(self, button):
		if gameStarted == False:
			roll(cup)
			refresh_buttons()
			reset_current_label()
		else:
			roll(keepers)
			refresh_buttons()
		

### dice buttons
	def on_button0_clicked(self, button):
		keep(cup, 0)
		current_label[-1].set_text(str(keepers[-1]))
		increment_current_label()
		refresh_buttons()

	def on_button1_clicked(self, button):
		keep(cup, 1)
		current_label[-1].set_text(str(keepers[-1]))
		increment_current_label()
		refresh_buttons()

	def on_button2_clicked(self, button):
		keep(cup, 2)
		current_label[-1].set_text(str(keepers[-1]))
		increment_current_label()
		refresh_buttons()

	def on_button3_clicked(self, button):
		keep(cup, 3)
		current_label[-1].set_text(str(keepers[-1]))
		increment_current_label()
		refresh_buttons()

	def on_button4_clicked(self, button):
		keep(cup, 4)
		current_label[-1].set_text(str(keepers[-1]))
		increment_current_label()
		refresh_buttons()

	def on_button5_clicked(self, button):
		keep(cup, 5)
		current_label[-1].set_text(str(keepers[-1]))
		increment_current_label()
		refresh_buttons()


### score buttons
	def on_button_one_clicked(self, button):
		count = keepers.count(1)		
		label_one.set_text(str(count))
		button_one.set_sensitive(False)
		reset_dice()
		print(cup)

	def on_button_two_clicked(self, button):
		count = keepers.count(2) * 2
		label_two.set_text(str(count))
		button_two.set_sensitive(False)
		reset_dice()
		print(cup)

	def on_button_three_clicked(self, button):
		count = keepers.count(3) * 3
		label_three.set_text(str(count))
		button_three.set_sensitive(False)
		reset_dice()

	def on_button_four_clicked(self, button):
		count = keepers.count(4) * 4
		label_four.set_text(str(count))
		button_four.set_sensitive(False)
		reset_dice()

	def on_button_five_clicked(self, button):
		count = keepers.count(5) * 5
		label_five.set_text(str(count))
		button_five.set_sensitive(False)
		reset_dice()

	def on_button_six_clicked(self, button):
		count = keepers.count(6) * 6
		label_six.set_text(str(count))
		button_six.set_sensitive(False)
		reset_dice()

builder = Gtk.Builder()
builder.add_from_file("template.glade")
builder.connect_signals(Handler())

window = builder.get_object("window_main")

label0 = builder.get_object("label0")
label1 = builder.get_object("label1")
label2 = builder.get_object("label2")
label3 = builder.get_object("label3")
label4 = builder.get_object("label4")
label5 = builder.get_object("label5")

label_one = builder.get_object("label_one")
label_two = builder.get_object("label_two")
label_three = builder.get_object("label_three")
label_four = builder.get_object("label_four")
label_five = builder.get_object("label_five")
label_six = builder.get_object("label_six")
label_3x = builder.get_object("label_3x")
label_4x = builder.get_object("label_4x")
label_full = builder.get_object("label_full")
label_small = builder.get_object("label_small")
label_large = builder.get_object("label_large")
label_yazee = builder.get_object("label_yazee")
label_chance = builder.get_object("label_chance")

current_label = [label0]
leftover_labels = [label1, label2, label3, label4, label5]

button0 = builder.get_object("button0")
button1 = builder.get_object("button1")
button2 = builder.get_object("button2")
button3 = builder.get_object("button3")
button4 = builder.get_object("button4")
button5 = builder.get_object("button5")

button_one = builder.get_object("button_one")
button_two = builder.get_object("button_two")
button_three = builder.get_object("button_three")
button_four = builder.get_object("button_four")
button_five = builder.get_object("button_five")
button_six = builder.get_object("button_six")
button_3x = builder.get_object("button_3x")
button_4x = builder.get_object("button_4x")
button_full = builder.get_object("button_full")
button_small = builder.get_object("button_small")
button_large = builder.get_object("button_large")
button_yazee = builder.get_object("button_yazee")
button_chance = builder.get_object("button_chance")

window.show_all()

Gtk.main()