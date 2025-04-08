import tkinter as tk
import webtools, json, unrelated, ctypes, os
import matplotlib.pyplot as pyplot

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

with open('./data/themes.json') as f:
    themes = json.load(f)

slack_base = "https://{}.slack.com" 
atla_base = "https://{}.atlassian.net"

def changeTheme(bg,fg,fontname, root, menubar):
    global bgcolor, textcolor, font
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

def update(fontsize, root, window, timeout):
    global font
    fontname = font[0]

    font=(fontname, fontsize, "normal")
    webtools.timeout = timeout #, webtools.printall , printall

    for widget in root.winfo_children():
        widget.config(font=font)

    for widget in window.winfo_children():
        widget.config(font=font)

    print(font)
    print(webtools.timeout) #, printall

def showestimate(bucket_variations, bases):
    window = tk.Tk()
    window.config(bg=bgcolor)
    window.geometry("200x100")

    tk.Label(window, text="Estimated Searches: {}".format(len(bucket_variations)*len(bases)), bg=bgcolor, fg=textcolor).pack()
    tk.Label(window, text="Estimated Time: {}m".format(round(((len(bucket_variations)*len(bases))/93)/60)), bg=bgcolor, fg=textcolor).pack()
    tk.Button(window, text="Scan", bg=bgcolor, fg=textcolor, command=window.quit).pack()

    window.mainloop()
    window.update()

def startGUI(keywords, searchCustom, bases, addKeyword, keystring, bucket_variations, currentChecked, checked):
    root = tk.Tk()
    root.title("WEB TOOLS")

    root.geometry("210x300")
    root.configure(bg=bgcolor)
    img = tk.PhotoImage(file='./data/empty-bucket.png')

    root.iconphoto(True, img)
    myappid = "./data/empty-bucket.png"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    menubar = tk.Menu(root)
  
    file = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)
    settings = tk.Menu(menubar, tearoff=False)
    thememenu = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)
    unrelatedMenu = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)
    pause = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)

    all = bases
    all.append(atla_base)

    settings.add_command(label="search buckets", command=lambda:searchCustom(bases, maxthreads, keywords, bucket_variations))
    settings.add_command(label="search buckets+atlassian", command=lambda:searchCustom(all, maxthreads, keywords, bucket_variations))
    settings.add_command(label="search slack",command=lambda:searchCustom([slack_base], maxthreads, keywords, bucket_variations))
    settings.add_command(label="search atlassian",command=lambda:searchCustom([atla_base], maxthreads, keywords, bucket_variations))
    settings.add_command(label="search custom", command=lambda:searchCustom([customBase.get()], maxthreads, keywords, bucket_variations))
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
            category_menu.add_command(label=name, command=lambda bg=bg, fg=fg, font2=font2: changeTheme(bg, fg,font2, root, menubar))

        thememenu.add_cascade(label=category.capitalize(), menu=category_menu)

    thememenu.add_command(label="Create theme", command=lambda:os.system("python createtheme.py"))

    menubar.add_cascade(label="settings", menu=file) 
    menubar.add_cascade(label="search", menu=settings)
    menubar.add_cascade(label="theme", menu=thememenu)
    menubar.add_cascade(label="pause", menu=pause)
    file.add_cascade(label="unrelated", menu=unrelatedMenu)

    root.config(menu=menubar) 

    tk.Label(text="BRUTE FORCE 😛", bg=bgcolor, font=font, fg=textcolor).pack()

    keywordsLabel= tk.Message(text=f"KEYWORDS: {keystring}", bg=bgcolor, fg=textcolor, font=font)
    keywordsLabel.pack()

    addKeywords = tk.Entry(root, bg=bgcolor, fg=textcolor, font=font)
    addKeywords.insert(0,"example")
    addKeywords.pack()

    tk.Button(text="Add keyword", bg=bgcolor, fg=textcolor, font=font, command=addKeyword).pack()

    tk.Label(root,text="Custom url \/", bg=bgcolor, fg=textcolor, font=font).pack()
    customBase = tk.Entry(root, bg=bgcolor, fg=textcolor, font=font)
    customBase.insert(0,"https://{}.example.com")
    customBase.pack()

    threadsLabel = tk.Label(root, text="THREADS: 0", bg=bgcolor, fg=textcolor, font=font)
    threadsLabel.pack()

    checkedLabel = tk.Label(root, text="SCANNED: 0", bg=bgcolor, fg=textcolor, font=font)
    checkedLabel.pack()

    foundLabel = tk.Label(root, text="FOUND: 0", bg=bgcolor, fg=textcolor, font=font)
    foundLabel.pack()

    tk.Label(root,text="Max Threads", bg=bgcolor, fg=textcolor, font=font).pack()
    maxthreads = tk.Entry(root,bg=bgcolor, fg=textcolor, font=font)
    maxthreads.insert(0, "250")
    maxthreads.pack()

    return root, keywordsLabel, addKeywords, customBase, threadsLabel, checkedLabel, maxthreads, foundLabel

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
    window = tk.Tk()
    window.geometry("200x300")
    window.title("settings")
    window.config(bg=bgcolor)

    tk.Label(window,text="SETTINGS", bg=bgcolor, fg=textcolor, font=font).pack()

    tk.Label(window,text="font size", bg=bgcolor, fg=textcolor, font=font).pack()
    fontsize = tk.Entry(window,bg=bgcolor,fg=textcolor,font=font)
    fontsize.insert(0, "10")
    fontsize.pack()

    tk.Label(window, text="timeout",bg=bgcolor,fg=textcolor,font=font).pack()
    timeout = tk.Entry(window,bg=bgcolor,fg=textcolor,font=font)
    timeout.insert(0,"10")
    timeout.pack()

    tk.Button(
        window, 
        text="apply", 
        bg=bgcolor, 
        fg=textcolor, 
        font=font, 
        command=lambda: (
            print("Checkbox States Before Update Call:"),  # Debug print
            update(
                int(fontsize.get()), 
                root, 
                window, 
                int(timeout.get()), 
            )
        )
    ).pack()