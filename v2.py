import threading, os, time, webtools, GUIHandler

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

    for i in base:
        t2 = threading.Thread(target=webtools.checkBases, args=(custom_name, i, root, resultLabel,))
        currentChecked += len(base)

        t2.start()

def searchCustom(base, maxthreads, keywords, bucket_variations):
    loadKeywords()
    threadlimit = int(maxthreads.get()) if maxthreads.get().isdigit() else 100

    for custom in bucket_variations:
        while threading.active_count() > threadlimit:
            root.update()

        t1 = threading.Thread(target=check_custom, args=(custom,base,))
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

root, keywordsLabel, addKeywords, customBase, threadsLabel, checkedLabel, maxthreads, resultLabel = GUIHandler.startGUI(keywords, searchCustom, bases, addKeyword, keystring, bucket_variations, currentChecked, checked)

root.mainloop()