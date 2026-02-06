from tkinter import *
from tkinter import font, ttk, colorchooser
import json, simplejson

bgcolor = "#ffffff"
fgcolor = "#000000"

def update():
    root.config(bg=bgcolor)

    for i in root.winfo_children():
        if not i["text"] == "Change Background" and not i["text"] == "Change Text Color":
            i.config(font=(clicked.get(), 10, "normal"), background=bgcolor, foreground=fgcolor) #.get()
        else:
            i.config(font=(clicked.get(), 10, "normal")) #.get()

    root.update()

def create():
    with open("./data/themes.json") as file:
        custom = json.load(file)
        if not catagory.get() in catagories:
            custom[catagory.get()] = []

        custom[catagory.get()].append({
            "name": nameValue.get(),
            "bg": bgcolor,
            "fg": fgcolor,
            "font": clicked.get()
        })
        custom = simplejson.dumps(custom, indent=4, sort_keys=False)
        custom = str(custom).replace("'", '"', -1)
           
    with open("./data/themes.json", "w") as old:
        old.write(custom)
        old.flush()
    root.quit()

def check_input(event):
    value = event.widget.get()

    if value == '':
        drop2['values'] = options
    else:
        data = []
        for item in options:
            if value.lower() in item.lower():
                data.append(item)
        drop2['values'] = data

def change_color(colorvalue, button):
    global fgcolor, bgcolor

    if button == changebg:
        bgcolor = colorchooser.askcolor()[1]
        changebg.config(bg=bgcolor)
    else:
        fgcolor = colorchooser.askcolor()[1]
        changefg.config(bg=fgcolor)

    print(colorvalue, bgcolor, fgcolor)

root = Tk() 
root.geometry( "200x250" ) 
root.config(bg="#ffffff")
root.title("Theme Creator")

#   img = PhotoImage(file='./data/empty-bucket.png')
#   root.iconphoto(True, img)
#   myappid = "./data/empty-bucket.png"
#   ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

clicked = StringVar() 
clicked.set( "Arial" ) 

nameValue = StringVar()
nameValue.set("Name")

catagory = StringVar()
catagory.set("custom")

catagories = []

with open("./data/themes.json") as file:
    loaded = json.load(file)
    for i in loaded:
        print(i)
        catagories.append(i)

text = Message(root,text="The quick brown fox jumps over the lazy dog", bg=bgcolor, fg=fgcolor)
text.pack()

options = font.families()

Entry(root,textvariable=nameValue, bg=bgcolor, fg=fgcolor).pack()

drop2 = ttk.Combobox(root, values=options, textvariable=clicked)
drop2.bind('<KeyRelease>', check_input)
drop2.pack()

catagorydrop = ttk.Combobox(root, values=catagories, textvariable=catagory)
catagorydrop.pack()

changebg = Button(root,text="Change Background", fg="#000000", bg="#ffffff")
changebg.config(command=lambda:change_color(bgcolor, changebg))
changebg.pack()

changefg = Button(root,text="Change Text Color", bg="#000000", fg="#ffffff")
changefg.config(command=lambda:change_color(fgcolor, changefg))
changefg.pack()

Button(root, command=update, text="test", bg=bgcolor, fg=fgcolor).pack()
Button(root, command=create, bg=bgcolor, fg=fgcolor, text="Create").pack()

root.mainloop()