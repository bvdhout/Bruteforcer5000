import threading, os, time
import scripts.webtools as webtools
import scripts.GUIHandler as GUIHandler
# hoi wouter

keywordsFile = open("./data/keywords.txt", "r")
variationsFile = open("./data/variations.txt", "r")
results = open("./data/results.txt", "w")

variations = []

for var in variationsFile.read().split():
    variations.append(var)

keywords = []
keystring = ""

currentChecked = 0
foundNum = 0

checked = []

for word1 in keywordsFile.read().split():
    keywords.append(word1)
    keystring += word1+", "

bucket_variations = []

def loadKeywords():
    bucket_variations.clear()
    for word in keywords:
        bucket_variations.append(word)
        webtools.loadVariations(variations, word, bucket_variations)

def check_custom(custom_name, base, found):
    global currentChecked

    for i in base: 
        t2 = threading.Thread(target=webtools.checkBases, args=(custom_name, i, root,found,))
        currentChecked += 1

        t2.start()

def searchCustom(base, maxthreads, keywords, bucket_variations):
    global threadsLabel, checkedLabel, foundlabel, currentChecked
    loadKeywords()
    threads, checked, found, window = GUIHandler.showestimate(bucket_variations, base)

    threadlimit = maxthreads
    currentChecked = 0
    webtools.foundNum = 0

    for custom in bucket_variations:
        while threading.active_count() >= threadlimit:
            root.update()

        t1 = threading.Thread(target=check_custom, args=(custom,base,found))
        t1.start()

        if window:
            threads.config(text=f"THREADS: {threading.active_count()}")
            checked.config(text=f"SCANNED: {currentChecked}")
            found.config(text=f"FOUND: {webtools.foundNum}")
            window.update()

def addKeyword(addKeywords, value):
    global keywords, keywordsLabel, keystring
    if value == False:
        keywords.append(addKeywords.get())
        keystring = ""
        for i in keywords:
            keystring += i+", "
        keywordsLabel.config(text=f"KEYWORDS: {keystring}")
        with open("./data/keywords.txt", "w") as wordsfile:
            for word in keywords:
                wordsfile.write(word+"\n")
                wordsfile.flush()
    else:
        keywords = []
        keystring = ""
        keywordsLabel.config(text=f"KEYWORDS: {keystring}")
        with open("./data/keywords.txt", "w") as wordsfile:
            wordsfile.write("")
            wordsfile.flush()

root, keywordsLabel = GUIHandler.startGUI(keywords, searchCustom, addKeyword, keystring, bucket_variations, currentChecked, checked)

root.mainloop()

# git remote -v
# git add .
# git commit -m "message"
# git pull origin main
# git push origin main