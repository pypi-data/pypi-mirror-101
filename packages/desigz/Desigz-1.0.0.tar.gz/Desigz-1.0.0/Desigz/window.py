# from Desigz.system import rgbcolorpick
from Desigz.system import *
import tkinter;from tkinter import Button
root = tkinter.Tk()

#var
DEFAULT_BG = "#202020"
WIDGET_STRING = "widget"

class WINDOW:
	def app(self):
		root.configure(bg=DEFAULT_BG)
		root.geometry("400x370")
		root.iconbitmap("D:\Programms\py\Lib\Desigz\Material\ICO.ico")
		root.title("[DESIGZ]")
	def appconfigure(self,bg=DEFAULT_BG,size={"width":"400","height":"350"}):
		print("[APP_CONFIGURE]:")
		print("  [SIZE]:")
		print("    [WIDTH] : " + "[" + size["width"] + "]" + ";")
		print("    [HEIGHT] : " + "[" + size["height"] + "]" + ";")
		root.configure(bg=bg)

		h = size["height"]
		ht = int(h)-30
		height = f"{ht}"

		size = size["width"] + "x" + height
		# print(size)
		root.geometry(size)
	def run(self):
		root.mainloop()

def btndefunc():
	print("STONKS")

def button(
	title=WIDGET_STRING,
	function=btndefunc,
	x=0,y=0,
	bg=DEFAULT_BG,fg="white",
	width=55,height=24
	):
	button = Button(root,text=title,command=function,bg=bg,fg=fg,
		width=width,height=height
		)
	button.place(x=x,y=y)

if __name__=="__main__":
	NULL