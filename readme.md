# Bruteforcer 5000
### A program brute forcing specific urls/subdomains by keyword

---

## What can it do?
- [x] Brute force buckets or any website like slack or atlassian
- [x] Scan subdomains using crt.sh servers
- [x] Brute force sitemaps
- [x] Switch between and create super awesomesauce themes
- [x] Do a reverse ip scan on any domain
- [ ] Make a sandwich
- [ ] Dominate the world
- [ ] Order a pizza 

>This program can brute force websites by keyword (For example: Slack, Atlassian, Amazon Aws buckets), there is also a subdomain scanner built in using the crt.sh servers, a sitemap finder by brute force and a reverse ip scanner that works by domain

## Requirements
- Tested on python 3.11.1 using other versions may cause errors,
- Internet connection is also needed to run any of the functions (except for the themes)
- Dependencies can be found in `requirements.txt` or see below:
    - `tkinter`
    - `matplotlib`
    - `simplejson`

## Program use
1. Use the terminal to install dependencies
2. Change/Add keywords to `data/keywords.txt`
2. Run v2.py
3. Add more keywords in the GUI if needed
4. If using a custom url base enter into the given entry
5. Run by clicking the `search` button in the menubar and clicking on the appropriate command and then pressing `scan` 
6. See results in `search` in the menubar or in `data/results.txt`, or use any of the functions in the unrelated tab under the settings

---

> This program is not meant for malicious intents. If used for such cases the author is in no way liable

## Licence
See LICENSE file.

## LEGAL
See LEGAL file.
