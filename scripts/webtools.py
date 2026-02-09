import requests, threading, socket
import tkinter as tk

results = open("./data/results.txt", "w")
variations = open("./data/variations.txt", "r").read().split()

subdomain_base = "https://crt.sh/?q={}&output=json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

result = ""
resultList = []
checked = []
failed = []
foundNum = 0

printall = False

timeout = 5

def loadVariations(varations, word, bucket_variations):
    for variation in varations:
        bucket_variations.append(word+variation)
        bucket_variations.append(variation+word)
        bucket_variations.append(word+"-"+variation)
        bucket_variations.append(variation+"-"+word)

def checkBases(bucket_name, base, root, foundlabel):
    global result, foundNum

    url = base.format(bucket_name)

    checked.append({"found": len(resultList), "failed": len(failed)})
    
    if printall:
        print(url+"\n")
    
    try:
        response = requests.head(url, timeout=timeout, headers=HEADERS)  # usually 10 sec
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.Timeout:
        failed.append(url)
        return
    except requests.exceptions.RequestException as e:
        return

    if response.status_code == 200:
        print(f"[+] Public Subdomain Found: {url}")
        results.write(f"{url}\n")
        results.flush()
        
        result += url+"\n"
        resultList.append(url)
        root.update()
        response.close()
        foundNum += 1

    response.close()

    return checked, results, 

def showResults(bgcolor,textcolor):
    root = tk.Tk()
    root.geometry("500x300")

    scrollbar = tk.Scrollbar(root)
    scrollbar.pack( side = tk.RIGHT, fill=tk.BOTH)

    mylist = tk.Listbox(root,width=500, yscrollcommand = scrollbar.set)
    for index, line in enumerate(open("./data/results.txt", "r").read().split()):
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
                    if "\n" in i["name_value"]: 
                        namevalues = i["name_value"].split("\n")
                        for value in namevalues:
                            if not value in resultList and not "*" in value:
                                print(value, "\n")
                                window.update()

                                results.write("{}\n".format(value))
                                results.flush()
                        
                                result += value+"\n"
                                resultList.append(value)
                    
                    elif not i["name_value"] in resultList and not "*" in i["name_value"]:
                        print(i["name_value"], "\n")
                        window.update()

                        results.write("{}\n".format(i["name_value"]))
                        results.flush()
                
                        result += i["name_value"]+"\n"
                        resultList.append(i["name_value"])

            print(len(resultList))

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

def scrapeS3(bgcolor, textcolor):
    def start (url):
        url = f'https://{domain.get()}.s3.amazonaws.com'

        try:
            response = requests.head(url, timeout=timeout, headers=HEADERS)
            response.raise_for_status()
        except requests.exceptions.Timeout: 
            print("Request timed out.")
            return
        except requests.exceptions.RequestException as e:
            print(e)
            return

        if response.status_code == 200:
            print(response.text, response.headers, response.raw)
        else:
            print(response.status_code)
    window = tk.Tk()

    window.title("SCRAPE S3")
    window.geometry("200x75")
    window.configure(bg=bgcolor)

    tk.Label(window, text="BUCKET NAME", bg=bgcolor, fg=textcolor).pack()
    domain = tk.Entry(window, bg=bgcolor, fg=textcolor)
    domain.insert(0, "example")
    domain.pack()

    button = tk.Button(window, text="SCAN", bg=bgcolor, fg=textcolor, command=lambda url=domain.get(): start(url,))
    button.pack()

    window.mainloop()

def sitemap(bgcolor, textcolor):

    def find_sitemap():
        global result
        sitemaps = ["sitemap.xml", "sitemap", "sitemap.txt", "sitemap.html"]
        scanDomain = domain.get()

        homepage = "https://www.{}/".format(scanDomain)

        for base in sitemaps:
            url = homepage+base
            
            try:
                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
            except requests.exceptions.Timeout:
                print("Request timed out.")
                continue
            except requests.exceptions.RequestException as e:
                continue

            if response.status_code == 200 and not response.history:
                result += url+"\n"
                results.write("{}\n".format(url))

                searchButton.config(text="SEARCHING...")
                label.config(text="SITEMAPS: \n"+result)

                results.flush()
                window.update()

        try:
            response = requests.get(homepage+'/robots.txt', timeout=timeout)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            print("Request timed out.")
            return
        except requests.exceptions.RequestException as e:
            return

        if response.status_code == 200 and not response.history:
            for line in response.text.split("\n"):
                if "Sitemap:" in line:
                    if not line.split(" ")[1] in resultList:
                        url = line.split(" ")[1]
                        result += url+"\n"
                        results.write("{}\n".format(url))

                        label.config(text="SITEMAPS: \n"+result)

                        results.flush()
                        window.update()

        searchButton.config(text="SEARCH")
    
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

def reverse_ip(bgcolor, textcolor): # die van enzo is superieur dit is simpelweg een kleine variant (ik wordt niet onder druk gezet om dit te zeggen)
    def get_ip():
        response = requests.get("https://{}/".format(domain.get()))

        if response.status_code == 200:
            ip = socket.gethostbyname(domain.get())

            try:
                global result
                answer = requests.get("https://api.reverseipdomain.com/?ip={}".format(ip), timeout=timeout)
                if answer.status_code == 200:
                    for i in answer.json()["result"]:
                        result += i+"\n"
                        results.write("{}\n".format(i))

                        searchButton.config(text="SEARCHING...")
                        label.config(text="SITEMAPS: \n"+result)

                        results.flush()
                        window.update()
            except requests.Timeout:
                print("Request timed out")
        else:
            print("failed request")

    window = tk.Tk()

    window.title("REVERSE IP SEARCH")
    window.geometry("200x150")
    window.configure(bg=bgcolor)

    tk.Label(window, text="DOMAIN:", bg=bgcolor, fg=textcolor).pack()
    domain = tk.Entry(window, bg=bgcolor, fg=textcolor)
    domain.insert(0, "example.com")
    domain.pack()

    searchButton = tk.Button(window, text="SEARCH", bg=bgcolor, fg=textcolor, command=get_ip)
    searchButton.pack()

    label = tk.Label(window, text= "RESULTS: ", bg=bgcolor, fg=textcolor)
    label.pack()

    window.mainloop()
