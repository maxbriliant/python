import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:
	def onDestroy(self, *args):
		Gtk.main_quit()
	def onButtonPressed(self, button):
		print("Hello World!")
	def oneClicked(self, widget):
		print("1")
	
	self.one = builder.get_object("one")
	self.one.connect("clicked",oneClicked)

builder = Gtk.Builder()
builder.add_from_file("calc.glade")
builder.connect_signals(Handler())








window = builder.get_object("windowMain")
window.show_all()
window.connect("destroy", Gtk.main_quit)
Gtk.main()
