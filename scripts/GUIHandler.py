import tkinter as tk
import json, ctypes, os, threading
import matplotlib.pyplot as pyplot
import scripts.webtools as webtools
import scripts.unrelated as unrelated

bgcolor = "black"
textcolor = "white"
font = ("Tahoma", 10, "normal")

graph_settings = {
    "colors": {
        "found": (0.1,0.2,1,1),
        "failed": (1,0,0,1),
        "scanned": (0.1,1,0,1)
    }
}

maxthreadsVar = 250
checkbuttons = []

with open('./data/themes.json') as f:
    themes = json.load(f)

with open('./data/bases.json') as f:
    allBases = json.load(f)

with open('./data/settings.json') as f:
    settingsL = json.load(f)

stylesettings = settingsL.items()
stylesettings = dict(stylesettings)["style"]
scansettings = settingsL.items()
scansettings = dict(scansettings)["scan"]

theme = themes[stylesettings["catagory"]]
for item in theme:
    if item["name"] == stylesettings["style"]: theme = item

bgcolor = theme["bg"]
textcolor = theme["fg"]
font = (theme["font"], stylesettings["textsize"], "normal")
maxthreadsVar = scansettings["maxthreads"]

selected_bases = []

def changeTheme(bg,fg,fontname, root, menubar, name, catagory):
    global bgcolor, textcolor, font, stylesettings, scansettings, settingsL, theme
    bgcolor = bg
    textcolor = fg

    fontsize = font[1]
    usedfont=(fontname, fontsize, "normal")

    root.config(bg=bg)
    root.update_idletasks()

    font = usedfont
    for widget in root.winfo_children():
        widget.config(bg=bg, fg=fg, font=usedfont)

    for popup in menubar.winfo_children():
        popup.config(bg=bg,fg=fg,font=usedfont)

    theme = themes[catagory][(i for i, item in enumerate(themes[catagory]) if item["name"] == name).__next__()]

    stylesettings = {
        "catagory": catagory,
        "style": name,
        "textsize": fontsize
    }

    settingsL = {
        "style": stylesettings,
        "scan": scansettings
    }

    with open('./data/settings.json', "w") as f:
        json.dump(settingsL, f)

def update(fontsize, root, window, timeout, maxthreads):
    global font, maxthreadsVar, scansettings, stylesettings, settingsL
    fontname = font[0]

    font=(fontname, fontsize, "normal")
    webtools.timeout = timeout #, webtools.printall , printall

    maxthreadsVar = maxthreads

    for widget in root.winfo_children():
        widget.config(font=font)

    for widget in window.winfo_children():
        widget.config(font=font)

    scansettings = {
        "maxthreads": maxthreadsVar,
        "timeout": webtools.timeout
    }

    stylesettings["textsize"] = fontsize

    settingsL = {
        "style": stylesettings,
        "scan": scansettings
    }

    with open('./data/settings.json', "w") as f:
        json.dump(settingsL, f)

def showestimate(bucket_variations, bases):
    window = tk.Tk()
    window.config(bg=bgcolor)
    window.geometry("200x100")

    l1 = tk.Label(window, text="Estimated Searches: {}".format(len(bucket_variations)*len(bases)), bg=bgcolor, fg=textcolor)
    l2 = tk.Label(window, text="Estimated Time: {}m".format(round(((len(bucket_variations)*len(bases))/93)/60)), bg=bgcolor, fg=textcolor)
    l3 =tk.Button(window, text="Scan", bg=bgcolor, fg=textcolor, command=window.quit)

    l1.pack()
    l2.pack()
    l3.pack()

    def start_scan():
        l1.destroy()
        l2.destroy()
        l3.destroy()

        threads = tk.Label(window, text="THREADS: 0", bg=bgcolor, fg=textcolor, font=font)
        checked = tk.Label(window, text="SCANNED: 0", bg=bgcolor, fg=textcolor, font=font)
        found = tk.Label(window, text="FOUND: 0", bg=bgcolor, fg=textcolor, font=font)

        threads.pack()
        checked.pack()
        found.pack()

        window.update()

        return threads, checked, found

    window.mainloop()

    threads, checked, found = start_scan()
    window.update()

    return threads, checked, found, window

def add_base(settings):
    global selected_bases

    window = tk.Tk()
    window.geometry("200x100")
    window.title("add base")

    window.config(bg=bgcolor)

    #tk.Label(window, text="ADD BASE", bg=bgcolor, fg=textcolor, font=font).pack()
    baseentry = tk.Entry(window, bg=bgcolor, fg=textcolor, font=font)
    baseentry.insert(0, "https://{}.example.com")
    baseentry.pack()

    name = tk.Entry(window, bg=bgcolor, fg=textcolor, font=font)
    name.insert(0, "example")
    name.pack()

    def add_and_close():
        allBases[name.get()] = [baseentry.get()]
        
        with open ("./data/bases.json", "w") as f:
            json.dump(obj=allBases, fp=f)

        settings.add_checkbutton(label=name.get(), command=lambda base=allBases[name.get()]: add_rem_base(base))

        window.destroy()

    tk.Button(window, text="add", bg=bgcolor, fg=textcolor, font=font, command=add_and_close).pack()

def add_keyword(addKeyword, clear):
    if clear == True:
        addKeyword(None, True)
        return
    
    window = tk.Tk()
    window.geometry("200x100")
    window.title("add keyword")
    window.config(bg=bgcolor)

    tk.Label(window, text="ADD KEYWORD", bg=bgcolor, fg=textcolor, font=font).pack()
    keywordentry = tk.Entry(window, bg=bgcolor, fg=textcolor, font=font)
    keywordentry.insert(0, "example")
    keywordentry.pack()

    def add_and_close():
        addKeyword(keywordentry, False)
        window.destroy()

    tk.Button(window, text="add", bg=bgcolor, fg=textcolor, font=font, command=add_and_close).pack()
    window.mainloop()

def add_rem_base(base):
    global selected_bases, allBases
    for var in base:
        if base == allBases:
            selected_bases.append(var)
            continue

        if var not in selected_bases:
            selected_bases.append(var)
        else:
            selected_bases.remove(var)

def startGUI(keywords, searchCustom, addKeyword, keystring, bucket_variations, currentChecked, checked):
    global checkbuttons
    root = tk.Tk()
    root.title("WEB TOOLS")

    root.geometry("210x150")
    root.configure(bg=bgcolor)
    img = tk.PhotoImage(file='./data/empty-bucket.png')

    root.iconphoto(True, img)
    myappid = "./data/empty-bucket.png"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    menubar = tk.Menu(root)
  
    file = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)
    settings = tk.Menu(menubar, tearoff=True)
    thememenu = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)
    unrelatedMenu = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)
    pause = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)

    baseOptions = tk.Menu(menubar, tearoff=False)

    baseOptions.add_command(label='all', command=lambda: add_rem_base(allBases.items()))
    for name, base in allBases.items():
        button = baseOptions.add_checkbutton(label=name, command=lambda base=base: add_rem_base(base))
        
        checkbuttons.append(button)

    settings.add_command(label="add custom", command=lambda:add_base(baseOptions))
    settings.add_command(label="start scan", command=lambda:searchCustom(selected_bases, maxthreadsVar, keywords, bucket_variations))
    settings.add_command(label="show results", command=lambda:webtools.showResults(bgcolor,textcolor))

    unrelatedMenu.add_command(label="subscan", command=lambda:webtools.openSubScanner(bgcolor,textcolor)) 
    unrelatedMenu.add_command(label="sitemap", command=lambda:webtools.sitemap(bgcolor, textcolor))
    unrelatedMenu.add_command(label="reverse ip", command=lambda:webtools.reverse_ip(bgcolor,textcolor))
    file.add_command(label="plot graph", command = lambda:plotGraph(currentChecked,keystring, webtools.checked))
    file.add_command(label="exit", command=root.quit)
    file.add_command(label="open settings", command=lambda:openSettings(root))

    unrelatedMenu.add_command(label="decypher", command=unrelated.openDecypher)

    for category, items in themes.items():
        category_menu = tk.Menu(thememenu, tearoff=False)
        for item in items:
            name, bg, fg, font2 = item["name"], item["bg"], item["fg"], item["font"]
            category_menu.add_command(label=name, command=lambda bg=bg, fg=fg, font2=font2, category=category,name=name: changeTheme(bg, fg,font2, root, menubar, name,category))

        thememenu.add_cascade(label=category.capitalize(), menu=category_menu)

    thememenu.add_command(label="Create theme", command=lambda:os.system("python createtheme.py"))

    menubar.add_cascade(label="settings", menu=file) 
    menubar.add_cascade(label="search", menu=settings)
    menubar.add_cascade(label="theme", menu=thememenu)
    menubar.add_cascade(label="pause", menu=pause)
    file.add_cascade(label="unrelated", menu=unrelatedMenu)
    settings.add_cascade(label="bases", menu=baseOptions)

    root.config(menu=menubar) 

    tk.Label(text="BRUTE FORCE 😛", bg=bgcolor, font=font, fg=textcolor).pack()

    keywordsLabel= tk.Label(text=f"KEYWORDS: {keystring}", bg=bgcolor, fg=textcolor, font=font, wraplength=200)
    keywordsLabel.pack()

    #addKeywords = tk.Entry(root, bg=bgcolor, fg=textcolor, font=font)
    #addKeywords.insert(0,"example")
    #addKeywords.pack()

    tk.Button(text="Add keyword", bg=bgcolor, fg=textcolor, font=font, command=lambda: add_keyword(addKeyword, False,)).pack()
    tk.Button(text="Clear keywords", bg=bgcolor, fg=textcolor, font=font, command=lambda: add_keyword(addKeyword, True,)).pack()

    #tk.Label(root,text="Max Threads", bg=bgcolor, fg=textcolor, font=font).pack()
    #maxthreads = tk.Entry(root,bg=bgcolor, fg=textcolor, font=font)
    #maxthreads.insert(0, "250")
    #maxthreads.pack()

    return root, keywordsLabel
def plotGraph(currentChecked, keystring, checked):
    pyplot.axis([0, len(checked), 0, len(checked)])

    pyplot.ylabel('RESULTS')
    pyplot.xlabel('SEARCHED')
    pyplot.title(keystring)

    pyplot.bar(0,0,0,color=graph_settings["colors"]["failed"],label = "failed")
    pyplot.bar(0,0,0,color=graph_settings["colors"]["found"], label = "found")
    pyplot.bar(0,0,0,color=graph_settings["colors"]["scanned"], label = "scanned")

    x = []
    foundy = []
    failedy = []

    for i, v in enumerate(checked):
        x.append(i)
        foundy.append(v["found"])
        failedy.append(v["failed"])

    pyplot.legend(loc='upper left', shadow=False, facecolor='lightgray')

    pyplot.fill_between(x,x, color=graph_settings["colors"]["scanned"])
    pyplot.fill_between(x,foundy, color=graph_settings["colors"]["found"])
    pyplot.fill_between(x,failedy, color=graph_settings["colors"]["failed"])

    pyplot.title("GRAPH")
    pyplot.show()

def openSettings(root):
    global maxthreadsVar, settingsL
    window = tk.Tk()
    window.geometry("200x300")
    window.title("settings")
    window.config(bg=bgcolor)

    tk.Label(window,text="SETTINGS", bg=bgcolor, fg=textcolor, font=font).pack()

    tk.Label(window,text="font size", bg=bgcolor, fg=textcolor, font=font).pack()
    fontsize = tk.Entry(window,bg=bgcolor,fg=textcolor,font=font)
    fontsize.insert(0, settingsL["style"]["textsize"])
    fontsize.pack()

    tk.Label(window, text="timeout",bg=bgcolor,fg=textcolor,font=font).pack()
    timeout = tk.Entry(window,bg=bgcolor,fg=textcolor,font=font)
    timeout.insert(0, settingsL["scan"]["timeout"])
    timeout.pack()

    tk.Label(window, text="Max Threads", bg=bgcolor, fg=textcolor, font=font).pack()
    maxthreads = tk.Entry(window,bg=bgcolor, fg=textcolor, font=font)
    maxthreads.insert(0, maxthreadsVar)
    maxthreads.pack()

    tk.Button(
        window, 
        text="apply", 
        bg=bgcolor, 
        fg=textcolor, 
        font=font, 
        command=lambda: (
            update(
                int(fontsize.get()), 
                root, 
                window, 
                int(timeout.get()), 
                int(maxthreads.get()) if maxthreads.get().isdigit() else 250
            )
        )
    ).pack()