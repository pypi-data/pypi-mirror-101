from Desigz.system import *
import tkinter
from tkinter import Label
from tkinter import Button

"""

IM = INFOMESSAGE

"""

imroot = tkinter.Tk()

class MESSAGE:
	def __init__(self):
		NULL
	def infomes(self,cfg={"title":"INFO","text":"INFORMATION"},function=imroot.destroy):
		imroot.title(cfg["title"])
		imroot.geometry("250x170")

		lbl = Label(imroot,text=cfg["text"])
		lbl.place(x=0,y=0)

		btn = Button(imroot,text="Ok",command=function)
		btn.place(x=50,y=50)

		imroot.iconbitmap("D:\Programms\py\Lib\Desigz\Material\ICO.ico")
		imroot.mainloop()

if __name__=="__main__":
	pass