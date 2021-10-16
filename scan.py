import requests
from bs4 import BeautifulSoup
import ast
from alive_progress import alive_bar
import xlrd
import pandas as pd

# Load IPs
ip_list = []
rapid_lookup_data = {}
loc = input("Welcome to Rapid IP Lookup. Enter a filename or location to begin: ")

wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
 
for i in range(sheet.nrows):
    ip = sheet.cell_value(i, 0)
    ip_list.append(ip.replace(" ",""))

# Scrape data
print("Scraping Scamalytics data...for free!")
x = 0
with alive_bar(len(ip_list)) as bar:
	for ip in ip_list:
		scrape_info = []
		page = requests.get(f'https://scamalytics.com/ip/{ip_list[x]}')
		soup = BeautifulSoup(page.text, 'html.parser')
		scraped_page = soup.find_all('td')
		for td in scraped_page:
			scrape_info.append(td.text)
		if scrape_info[14] == "Open":
			rapid_lookup_data[ip_list[x]] = scrape_info[2], scrape_info[5], scrape_info[21], scrape_info[22], scrape_info[23], scrape_info[24], scrape_info[25], scrape_info[26]
		elif scrape_info[14] == "Closed":
			rapid_lookup_data[ip_list[x]] = scrape_info[2], scrape_info[5], scrape_info[21], scrape_info[22], scrape_info[23], scrape_info[24], scrape_info[25], scrape_info[26]
		else:
			rapid_lookup_data[ip_list[x]] = scrape_info[2], scrape_info[5], scrape_info[15], scrape_info[16], scrape_info[17], scrape_info[18], scrape_info[19], scrape_info[20]
		bar()
		x = x + 1

# Write data
print("Writing data to file... ")
df = pd.DataFrame.from_dict(rapid_lookup_data, orient='index', columns=['ISP', 'Country', 'Anonymizing VPN', 'Tor Exit Node', 'Server', 'Public Proxy', 'Web Proxy', 'Search Engine Robot'])
file_name = "scamalytics_data.xlsx"
df.to_excel(file_name)
print('Done!')


