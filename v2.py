import requests, threading, os, time
import xml.etree.ElementTree as ET
import tkinter as tk
import matplotlib.pyplot as pyplot

keywordsFile = open("./keywords.txt", "r")
variationsFile = open("./variations.txt", "r")
results = open("./results.txt", "w")

bgcolor = "bisque"
textcolor = "PeachPuff4"

variations = []

for var in variationsFile.read().split():
    variations.append(var)

keywords = []
keystring = ""

currentChecked = 0

result = ""
resultList = []

checked = []

for word1 in keywordsFile.read().split():
    keywords.append(word1)
    keystring += word1+", "

file_keywords = ["password", "config", "backup", "database", "credentials", "robots"]

bucket_variations = []

slack_base = "https://{}.slack.com"
atla_base = "https://{}.atlassian.net"

def loadVariations(varations2, word):
    bucket_variations.append(word)

    for variation in varations2:
        bucket_variations.append(word+variation)
        bucket_variations.append(variation+word)
        bucket_variations.append(word+"-"+variation)
        bucket_variations.append(variation+"-"+word)

def checkBases(bucket_name, base):
    global result, currentChecked
    url = base.format(bucket_name)
    response = requests.get(url)

    checked.append(len(resultList))
#    print(response.headers)
    print(url+"\n")
    if response.status_code == 200:
        print(f"[+] Public Bucket Found: {url}")
        results.write(f"{url}\n")
        results.flush()
        
        result += url+"\n"
        resultList.append(url)
        resultLabel.config(text=f"RESULT: \n {result}")

        root.update()

def loadKeywords():
    for word in keywords:
        bucket_variations.append(word)

        print(word)

        loadVariations(variations, word)

bases = open("./bases.txt").read().split()


def check_s3_bucket(bucket_name):
    global currentChecked

    for base in bases:
        t2 = threading.Thread(target=checkBases, args=(bucket_name, base))

        currentChecked += len(bases)

        t2.start()

def check_slack(slack_name):
    global currentChecked

    for i in range(1):

        t2 = threading.Thread(target=checkBases, args=(slack_name, slack_base))
        currentChecked += 1

        t2.start()


def check_atlassian(atla_name):
    global currentChecked

    for i in range(1):

        t2 = threading.Thread(target=checkBases, args=(atla_name, atla_base))
        currentChecked += 1

        t2.start()

def check_custom(custom_name):
    global currentChecked

    start = time.time()

    for i in range(1):

        t2=threading.Thread(target=checkBases, args= (custom_name, customBase.get()))
        currentChecked += 1

        t2.start()

    end = time.time()

def search():
    loadKeywords()
    threadlimit = maxthreads.get() if maxthreads.get().isdigit() else 100

    for bucket in bucket_variations:
        while threading.active_count() > threadlimit:
            threadsLabel.config(text=f"THREADS: {threading.active_count()}")
            checkedLabel.config(text=f"SCANNED: {currentChecked}")
            root.update()
            

        t1 = threading.Thread(target=check_s3_bucket, args=(bucket,))
        t1.start()

        threadsLabel.config(text=f"THREADS: {threading.active_count()}")
        checkedLabel.config(text=f"SCANNED: {currentChecked}")
        root.update()

def searchSlack():
    loadKeywords()
    threadlimit = maxthreads.get() if maxthreads.get().isdigit() else 100

    for slack in bucket_variations:
        while threading.active_count() > threadlimit:
            threadsLabel.config(text=f"THREADS: {threading.active_count()}")
            checkedLabel.config(text=f"SCANNED: {currentChecked}")
            root.update()

        t1 = threading.Thread(target=check_slack, args=(slack,))
        t1.start()

        threadsLabel.config(text=f"THREADS: {threading.active_count()}")
        checkedLabel.config(text=f"SCANNED: {currentChecked}")
        root.update()

def searchAtlassian():
    loadKeywords()
    threadlimit = maxthreads.get() if maxthreads.get().isdigit() else 100

    for atla in bucket_variations:
        while threading.active_count() > threadlimit:
            threadsLabel.config(text=f"THREADS: {threading.active_count()}")
            checkedLabel.config(text=f"SCANNED: {currentChecked}")
            root.update()

        t1 = threading.Thread(target=check_atlassian, args=(atla,))
        t1.start()

        threadsLabel.config(text=f"THREADS: {threading.active_count()}")
        checkedLabel.config(text=f"SCANNED: {currentChecked}")
        root.update()

def searchCustom():
    loadKeywords()
    threadlimit = maxthreads.get() if maxthreads.get().isdigit() else 100

    for custom in bucket_variations:
        while threading.active_count() > threadlimit:
            threadsLabel.config(text=f"THREADS: {threading.active_count()}")
            checkedLabel.config(text=f"SCANNED: {currentChecked}")
            root.update()

        t1 = threading.Thread(target=check_custom, args=(custom,))
        t1.start()

        threadsLabel.config(text=f"THREADS: {threading.active_count()}")
        checkedLabel.config(text=f"SCANNED: {currentChecked}")
        root.update()

def addKeyword():
    keywords.append(addKeywords.get())
    keystring = ""

    for i in keywords:
        keystring += i+", "

    keywordsLabel.config(text=f"KEYWORDS: {keystring}")

root = tk.Tk()
root.title("WEB TOOLS")

root.geometry("300x500")
root.configure(bg=bgcolor)

tk.Label(text="BRUTE FORCE 😛", bg=bgcolor, font="Helvetica", fg=textcolor).pack()
keywordsLabel= tk.Label(text=f"KEYWORDS: {keystring}", bg=bgcolor, fg=textcolor)
keywordsLabel.pack()

addKeywords = tk.Entry(root, bg=bgcolor, fg=textcolor)
addKeywords.pack()

tk.Button(text="Add keyword", bg=bgcolor, fg=textcolor, command=addKeyword).pack()

tk.Button(text="SEARCH BUCKETS", command=search, bg=bgcolor, fg=textcolor).pack()
tk.Button(root,text="SEARCH SLACK", bg=bgcolor, fg=textcolor, command=searchSlack).pack()
tk.Button(root, text="SEARCH ATLASSIAN", bg=bgcolor, fg=textcolor, command=searchAtlassian).pack()
tk.Button(root, text="SEARCH CUSTOM", bg=bgcolor, fg=textcolor, command=searchCustom).pack()

customBase = tk.Entry(root, bg=bgcolor, fg=textcolor)
customBase.pack()

threadsLabel = tk.Label(root, text="THREADS: 0", bg=bgcolor, fg=textcolor)
threadsLabel.pack()

checkedLabel = tk.Label(root, text="SCANNED: 0", bg=bgcolor, fg=textcolor)
checkedLabel.pack()

tk.Label(root,text="Max Threads", bg=bgcolor, fg=textcolor).pack()
maxthreads = tk.Entry(root,bg=bgcolor, fg=textcolor)
maxthreads.pack()

resultLabel = tk.Label(root, text="RESULTS: ", bg=bgcolor, fg=textcolor)
resultLabel.pack()

root.mainloop()

pyplot.axis([0,currentChecked, 0, currentChecked])
#pyplot.bar(0,len(resultList),1)
pyplot.ylabel('THING FOUND!!!')
pyplot.xlabel('LINKS SEARCHED')

for i, v in enumerate(checked):
    pyplot.bar(i,v,1,color=(0.1,0.2,1,1))

pyplot.plot()
pyplot.show()