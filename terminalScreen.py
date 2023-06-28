# pip install guizero

import tkinter

window = tkinter.Tk()
window.geometry("600x400")

def switchScreen(forgetScreen, showScreen):
    forgetScreen.place_forget()
    showScreen.place(relx=0.5, rely=0.5, anchor="c")
     


rfid = tkinter.Frame(window)
rfid.place(relx=0.5, rely=0.5, anchor="c")
secondScreen = tkinter.Frame(window)

#screen 1
text1 = tkinter.Label(rfid, text="Scanning for RFID...", font=("Arial", 30))
text1.grid(column=0, row=0)
button1 = tkinter.Button(rfid, text="next",  font=("Arial", 30), command=switchScreen(rfid, secondScreen))
button1.grid(column=0, row=1)

#screen 2
text2 = tkinter.Label(secondScreen, text="second screen", font=("Arial", 30))
text2.grid(column=0, row=0)
button2 = tkinter.Button(secondScreen, text="next",  font=("Arial", 30), command=switchScreen(secondScreen, rfid))
button2.grid(column=0, row=1)

window.mainloop()