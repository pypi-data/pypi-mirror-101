import os
import sys
import webbrowser

#Variables

NULL = "nullity"

def rgbcolorpick(rgb):
    return "#%02x%02x%02x" % rgb

#    ЦВЕТА В КЗС
red_rgb = rgbcolorpick((255,0,0))
green_rgb = rgbcolorpick((0,255,0))
blue_rgb = rgbcolorpick((0,0,255))
black_rgb = rgbcolorpick((0,0,0))
white_rgb = rgbcolorpick((255,255,255))

if __name__=="__main__":
	import tkinter
	root = tkinter.Tk()
	root.geometry("400x370")
	root.title("MCLAUNCHER")
	root.configure(bg="#303030")
	from tkinter import Label

	lbl = Label(
		text="MINECRAFT",
		font=["Arial",20,"bold"],
		bg="#303030",fg="white"
		)

	def FUNC():
		root.destroy()

	lbl.place(x=124,y=30)

	from tkinter import Button
	btn = Button(
		text="PLAY",width=10,height=2,
		bg="#404040",fg="white",font=["Arial",11,"bold"],
		command=FUNC
		)
	btn.place(x=151,y=100)

	root.mainloop()