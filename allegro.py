# -*- coding: utf-8 -*-
import time
import psycopg2
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

'''User interaction to set the url variable'''
#url = raw_input("Paste your URL here: ")

'''Uncomment to use the URL test variable'''
url="https://allegro.pl/listing?string=windows&order=m&bmatch=ss-base-relevance-floki-5-nga-hcp-wp-ele-1-1-0329"

'''---Custom functions definition area---'''
#: Receives a url and opens it into the browser
def goToUrl(url, browser):
	print("Opening the URL: " + url)
	browser.get(url)
'''---end Custom function definition area---'''

'''---Firefox browser settings---'''
browser = webdriver.Firefox()
browser.set_window_size(1024, 768)
goToUrl(url, browser)
#delay = 3 # seconds
'''---end Firefox browser settings---'''

'''---DB connection settings---'''
print('Connecting to the PostgreSQL database...')
conn = psycopg2.connect(host="localhost", database="glassdoor", user="scraper", password="scraper") #SQL connection details
curs = conn.cursor() #cursor initialization
'''---end DB connection settings---'''

'''---Variables declaration area---'''
i = 1 #page counter
pages_remaining = True #pagination loop sentinel
'''---end Variables declaration area---'''
 
'''---Scraper logic area---'''
while pages_remaining:
	mains = browser.find_elements_by_class_name('_433675f')
	print "Processing page ", i
	for main in mains:
		product = [] #array that contains all the product detail
		url_element=main.find_element_by_xpath('.//h2/a')
		name=url_element.text
		url=url_element.get_attribute('href')
		#print url
		#print name
		product.append(name) #array id 0
		product.append(url) #array id 1
		try:
			#state=main.find_element_by_xpath('.//span[contains(text(),"Używany")]').text
			status=main.find_element_by_xpath('.//div[@class="bec3e46"]/dl/dd/span').text
			#print status
			product.append(status) #array id 2
		except:
			#print "Product Status: null"
			product.append("null") #array id 2
		try:
			#state=main.find_element_by_xpath('.//span[contains(text(),"Używany")]').text
			version=main.find_element_by_xpath('.//div[@class="bec3e46"]/dl/dd[2]/span').text
			#print version
			product.append(version) #array id 3
		except:
			#print "Version: null"
			product.append("null") #array id 3
		try:
			price=main.find_element_by_xpath('.//div[@class="ae47445 "]').text
			#print price
			product.append(price) #array id 4
		except:
			#print "Price: null"
			product.append("null") #array id 4
		try:
			sold_items=main.find_element_by_xpath('.//div[3]/span/strong').text
			#print sold_items
			product.append(sold_items) #array id 5
		except:
			#print "Sold Items: null"
			product.append("null") #array id 5
		try:
			installments=main.find_element_by_xpath('.//div[@class="_8c4d8c1"]').text
			#print installments
			product.append(installments) #array id 6
		except:
			#print "Installments: null"
			product.append("null") #array id 6
		try:
			vendor_status=main.find_element_by_xpath('.//div[@class="_1dfbbae"]/span[2]').text
			#print vendor_status
			product.append(vendor_status) #array id 7
		except:
			#print "Vendor Status: null"
			product.append("null") #array id 7
		data = (product[0], product[2], product[3], product[4], product[5], product[6], product[7], product[1])
		#product.append({'url': url, 'state': state, 'price': price, 'pippo': pippo, 'pluto': pluto})
		sql = "INSERT INTO allegro1(s1_pname, s1_pstatus, s1_pversion, s1_price, s1_psold, s1_installments, s1_vstatus, s1_url) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
		curs.execute(sql, data)
		conn.commit() #commit the sql insert
		del product[:] #deletes the list in order to free memory
	try:
		#Checks if there are more pages with links
		paginator = browser.find_element_by_class_name('next')
		next_link=paginator.find_element_by_xpath('.//a')
		next_link.click()
		time.sleep(15)
		i+=1
	except:
		pages_remaining = False
'''---end Scraper logic area---'''

'''---Finalization processes---'''
curs.close()
conn.close()
#browser.quit()
'''---end Finalization processes---'''
