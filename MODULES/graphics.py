from tkinter import Tk, Frame, Label

root = Tk()
root.title("Asistente Virual - JL TUTORIALES")
root.geometry('640x480')

class main_window(Frame):
	def __init__(self, root):
		super().__init__(root)
		Label(self, text = "Ventana Principal").pack()

		self.pack()

w1 = main_window(root)

root.mainloop()