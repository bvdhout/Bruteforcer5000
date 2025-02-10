import tkinter as tk
import webtools, json, unrelated
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

    root.geometry("210x300")
    root.configure(bg=bgcolor)

    menubar = tk.Menu(root)
  
    file = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)
    settings = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)
    thememenu = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)
    unrelatedMenu = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)
    pause = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)

    settings.add_command(label="search buckets",command=lambda:searchCustom(bases, maxthreads, keywords, bucket_variations))
    settings.add_command(label="search slack",command=lambda:searchCustom([slack_base], maxthreads, keywords, bucket_variations))
    settings.add_command(label="search atlassian",command=lambda:searchCustom([atla_base], maxthreads, keywords, bucket_variations))
    settings.add_command(label="search custom", command=lambda:searchCustom([customBase.get()], maxthreads, keywords, bucket_variations))
    settings.add_command(label="show results", command=lambda:webtools.showResults(bgcolor,textcolor))

    unrelatedMenu.add_command(label="subscan", command=lambda:webtools.openSubScanner(bgcolor,textcolor)) 
    unrelatedMenu.add_command(label="sitemap", command=lambda:webtools.sitemap(bgcolor, textcolor))
    unrelatedMenu.add_command(label="reverse ip", command=lambda:webtools.reverse_ip(bgcolor,textcolor))
    file.add_command(label="plot graph", command = lambda:plotGraph(currentChecked,keystring, webtools.checked))
    file.add_command(label="exit", command=root.quit)

    unrelatedMenu.add_command(label="decypher", command=unrelated.openDecypher)

    for category, items in themes.items():
        category_menu = tk.Menu(thememenu, tearoff=False)
        for item in items:
            name, bg, fg = item["name"], item["bg"], item["fg"]
            category_menu.add_command(label=name, command=lambda bg=bg, fg=fg: changeTheme(bg, fg, root, menubar))

        thememenu.add_cascade(label=category.capitalize(), menu=category_menu)

    menubar.add_cascade(label="settings", menu=file) 
    menubar.add_cascade(label="search", menu=settings)
    menubar.add_cascade(label="theme", menu=thememenu)
    menubar.add_cascade(label="pause", menu=pause)
    file.add_cascade(label="unrelated", menu=unrelatedMenu)

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

    foundLabel = tk.Label(root, text="FOUND: 0", bg=bgcolor, fg=textcolor)
    foundLabel.pack()

    tk.Label(root,text="Max Threads", bg=bgcolor, fg=textcolor).pack()
    maxthreads = tk.Entry(root,bg=bgcolor, fg=textcolor)
    maxthreads.insert(0, "250")
    maxthreads.pack()

    return root, keywordsLabel, addKeywords, customBase, threadsLabel, checkedLabel, maxthreads, foundLabel

def plotGraph(currentChecked, keystring, checked):
    sigma = currentChecked
    pyplot.axis([0, len(checked), 0, len(checked)])

    pyplot.ylabel('RESULTS')
    pyplot.xlabel('SEARCHED')
    pyplot.title(keystring)

    for i, v in enumerate(checked):
        pyplot.bar(i,v,1,color=(0.1,0.2,1,1))

    pyplot.plot()
    pyplot.show()