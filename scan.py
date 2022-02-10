from alive_progress import alive_bar
import pandas as pd
import re

# Load IPs
rapid_lookup_data = {}
loc = input("Enter a filename or location to begin: ")

with open(loc) as f:
	ip_list = [line.rstrip() for line in f]

# Scrape data
print("Retrieving Scamalytics data...for free!")

x = 0

with alive_bar(len(ip_list)) as bar:
	for ip in ip_list:
		# Retrieve table
		df = pd.read_html(f'https://scamalytics.com/ip/{ip_list[x]}')
		dataframe_result = df[0]

		# Convert DF to list of lists
		isp = dataframe_result.query('Operator=="ISP Name"').values.tolist()
		country = dataframe_result.query('Operator=="Country Name"').values.tolist()
		anonymizing_vpn = dataframe_result.query('Operator=="Anonymizing VPN"').values.tolist()
		server = dataframe_result.query('Operator=="Server"').values.tolist()
		tor_exit_node = dataframe_result.query('Operator=="Tor Exit Node"').values.tolist()
		public_proxy = dataframe_result.query('Operator=="Public Proxy"').values.tolist()
		web_proxy = dataframe_result.query('Operator=="Web Proxy"').values.tolist()
		search_engine_robot = dataframe_result.query('Operator=="Search Engine Robot"').values.tolist()

		# Retrieve list from converted list of lists
		embedded_isp_list = isp[0]
		embedded_country_list = country[0]
		embedded_vpn_list = anonymizing_vpn[0]
		embedded_server_list = server[0]
		embedded_tor_list = tor_exit_node[0]
		embedded_public_proxy_list = public_proxy[0]
		embedded_web_proxy_list = web_proxy[0]
		embedded_search_engine_robot_list  = search_engine_robot[0]

		# Retrieve result from embedded list
		isp_result = embedded_isp_list[1]
		country_result = embedded_country_list[1]
		vpn_result = embedded_vpn_list[1]
		vps_result = embedded_server_list[1]
		tor_result = embedded_tor_list[1]
		public_proxy_result = embedded_public_proxy_list[1]
		web_proxy_result = embedded_web_proxy_list[1]
		search_engine_robot_result = embedded_search_engine_robot_list[1]
			
		rapid_lookup_data[ip_list[x]] = isp_result, country_result, vpn_result, vps_result, tor_result, public_proxy_result, web_proxy_result, search_engine_robot_result

		bar()

		x = x + 1

# Write data
print("Writing data to file... ")
df = pd.DataFrame.from_dict(rapid_lookup_data, orient='index', columns=['ISP', 'Country', 'Anonymizing VPN', 'Server', 'Tor Exit Node', 'Public Proxy', 'Web Proxy', 'Search Engine Robot'])
file_name = "scamalytics_data.xlsx"
df.to_excel(file_name)
print('Done!')
