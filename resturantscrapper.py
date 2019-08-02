from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as soup
from time import sleep
import random
import csv


CHROMEDRIVER_PATH = "C:\\Users\\Windows 10 Pro\\Downloads\\chromedriver"
browser = webdriver.Chrome(CHROMEDRIVER_PATH)


def generate_random():
  #It returns a random value between 3 and 5. That number indicates the seconds to be wait
  rand = random.randint(3, 8)
  return rand


def get_no_page():
  try:
    _page_no = browser.find_element_by_xpath(
        '//*[@id="search-results-container"]/div[2]/div[1]/div[1]/div/b[2]').text
    return(int(_page_no))
  except:
    return("cant access number of page results")

_resturant_links=[]
def extract_links(link):
  browser.get(link)
  sleep(generate_random())
  contents = soup(browser.page_source, "html.parser")
  all = contents.find_all("div", class_="content")
  for n in all:
    try:
      website = n.select(
          "a.result-title.hover_feedback.zred.bold.ln24.fontsize0")[-1]['href']
      _resturant_links.append(website)
    except:
      website = None
  

def scrape_data(links):

  browser.get(links)
  sleep(generate_random())
  http_contents = soup(browser.page_source, "html.parser")

  try:
    name = http_contents.select(
        "h1.ui.res-name.mb0.header.nowrap")[-1].text.strip()
  except:
    name= None
  try:
    address = http_contents.find_all(
      "div", class_="resinfo-icon")[0].text.strip()
  except:
    address = None

  try:
    phone = http_contents.find("span", class_="tel").text.strip()
  except:
    phone = None
  try:
    website = browser.find_element_by_xpath(
        '//*[@id="mainframe"]/div[1]/div/div[1]/div[4]/div/div[1]/div[5]/div/a').get_attribute("href")
  except:
    website = None

  csv_writer.writerow([name, address, phone, website])


url = 'https://www.zomato.com/carlinville-il/breakfast'
browser.get(url)
sleep(generate_random())
print("%s page result found" % (get_no_page()))

pages = 2  # <how many pages to scrape

csv_file = open('restuarants_leads', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Name', 'Address', 'Phonenumber', 'website'])

for n in range(1, pages+1):
  page_links = "?page=%s" % (n)
  web_url = url+page_links
  extract_links(web_url)
  sleep(generate_random())

for i in _resturant_links:
  scrape_data(i)
  sleep(generate_random())

browser.quit()
csv_file.close()
