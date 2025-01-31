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

def checkBases(bucket_name, base, root, resultLabel):
    global result

    url = base.format(bucket_name)
    response = requests.get(url)

    checked = []
    resultList = []
    result

    checked.append(len(resultList))
    print(url+"\n")
    if response.status_code == 200:
        print(f"[+] Public Bucket Found: {url}")
        results.write(f"{url}\n")
        results.flush()
        
        result += url+"\n"
        resultList.append(url)
        resultLabel.config(text=f"RESULT: \n {result}")

        root.update()

        response.close()
    response.close()

    return checked, results, 


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