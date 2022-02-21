import requests 
from bs4 import BeautifulSoup
from lxml import etree
import csv


def get_all_text():
	url = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html'
	#url2 = 'https://zakupki.gov.ru/epz/order/extendedsearch/results.html?searchString=&morphology=on&search-filter=%D0%94%D0%B0%D1%82%D0%B5+%D1%80%D0%B0%D0%B7%D0%BC%D0%B5%D1%89%D0%B5%D0%BD%D0%B8%D1%8F&pageNumber=%d&sortDirection=false&recordsPerPage=_10&showLotsInfoHidden=false&savedSearchSettingsIdHidden=&sortBy=UPDATE_DATE&fz44=on&fz223=on&af=on&ca=on&pc=on&pa=on&placingWayList=&selectedLaws=&priceFromGeneral=&priceFromGWS=&priceFromUnitGWS=&priceToGeneral=&priceToGWS=&priceToUnitGWS=&currencyIdGeneral=-1&publishDateFrom=&publishDateTo=&applSubmissionCloseDateFrom=&applSubmissionCloseDateTo=&customerIdOrg=&customerFz94id=&customerTitle=&okpd2Ids=&okpd2IdsCodes=&gws=' % (page)
	r = requests.get(url)
	return r.text

def contain_price(soup):
	price_list = soup.find('div', {'class': 'price-block__value'}).text
	return price_list

def contain_number(soup):
	number_list = soup.find('div', {'class': 'registry-entry__header-mid__number'}).text
	return number_list

def contain_cards(text):
	soup = BeautifulSoup(text)
	card_list = soup.find_all('div', {'class': 'search-registry-entry-block box-shadow-search-input'})
	return card_list

def filter_text(text):
	text = text.split()
	if text[0].isnumeric():
		text.pop()
	else:
		text.pop(0)
	text = ''.join(text)
	text = text.replace(',','.')
	return text

to_parse = get_all_text()
cards = contain_cards(to_parse)  

fields = ['number', 'price']
rows = []
for card in cards:
	number = filter_text(contain_number(card))
	price = filter_text(contain_price(card))
	rows.append([number, price])

print(rows)
filename = "results.csv"
csvfile = open(filename, "w", encoding= 'UTF-8')
csvwriter = csv.writer(csvfile)

csvwriter.writerow(fields)
csvwriter.writerows(rows)


