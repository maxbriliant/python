import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
	def on_window_destroy(self, *args):
		Gtk.main_quit()

	def button11_clicked(self, button):
		label = click()
		button11.set_label(label)
		button11.set_sensitive(False)
		senk1[0] = label
		waage1[0] = label
		quer1[0] = label
		printWaage()
		global counter
		counter+=1

		if counter == 9:
			check()
			if won == False:
				reset()

		check()

	def button12_clicked(self, button):
		label = click()
		button12.set_label(label)
		button12.set_sensitive(False)
		senk2[0] = label
		waage1[1] = label
		printWaage()
		global counter
		counter+=1

		if counter == 9:
			check()
			if won == False:
				reset()

		check()

	def button13_clicked(self, button):
		label = click()
		button13.set_label(label)
		button13.set_sensitive(False)
		senk3[0] = label
		waage1[2] = label
		quer2[0] = label
		printWaage()
		global counter
		counter+=1

		if counter == 9:
			check()
			if won == False:
				reset()

		check()

	def button21_clicked(self, button):
		label = click()
		button21.set_label(label)
		button21.set_sensitive(False)
		senk1[1] = label
		waage2[0] = label
		printWaage()
		global counter
		counter+=1

		if counter == 9:
			check()
			if won == False:
				reset()

		check()

	def button22_clicked(self, button):
		label = click()
		button22.set_label(label)
		button22.set_sensitive(False)
		senk2[1] = label
		waage2[1] = label
		quer1[1] = label
		quer2[1] = label
		printWaage()
		global counter
		counter+=1

		if counter == 9:
			check()
			if won == False:
				reset()

		check()

	def button23_clicked(self, button):
		label = click()
		button23.set_label(label)
		button23.set_sensitive(False)
		senk3[1] = label
		waage2[2] = label
		printWaage()
		global counter
		counter+=1

		if counter == 9:
			check()
			if won == False:
				reset()

		check()

	def button31_clicked(self, button):
		label = click()
		button31.set_label(label)
		button31.set_sensitive(False)
		senk1[2] = label
		waage3[0] = label
		quer2[2] = label
		printWaage()
		global counter
		counter+=1

		if counter == 9:
			check()
			if won == False:
				reset()

		check()

	def button32_clicked(self, button):
		label = click()
		button32.set_label(label)
		button32.set_sensitive(False)
		senk2[2] = label
		waage3[1] = label
		printWaage()
		global counter
		counter+=1

		if counter == 9:
			check()
			if won == False:
				reset()

		check()

	def button33_clicked(self, button):
		label = click()
		button33.set_label(label)
		button33.set_sensitive(False)
		senk3[2] = label
		waage3[2] = label
		quer1[2] = label
		printWaage()
		global counter
		counter+=1

		if counter == 9:
			check()
			if won == False:
				reset()

		check()

	def buttonYes_clicked(self, button):
		reset()
		messageBox.hide()

	def buttonNo_clicked(self, button):
		Gtk.main_quit()

def click():
	if last == []:
		last.append("X")
		return "X"
	if last[-1] == "X":
		last.append("O")
		return "O"
	if last[-1] == "O":
		last.append("X")
		return "X"

def reset():
	button11.set_label(" ")
	button11.set_sensitive(True)
	button12.set_label(" ")
	button12.set_sensitive(True)
	button13.set_label(" ")
	button13.set_sensitive(True)
	button21.set_label(" ")
	button21.set_sensitive(True)
	button22.set_label(" ")
	button22.set_sensitive(True)
	button23.set_label(" ")
	button23.set_sensitive(True)
	button31.set_label(" ")
	button31.set_sensitive(True)
	button32.set_label(" ")
	button32.set_sensitive(True)
	button33.set_label(" ")
	button33.set_sensitive(True)	

	global last
	global waage1
	global waage2
	global waage3
	global senk1
	global senk2
	global senk3
	global quer1
	global quer2
	global counter
	global won

	last = []
	counter = 0
	won = False

	waage1 = [None, None, None]
	waage2 = [None, None, None]
	waage3 = [None, None, None]

	senk1 = [None, None, None]
	senk2 = [None, None, None]
	senk3 = [None, None, None]

	#q1= 11,22,33
	#q2= 13, 22, 31
	quer1 = [None, None, None]
	quer2 = [None, None, None]


def check(click):
	return None

def printSenk():
	print(senk1)
	print(senk2)
	print(senk3)
	print("\n")

def printWaage():
	print(waage1)
	print(waage2)
	print(waage3)
	print("\n")

def printQuer():
	print(quer1)
	print(quer2)
	print("\n")

def check():
	if (waage1[0] == "X") and (waage1[1] == "X") and (waage1[2] == "X"):
		print("X Gewinnt!")
		won = True
		messageBox.show_all()
	elif (waage1[0] == "O") and (waage1[1] == "O") and (waage1[2] == "O"):
		print("O Gewinnt!")
		won = True
		messageBox.show_all()
	elif (waage2[0] == "X") and (waage2[1] == "X") and (waage2[2] == "X"):
		print("X Gewinnt!")
		won = True
		messageBox.show_all()
	elif (waage2[0] == "O") and (waage2[1] == "O") and (waage2[2] == "O"):
		print("O Gewinnt!")
		won = True
		messageBox.show_all()
	elif (waage3[0] == "X") and (waage3[1] == "X") and (waage3[2] == "X"):
		print("X Gewinnt!")
		won = True
		messageBox.show_all()
	elif (waage3[0] == "O") and (waage3[1] == "O") and (waage3[2] == "O"):
		print("O Gewinnt!")
		won = True
		messageBox.show_all()

	elif (senk1[0] == "X") and (senk1[1] == "X") and (senk1[2] == "X"):
		print("X Gewinnt!")
		won = True
		messageBox.show_all()
	elif (senk1[0] == "O") and (senk1[1] == "O") and (senk1[2] == "O"):
		print("O Gewinnt!")
		won = True
		messageBox.show_all()
	elif (senk2[0] == "X") and (senk2[1] == "X") and (senk2[2] == "X"):
		print("X Gewinnt!")
		won = True
		messageBox.show_all()
	elif (senk2[0] == "O") and (senk2[1] == "O") and (senk2[2] == "O"):
		print("O Gewinnt!")
		won = True
		messageBox.show_all()
	elif (senk3[0] == "X") and (senk3[1] == "X") and (senk3[2] == "X"):
		print("X Gewinnt!")
		won = True
		messageBox.show_all()
	elif (senk3[0] == "O") and (senk3[1] == "O") and (senk3[2] == "O"):
		print("O Gewinnt!")
		won = True
		messageBox.show_all()


	elif (quer1[0] == "X") and (quer1[1] == "X") and (quer1[2] == "X"):
		print("X Gewinnt!")
		won = True
		messageBox.show_all()
	elif (quer1[0] == "O") and (quer1[1] == "O") and (quer1[2] == "O"):
		print("O Gewinnt!")
		won = True
		messageBox.show_all()
	elif (quer2[0] == "X") and (quer2[1] == "X") and (quer2[2] == "X"):
		print("X Gewinnt!")
		won = True
		messageBox.show_all()
	elif (quer2[0] == "O") and (quer2[1] == "O") and (quer2[2] == "O"):
		print("O Gewinnt!")
		won = True
		messageBox.show_all()

won = False
counter = 0
last = []

waage1 = [None, None, None]
waage2 = [None, None, None]
waage3 = [None, None, None]

senk1 = [None, None, None]
senk2 = [None, None, None]
senk3 = [None, None, None]


#q1= 11,22,33
#q2= 13, 22, 31
quer1 = [None, None, None]
quer2 = [None, None, None]


builder = Gtk.Builder()
builder.add_from_file("window.glade")
builder.connect_signals(Handler())

button11 = builder.get_object("button11")
button12 = builder.get_object("button12")
button13 = builder.get_object("button13")
button21 = builder.get_object("button21")
button22 = builder.get_object("button22")
button23 = builder.get_object("button23")
button31 = builder.get_object("button31")
button32 = builder.get_object("button32")
button33 = builder.get_object("button33")
buttonYes = builder.get_object("buttonYes")
buttonNo = builder.get_object("buttonNo")


messageBox = builder.get_object("messageBox")

window = builder.get_object("window")
window.show_all()


Gtk.main()
