import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject, Gio

class WindowMain:

	def __init__(self):

		self.builder = Gtk.Builder()
		self.builder.add_from_file("calc.glade")

		self.windowMain = self.builder.get_object("windowMain")
		self.windowMain.show()

		self.one = self.builder.get_object("one")
		self.one.connect("clicked", self.oneClicked)

	def oneClicked(self, widget):
		print("1")


	def main(self):
		Gtk.main()



application = WindowMain()
application.show_all()
application.connect("destroy", Gtk.main_quit)
application.main()