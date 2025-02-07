import threading, os, time, webtools, GUIHandler
import matplotlib.pyplot as pyplot
# hoi wouter

keywordsFile = open("./keywords.txt", "r")
variationsFile = open("./variations.txt", "r")
results = open("./results.txt", "w")

variations = []

for var in variationsFile.read().split():
    variations.append(var)

keywords = []
keystring = ""

currentChecked = 0

checked = []

for word1 in keywordsFile.read().split():
    keywords.append(word1)
    keystring += word1+", "

bucket_variations = []

def loadKeywords():
    for word in keywords:
        bucket_variations.append(word)
        webtools.loadVariations(variations, word, bucket_variations)

bases = open("./bases.txt").read().split()

def check_custom(custom_name, base):
    global currentChecked

    for i in base: #base
        t2 = threading.Thread(target=webtools.checkBases, args=(custom_name, i, root,foundlabel,))
        currentChecked += 1

        t2.start()

def searchCustom(base, maxthreads, keywords, bucket_variations):
    loadKeywords()
    threadlimit = int(maxthreads.get()) if maxthreads.get().isdigit() else 150
    if not maxthreads.get().isdigit(): print("maxthreads is nog digits so set to 150")

    for custom in bucket_variations:
        while threading.active_count() >= threadlimit:
            root.update()

        t1 = threading.Thread(target=check_custom, args=(custom,base,))
        t1.start()

        threadsLabel.config(text=f"THREADS: {threading.active_count()}")
        checkedLabel.config(text=f"SCANNED: {currentChecked}")
        foundlabel.config(text="FOUND: {}".format(len(open("./results.txt", "r").read().split())))
        root.update()

def addKeyword():
    keywords.append(addKeywords.get())
    keystring = ""

    for i in keywords:
        keystring += i+", "

    keywordsLabel.config(text=f"KEYWORDS: {keystring}")

root, keywordsLabel, addKeywords, customBase, threadsLabel, checkedLabel, maxthreads, foundlabel = GUIHandler.startGUI(keywords, searchCustom, bases, addKeyword, keystring, bucket_variations, currentChecked, checked)

root.mainloop()

# git remote -v
# git add .
# git commit -m "message"
# git push origin main