import tkinter as tk
import webtools
from matplotlib import pyplot

bgcolor = "black"
textcolor = "Yellow"

slack_base = "https://{}.slack.com" 
atla_base = "https://{}.atlassian.net"

def startGUI(keywords, searchCustom, bases, addKeyword, keystring, bucket_variations):
    root = tk.Tk()
    root.title("WEB TOOLS")

    root.geometry("200x300")
    root.configure(bg=bgcolor)

    menubar = tk.Menu(root, background=bgcolor, fg=textcolor,bg=bgcolor)
  
    file = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)
    settings = tk.Menu(menubar, tearoff=False, background=bgcolor, fg=textcolor, bg=bgcolor)

    settings.add_command(label="search buckets",command=lambda:searchCustom(bases, maxthreads, keywords, bucket_variations))
    settings.add_command(label="search slack",command=lambda:searchCustom([slack_base], maxthreads, keywords, bucket_variations))
    settings.add_command(label="search atlassian",command=lambda:searchCustom([atla_base], maxthreads, keywords, bucket_variations))
    settings.add_command(label="search custom", command=lambda:searchCustom([customBase.get()], maxthreads, keywords, bucket_variations))

    file.add_command(label="Subscan", command=webtools.openSubScanner) 
    file.add_command(label="Exit", command=root.quit)

    menubar.add_cascade(label="settings", menu=file) 
    menubar.add_cascade(label="search", menu=settings)
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