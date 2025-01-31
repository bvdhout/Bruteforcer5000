import threading, os, time, webtools, GUIHandler

keywordsFile = open("./keywords.txt", "r")
variationsFile = open("./variations.txt", "r")
results = open("./results.txt", "w")

bgcolor = "black"
textcolor = "Yellow"

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

bucket_variations = []

slack_base = "https://{}.slack.com" 
atla_base = "https://{}.atlassian.net"
subdomain_base = "https://crt.sh/?q={}&output=json"

def loadKeywords():
    for word in keywords:
        bucket_variations.append(word)

        print(word)

        webtools.loadVariations(variations, word, bucket_variations)

bases = open("./bases.txt").read().split()

def check_custom(custom_name, base):
    global currentChecked

    start = time.time()

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

def loadKeywords():
    for word in keywords:
        bucket_variations.append(word)

        print(word)

        webtools.loadVariations(variations, word, bucket_variations)

root, keywordsLabel, addKeywords, customBase, threadsLabel, checkedLabel, maxthreads, resultLabel = GUIHandler.startGUI(keywords, searchCustom, bases, addKeyword, keystring, bucket_variations)

root.mainloop()

GUIHandler.plotGraph(currentChecked, keystring, checked)