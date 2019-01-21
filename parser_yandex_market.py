from bs4 import BeautifulSoup
import requests
import json
import urllib.request
import datetime
import time

def get_data_json(path):
    with open(path) as data_json:
        data = json.load(data_json)
    return data


def get_find_link(data):
    parse_date_time = datetime.datetime.now().strftime("%d-%m-%Y %H:%M")
    parse_all_data = []
    for ym_link in data['ym_links']:
        time.sleep(10)
        find_link = ym_link + '/offers?lr=' + data['region']+'&local-offers-first=0&how=aprice'
        parse_link = ym_link
        parse_region = data['region']
        html1 = requests.get(find_link)
        html1.encodind = 'utf-8'
        html = html1.text
        soup = BeautifulSoup(html, 'lxml')
        try:
            product_name = soup.find('h1', class_='title').text
        except:
            product_name = ''
        top5ym_offers = parse_data(find_link)
        all_data = {'parse_link':parse_link,
                    'parse_region':parse_region,
                    'product_name':product_name,
                    'top5ym_offers':top5ym_offers}
        parse_all_data.append(all_data)
    parse_all ={'parse_date_time':parse_date_time,
                'parse_dates':parse_all_data}
    with open('output1.json', 'w') as f:
        json.dump(parse_all, f, ensure_ascii=False, indent=4)


def parse_data(find_link):
    html1 = requests.get(find_link)
    html1.encodind = 'utf-8'
    html = html1.text
    soup = BeautifulSoup(html, 'lxml')
    snip_card =soup.find_all('div', class_='n-snippet-card')
    top5ym_offers = []
    for card in snip_card[:5]:
        try:
            name = card.find('h3').text.strip()
        except:
            name = ''
        try:
            price = card.find('div', class_='price').text.strip().replace(" ", "")[:-1].strip()
        except:
            price = ''
        try:
            currency_simbol = card.find('div', class_='price').text.strip().replace(" ", "")[-1]
        except:
            currency_simbol = ''
        try:
            seller_lin = 'https:'+card.find('a').get('href')
            s_link = urllib.request.urlopen(seller_lin)
            seller_link = s_link.geturl().replace('&_openstat', ' ').replace('?utm', ' ').replace('&ymclid', ' ').split()[0]
        except:
            seller_link = ''
        data_top = {'name':name,
                'price':price,
                'currency_simbol':currency_simbol,
                'seller_link':seller_link
                }
        top5ym_offers.append(data_top)
    return top5ym_offers


def main():
    path = './input.json'
    data = get_data_json(path)
    get_find_link(data)
    

if __name__ == '__main__':
    main()