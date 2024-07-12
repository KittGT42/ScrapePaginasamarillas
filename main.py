import csv
import json
import time

import requests
from bs4 import BeautifulSoup
from notifiers import get_notifier

TOKEN = '7323608342:AAE4wNHiFs9tQMFgqutKkaJmhCeM2LzL3mQ'
CHAT_ID = '324015551'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
}

params = {
    'what': 'Nutricionistas',
    'qc': 'true',
}
# headers_csv = ['Name of the business', 'Profesional phone of the busines', 'Email from the business', 'Location of '
#                                                                                                       'the business',
#                'Website']
# with open('result.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerow(headers_csv)

username = "zabutniy20"
password = "XHt7nTwPHW"
PROXY_DNS = "161.77.171.5:50100"
# username = "u85352297558c05c3-zone-custom-region-us"
# password = "u85352297558c05c3"
# PROXY_DNS = "43.159.28.126:2334"
proxy = {"https": "http://{}:{}@{}".format(username, password, PROXY_DNS)}
url = 'https://www.paginasamarillas.es/search/nutricionistas/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/1?what=Nutricionistas&qc=true'

all_done_links = []
with open('links_done.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        all_done_links.append(row['links'])


def get_website(soup):
    data_pege = soup.find('div', class_='contenedor')['data-business']
    data_to_json = json.loads(data_pege)
    result_website = data_to_json['mapInfo']['adWebEstablecimiento']
    return result_website


def get_location_of_the_business(soup):
    data_pege = soup.find('div', class_='contenedor')['data-business']
    data_to_json = json.loads(data_pege)
    result_location = data_to_json['info']['businessAddress']
    return result_location


def get_name_of_the_business(soup):
    name_of_the_business = soup.find('h1', class_='mt-3 line-fluid').text.strip()
    return name_of_the_business


def get_professional_phone_of_the_business(soup):
    data_pege = soup.find('div', class_='contenedor')['data-business']
    data_to_json = json.loads(data_pege)
    professional_phone_of_the_business = data_to_json['info']['phone']
    return professional_phone_of_the_business


def get_email_from_the_business(soup):
    data_pege = soup.find('div', class_='contenedor')['data-business']
    data_to_json = json.loads(data_pege)
    result_email = data_to_json['customerMail']
    return result_email


def get_links(link):
    links_result = []
    time.sleep(5)
    response = requests.get(link, proxies=proxy, headers=headers, params=params, timeout=10)
    # while response.status_code == 403:
    #     print('Sleep 1 min')
    #     time.sleep(60)
    #     response = requests.get(link, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'lxml')
    links_in_divs = soup.find_all('div', class_='col-xs-11 comercial-nombre')
    for link in links_in_divs:
        links_result.append(link.find('a')['href'])
    return links_result


# try
for i in range(1, 150):
    print(f'+ Processing page {i}/149')
    url = (f'https://www.paginasamarillas.es/search/nutricionistas/all-ma/all-pr/all-is/all-ci/all-ba/all-pu/all-nc/'
           f'{i}?what=Nutricionistas&qc=true')
    links_from_page = get_links(url)
    counter = 0
    for link in links_from_page:
        counter += 1
        print(f'+ Processing {counter} / {len(links_from_page)}')
        if link in all_done_links:
            print(f'Done link {link}')
        else:
            with open('links_done.csv', 'a') as f:
                f.write(link + '\n')
            time.sleep(5)
            response = requests.get(link, proxies=proxy, headers=headers, timeout=10)
            # while response.status_code == 403:
            #     print('Sleep 1 min')
            #     time.sleep(60)
            #     response = requests.get(link, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'lxml')
            try:
                name_of_business = get_name_of_the_business(soup)
            except Exception as e:
                print(f'{e} problem with name in {link}')
                name_of_business = ''
            try:
                telephone_of_business = get_professional_phone_of_the_business(soup)
            except Exception as e:
                print(f'{e} problem with telephone in {link}')
                telephone_of_business = ''
            try:
                email_of_business = get_email_from_the_business(soup)
            except Exception as e:
                print(f'{e} problem with email in {link}')
                email_of_business = ''
            try:
                location_of_business = get_location_of_the_business(soup)
            except Exception as e:
                print(f'{e} problem with location in {link}')
                location_of_business = ''
            try:
                website_of_business = get_website(soup)
            except Exception as e:
                print(f'{e} problem with website in {link}')
                website_of_business = ''
            with open('result.csv', 'a') as file:
                writer = csv.writer(file)
                writer.writerow([name_of_business, telephone_of_business, email_of_business, location_of_business,
                                 website_of_business])
# except:
#     telegram = get_notifier('telegram')
#     telegram.notify(token=TOKEN, chat_id=CHAT_ID, message='Something happened')
#     raise Exception('Something happened')
