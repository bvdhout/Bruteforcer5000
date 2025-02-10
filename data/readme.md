# Bucket Bruteforcer
### A program brute forcing specific bucket types by keyword

---

## What can it do?
- [x] Brute force buckets or any website like slack or atlassian
- [x] Scan subdomains using crt.sh servers
- [x] Brute force sitemaps
- [x] Switch between super awesomesauce themes
- [x] Do a reverse ip scan on any domain
- [ ] Make a sandwich
- [ ] Dominate the world
- [ ] Order a pizza 
- [ ] Outrun the immortal snail

This program can brute force websites by keyword (For example: Slack, Atlassian, Amazon Aws buckets), there is also a subdomain scanner built in using the crt.sh servers, a sitemap finder by brute force and a reverse ip scanner that works by domain

## Requirements
- Tested on python 3.11.1 using other versions may cause errors,
- Internet connection is also needed to run any of the functions (except for the themes)
- Dependencies can be found in `requirements.txt` or see below:
    - `tkinter` (imported as tk)
    - `matplotlib`
    - **The following libraries are included with python**
    - `threading`
    - `requests`
    - `socket`
    - `json`



## Program use
1. Use the terminal to install dependencies
2. Run v2.py
3. Add keywords if needed
4. If using a custom url base enter into the given entry
5. Run by clicking the `search` button in the menubar and clicking on the appropriate command
6. See results in `search` in the menubar or in `results.txt` or use any of the functions in the unrelated tab under the settings

This is a simple description of my program for a more detailed and technical explanation see below. V

---

# The cool part

## GUIHandler
>Starts GUI and takes care of the themes and graph,

### ChangeTheme: 
* Updates bgcolor and textcolor variables to desired theme then loops through each widget to update it,

### startGUI: 
* Creates all the widgets and the main window, this function is called from v2.py and returns all widgets,

### plotGraph: 
* Takes the checked items and shows the existing links found over time,

---
## webtools
>Has all requests related functions,

### loadVariations: 
* Goes through each variation stored in `variations.txt` and adds it to the keyword in a few different ways,

### checkBases: 
* Uses requests to check all of the variations created in "loadVariations" with the given url, when a code 200 OK returns the url gets added to the results and also gets written in `results.txt`,

### showResults: 
* Creates a simple tkinter window with a scrollbar showing each result,

### openSubScanner: 
* Opens the window for the subdomain scanner including an entry to enter the domain name to search,

### subScan: 
* Sends a request crt.sh with the given domain name, reads the returned json for each subdomain,

### sitemap: 
* Opens a new tkinter window almost the same as `openSubScanner()`, 

### find_sitemap: 
* Also uses bruteforce, goes through a list of common sitemap names and adds them to the given domain name then proceeding to send a request if code 200 OK is given the domain plus sitemap name gets added to the results and written to `results.txt`,

### reverse_ip:
* Does the same as `sitemap()` and `openSubScanner()`

### get_ip:
* Uses `socket` to get the ip adress of the given domain name then proceeds to send a request to `https://api.reverseipdomain.com/` with the ip adress returned by socket, it proceeds to filter through the json response writing all results to `results.txt` and the GUI

---
## v2
>Main program, run this to start,

### loadKeywords: 
* Loops through keywords list adding them to the bucket variations and running the "loadVariations" function for each word,

### check_custom: 
* Starts a new thread for each base running the "checkBases" function in webtools, also in charge of keeping up the currentChecked variable,

### searchCustom: 
* Starts of by loading the keywords then loops through each bucket variation and makes sure there are not too many threads running at the same time, if there are it will wait untill it has dropped below the limit (this limit can be set is the tkinter GUI defaults to 250 or 150 if something else than an integer is set), once the thread count is low enough it will open a new one running the "check_custom" function, finally updates all the counters in the GUI,

### addKeyword: 
* Adds the keyword in the given Entry to the `keywords` list upon click of the "add keyword" button,

---
## unrelated
>Takes care of the caesar shift window, decrypting and encrypting,

### openDecypher: 
* Opens a tkinter window with a ceasar shift decypherer,

### decrypt: 
* Goes through each character of the Entry given by the "openDecypher" function shifting them by the amount entered by user, finally returning the finished string where every character has shifted the right amount.

---
## txt files
>For easy access storage and settings,

### keywords.txt: 
* Store default keywords here, these load into the program upon starting, although keywords can ofcourse also be added the the program itself,

### variations.txt: 
* Stores exactly 957 variations for each keyword making sure it tries as many possible links.


### results.txt: 
* Final results get written into this file, does get cleared upon starting the program,

### bases.txt: 
* All bases for buckets can be added in here currently only stores 2 (googleapis and amazonaws),

---
## json file
>Currently only one to store the themes,

### themes.json:
* Stores every theme in a quickly editable list, can also be added on to easily.