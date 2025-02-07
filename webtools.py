import requests, threading
import tkinter as tk

results = open("./results.txt", "w")
variations = open("./variations.txt", "r").read().split()

subdomain_base = "https://crt.sh/?q={}&output=json"

result = ""
resultList = []
checked = []

def loadVariations(varations, word, bucket_variations):
    for variation in varations:
        bucket_variations.append(word+variation)
        bucket_variations.append(variation+word)
        bucket_variations.append(word+"-"+variation)
        bucket_variations.append(variation+"-"+word)

def checkBases(bucket_name, base, root, foundlabel):
    global result

    url = base.format(bucket_name)

    checked.append(len(resultList))
    print(url+"\n")
    
    try:
        response = requests.get(url, timeout=8)  # 8 seconds timeout
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
    except requests.exceptions.Timeout:
        print("Request timed out.")

        return
    except requests.exceptions.RequestException as e:
        return

    if response.status_code == 200:
        print(f"[+] Public Bucket Found: {url}")
        results.write(f"{url}\n")
        results.flush()
        
        result += url+"\n"
        resultList.append(url)
        root.update()
        response.close()

    response.close()

    return checked, results, 

def showResults(bgcolor,textcolor):
    root = tk.Tk()
    root.geometry("500x300")

    scrollbar = tk.Scrollbar(root)
    scrollbar.pack( side = tk.RIGHT, fill=tk.BOTH)

    mylist = tk.Listbox(root,width=500, yscrollcommand = scrollbar.set)
    for index, line in enumerate(open("./results.txt", "r").read().split()):
       mylist.insert(tk.END, str(index) + ": " + str(line))
    
    mylist.pack( side = tk.LEFT, fill = tk.BOTH )
    scrollbar.config( command = mylist.yview )

    root.mainloop()

def openSubScanner(bgcolor,textcolor): # die van enzo is superieur dit is simpelweg een kleine variant (ik wordt niet onder druk gezet om dit te zeggen)
    def subScan(): 

        global result

        scanDomain = domain.get()

        window.update()
        url = subdomain_base.format(scanDomain)
        window.update()
        json = requests.get(url)

        if json.status_code == 200:
            subScanButton.config(text="SCANNING...")
            window.update()
            for i in json.json():
                if not i["name_value"] in resultList:
                    print(i["name_value"], "\n")
                    window.update()

                    results.write("{}\n".format(i["name_value"]))
                    results.flush()
            
                    result += i["name_value"]+"\n"
                    resultList.append(i["name_value"])

        json.close()
        
        subScanButton.config(text="SCAN")


    window = tk.Tk()

    window.title("SUBDOMAIN SCANNER")
    window.geometry("200x75")
    window.configure(bg=bgcolor)

    tk.Label(window, text="DOMAIN", bg=bgcolor, fg=textcolor).pack()
    domain = tk.Entry(window, bg=bgcolor, fg=textcolor)
    domain.insert(0, "example.com")
    domain.pack()

    subScanButton = tk.Button(window, text="SCAN", bg=bgcolor, fg=textcolor, command=subScan)
    subScanButton.pack()

    window.mainloop()

def sitemap(bgcolor, textcolor):

    def find_sitemap():
        global result
        sitemaps = ["sitemap.xml", "sitemap", "sitemap.txt", "sitemap.html", "sitemap.xml.gz", "sitemap_index.xml", "sitemap.php", "sitemapindex.xml", "sitemap.gz"]
        scanDomain = domain.get()

        homepage = "https://www.{}/".format(scanDomain)

        for base in sitemaps:
            url = "https://www.{}/".format(scanDomain)+base
            failed = False
            
            try:
                json = requests.get(url, timeout=5)
                json.raise_for_status()
            except requests.exceptions.Timeout:
                print("link timed out after 5 seconds")
                failed = True
            except requests.exceptions.RequestException as e:
                failed = True

            if not failed and json.status_code == 200 and not json.history:
                result += url+"\n"
                results.write("{}\n".format(url))

                searchButton.config(text="SEARCHING...")
                label.config(text="SITEMAPS: \n"+result)

                results.flush()
                window.update()

            if not failed:
                json.close()
            
            searchButton.config(text="SEARCH")

        if result == "":
            label.config(text= "SITEMAPS: no sitemaps found")
            window.update()
    
    window = tk.Tk()

    window.title("FIND SITEMAP")
    window.geometry("200x150")
    window.configure(bg=bgcolor)

    tk.Label(window, text="DOMAIN", bg=bgcolor, fg=textcolor).pack()
    domain = tk.Entry(window, bg=bgcolor, fg=textcolor)
    domain.insert(0, "example.com")
    domain.pack()

    searchButton = tk.Button(window, text="SEARCH", bg=bgcolor, fg=textcolor, command=find_sitemap)
    searchButton.pack()

    label = tk.Label(window, text= "SITEMAPS: ", bg=bgcolor, fg=textcolor)
    label.pack()

    window.mainloop()