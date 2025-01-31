import tkinter as tk
import webtools, json
import matplotlib.pyplot as pyplot

bgcolor = "black"
textcolor = "white"

with open('./themes.json') as f:
    themes = json.load(f)

slack_base = "https://{}.slack.com" 
atla_base = "https://{}.atlassian.net"

def changeTheme(bg,fg, root, menubar):
    bgcolor = bg
    textcolor = fg

    root.config(bg=bgcolor)
    root.update_idletasks()

    for widget in root.winfo_children():
        widget.config(bg=bgcolor,fg=textcolor)

    for popup in menubar.winfo_children():
        popup.config(bg=bgcolor,fg=textcolor)

def startGUI(keywords, searchCustom, bases, addKeyword, keystring, bucket_variations, currentChecked, checked):
    root = tk.Tk()
    root.title("WEB TOOLS")

    root.geometry("200x300")
    root.configure(bg=bgcolor)

    menubar = tk.Menu(root, background=bgcolor, fg=textcolor,bg=bgcolor)
  
    file = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)
    settings = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)
    thememenu = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)

    settings.add_command(label="search buckets",command=lambda:searchCustom(bases, maxthreads, keywords, bucket_variations))
    settings.add_command(label="search slack",command=lambda:searchCustom([slack_base], maxthreads, keywords, bucket_variations))
    settings.add_command(label="search atlassian",command=lambda:searchCustom([atla_base], maxthreads, keywords, bucket_variations))
    settings.add_command(label="search custom", command=lambda:searchCustom([customBase.get()], maxthreads, keywords, bucket_variations))

    file.add_command(label="subscan", command=lambda:webtools.openSubScanner(bgcolor,textcolor)) 
    file.add_command(label="plot graph", command = lambda:plotGraph(currentChecked, keystring, checked))
    file.add_command(label="exit", command=root.quit)

    for category, items in themes.items():
        category_menu = tk.Menu(thememenu, tearoff=False)
        for item in items:
            name, bg, fg = item["name"], item["bg"], item["fg"]
            category_menu.add_command(label=name, command=lambda bg=bg, fg=fg: changeTheme(bg, fg, root, menubar))

        thememenu.add_cascade(label=category.capitalize(), menu=category_menu)

    menubar.add_cascade(label="settings", menu=file) 
    menubar.add_cascade(label="search", menu=settings)
    menubar.add_cascade(label="theme", menu=thememenu)
    root.config(menu=menubar) 

    tk.Label(text="BRUTE FORCE 😛", bg=bgcolor, font="Helvetica", fg=textcolor).pack()

    keywordsLabel= tk.Label(text=f"KEYWORDS: {keystring}", bg=bgcolor, fg=textcolor)
    keywordsLabel.pack()

    addKeywords = tk.Entry(root, bg=bgcolor, fg=textcolor)
    addKeywords.insert(0,"example")
    addKeywords.pack()

    tk.Button(text="Add keyword", bg=bgcolor, fg=textcolor, command=addKeyword).pack()

    tk.Label(root,text="Custom url \/", bg=bgcolor, fg=textcolor).pack()
    customBase = tk.Entry(root, bg=bgcolor, fg=textcolor)
    customBase.insert(0,"https://{}.example.com")
    customBase.pack()

    threadsLabel = tk.Label(root, text="THREADS: 0", bg=bgcolor, fg=textcolor)
    threadsLabel.pack()

    checkedLabel = tk.Label(root, text="SCANNED: 0", bg=bgcolor, fg=textcolor)
    checkedLabel.pack()

    tk.Label(root,text="Max Threads", bg=bgcolor, fg=textcolor).pack()
    maxthreads = tk.Entry(root,bg=bgcolor, fg=textcolor)
    maxthreads.insert(0, "100")
    maxthreads.pack()

    resultLabel = tk.Label(root, text="RESULTS: ", bg=bgcolor, fg=textcolor)
    resultLabel.pack()

    return root, keywordsLabel, addKeywords, customBase, threadsLabel, checkedLabel, maxthreads, resultLabel

def plotGraph(currentChecked, keystring, checked):
    pyplot.axis([0,currentChecked, 0, currentChecked])

    pyplot.ylabel('THING FOUND!!!')
    pyplot.xlabel('LINKS SEARCHED')
    pyplot.title(keystring)

    for i, v in enumerate(checked):
        pyplot.bar(i,v,1,color=(0.1,0.2,1,1))

    pyplot.plot()
    pyplot.show()