import requests
import xml.etree.ElementTree as ET
from itertools import product

# Keywords for generating bucket names dynamically
bucket_keywords = ["donald", "duck", "heineken", "dpg", "dev", "media", "static"]

# Keywords for filtering file names inside the bucket
file_keywords = ["donaldduck", "file", "duckworld"]

# Generate possible bucket names
bucket_names = [f"{a}-{b}" for a, b in product(bucket_keywords, bucket_keywords)]

aws_url_template = "https://{}.s3.amazonaws.com/"

def check_s3_bucket(bucket_name):
    url = aws_url_template.format(bucket_name)
    response = requests.get(url)

    if response.status_code == 200:
        print(f"[+] Public Bucket Found: {url}")
        parse_and_filter_files(response.text, bucket_name, url)
    elif response.status_code == 403:
        print(f"[-] Bucket exists but is private: {url}")
    elif response.status_code == 404:
        print(f"[*] Bucket does not exist: {url}")

def parse_and_filter_files(xml_data, bucket_name, bucket_url):
    try:
        root = ET.fromstring(xml_data)
        files = [obj.find("Key").text for obj in root.findall(".//Contents")]

        # Filter files by keywords
        filtered_files = [f for f in files if any(kw.lower() in f.lower() for kw in file_keywords)]

        if filtered_files:
            print(f"  >>> Matching Files in {bucket_name}:")
            for file in filtered_files:
                print(f"      - {bucket_url}/{file}")
        else:
            print(f"  >>> No matching files found in {bucket_name}.")
    except ET.ParseError:
        print("  >>> Could not parse bucket contents (possibly empty or restricted).")

# Run the scanner
for bucket in bucket_names:
    check_s3_bucket(bucket)
