# Bucket Bruteforcer
### A program brute forcing specific bucket types by keyword

---

## What can it do?
This program can brute force websites by keyword (For example: Slack, Atlassian, Amazon Aws buckets), there is also a subdomain scanner built in using the crt.sh servers and there is a sitemap finder by brute force.

## Requirements
- Tested on python 3.11.1 using other versions may cause errors,
- Dependencies are listed in `requirements.txt` see below:
    - Tkinter (imported as tk)
    - matplotlib.pyplot
    - ### The following libraries are included with python
    - threading
    - json

## Program use
- 1, Run v2.py
- 2, Add keywords
- 3, If using a custom url base enter into the given entry
- 4, Run by clicking the button in menubar
- 5, See results in `search` in the menubar or in `results.txt`

This is a simple description for a more detailed and technical explanation see below. V

---

# the cool part

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
* Opens a new tkinter window almost the same as "openSubScanner", 

### find_sitemap: 
* Also uses bruteforce, goes through a list of common sitemap names and adds them to the given domain name then proceeding to send a request if code 200 OK is given the domain plus sitemap name gets added to the results and written to `results.txt`,

---
## v2
>Main program, run this to start,

### loadKeywords: 
* Loops through keywords list adding them to the bucket variations and running the "loadVariations" function for each word,

### check_custom: 
* Starts a new thread for each base running the "checkBases" function in webtools, also in charge of keeping up the currentChecked variable,

### searchCustom: 
* Starts of by loading the keywords then loops through each bucket variation and makes sure there are not too many threads running at the same time, if there are it will wait untill it has dropped below the limit (this limit can be set is the tkinter GUI defaults to 250 or 150 if a noninteger is set), once the thread count is low enough it will open a new one running the "check_custom" function, finally updates all the counters in the GUI,

### addKeyword: 
* Adds the keyword in the given Entry upon click of the "add keyword" button,

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