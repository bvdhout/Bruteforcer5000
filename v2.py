import requests
import xml.etree.ElementTree as ET
import os
import threading
import tkinter as tk
import time

keywordsFile = open("./keywords.txt", "r")
variationsFile = open("./variations.txt", "r")
results = open("./results.txt", "w")

bgcolor = "SteelBlue1"
textcolor = "midnight blue"

variations = []

for var in variationsFile.read().split():
    variations.append(var)

keywords = []
keystring = ""

currentChecked = 0

result = ""

for word1 in keywordsFile.read().split():
    keywords.append(word1)
    keystring += word1+", "

file_keywords = ["password", "config", "backup", "database", "credentials", "robots"]

bucket_variations = []

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
    print(url+"\n")
    if response.status_code == 200:
        print(f"[+] Public Bucket Found: {url}")
        print(len(response.content))
        parse_and_filter_files(response.text, bucket_name, url)
        results.write(f"{url}: {len(response.content)}\n")
        results.flush()
        
        result += url+"\n"
        resultLabel.config(text=f"RESULT: \n {result}")

        root.update()

for word in keywords:
    bucket_variations.append(word)

    print(word)

    loadVariations(variations, word)

bases = open("./bases.txt").read().split()#["https://{}.nyc3.digitaloceanspaces.com", "https://{}.s3.amazonaws.com/", "https://{}.ams3.digitaloceanspaces.com"]


def check_s3_bucket(bucket_name):
    global currentChecked

    for base in bases:
        t2 = threading.Thread(target=checkBases, args=(bucket_name, base))

        currentChecked += len(bases)

        t2.start()

def parse_and_filter_files(xml_data, bucket_name, bucket_url):
    try:
        root = ET.fromstring(xml_data)
        files = [obj.find("Key").text for obj in root.findall(".//Contents")]

        filtered_files = [f for f in files if any(kw.lower() in f.lower() for kw in file_keywords)]

        if filtered_files:
            print(f"  >>> Matching Files in {bucket_name}:")
            for file in filtered_files:
                print(f"      - {bucket_url}/{file}")
        else:
            print(f"  >>> No matching files found in {bucket_name}.")
    except ET.ParseError:
        print("  >>> Could not parse bucket contents (possibly empty or restricted).")

def search():

    for bucket in bucket_variations:
        while threading.active_count() > int(maxthreads.get()):
            threadsLabel.config(text=f"THREADS: {threading.active_count()}")
            checkedLabel.config(text=f"SCANNED: {currentChecked}")
            root.update()
            

        t1 = threading.Thread(target=check_s3_bucket, args=(bucket,))
        t1.start()

        threadsLabel.config(text=f"THREADS: {threading.active_count()}")
        checkedLabel.config(text=f"SCANNED: {currentChecked}")
        root.update()


#    t1.join()

root = tk.Tk()
root.title("Search Buckets")

root.geometry("200x300")
root.configure(bg=bgcolor)

tk.Label(text="Find Buckets!! yaay", bg=bgcolor, font="Helvetica", fg=textcolor).pack()
tk.Label(text=f"KEYWORDS: {keystring}", bg=bgcolor, fg=textcolor).pack()
tk.Button(text="SEARCH", command=search, bg=bgcolor, fg=textcolor).pack()

resultLabel = tk.Label(root, text="RESULTS: ", bg=bgcolor, fg=textcolor)
resultLabel.pack()

threadsLabel = tk.Label(root, text="THREADS: 0", bg=bgcolor, fg=textcolor)
threadsLabel.pack()

checkedLabel = tk.Label(root, text="SCANNED: 0", bg=bgcolor, fg=textcolor)
checkedLabel.pack()

tk.Label(root,text="Max Threads", bg=bgcolor, fg=textcolor).pack()
maxthreads = tk.Entry(root,bg=bgcolor, fg=textcolor, )
maxthreads.pack()

root.mainloop()