#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import time
from profind.crawler.curl import Curl
from profind.database.mysql import MySQL
from profind.config import Config
import os


class Hepsiburada(object):
    def __init__(self):

        # site id
        self.site_id = 1

        # max page
        self.max_page = 1000

        # delay when fetching each product
        self.sleep = 5

        # e-commerce site categories and our category id in database
        self.categories = {
            'yazıcı': 3,
            'telefon': 4,
            'televizyon': 5,
            'beyaz eşya': 6,
            'kamera': 7,
            'klima': 8,
            'oyun': 9,
            'bilgisayar': 2,
            'kadın,ayakkabı': 12,
            'kadın,çanta': 13,
            'kadın,bavul': 13,
            'kadın,aksesuar': 14,
            'kadın': 11,
            'erkek,ayakkabı': 17,
            'erkek,çanta': 18,
            'erkek,bavul': 18,
            'erkek,aksesuar': 19,
            'erkek': 16,
            'kitap': 20,
            'dergi': 20,
            'bisiklet': 22,
            'fitness': 23,
            'pilates': 23,
            'vücut': 23,
            'şişme su': 24,
            'av': 25,
            'kozmetik': 26,
            'bakım': 26,
            'makyaj': 26,
            'ev,mobilya': 27,
            'ev,tekstil': 28,
            'ev,dekorasyon': 29,
            'ev,banyo': 30,
            'bebek,oyuncak': 33,
            'bebek,giyim': 34,
            'kırtasiye': 38,
            'ofis': 39,
            'pet shop': 40,
        }

        # category links
        self.links = {
            'electronic': 'https://www.hepsiburada.com/bilgisayarlar-c-2147483646',
            'clothing': 'https://www.hepsiburada.com/giyim-ayakkabi-c-2147483636',
            'home': 'https://www.hepsiburada.com/ev-dekorasyon-c-60002028',
            'office': 'https://www.hepsiburada.com/kirtasiye-ofis-urunleri-c-2147483643',
            'baby': 'https://www.hepsiburada.com/anne-bebek-oyuncak-c-2147483639',
            'outdoor': 'https://www.hepsiburada.com/spor-outdoor-urunleri-c-60001546',
            'cosmetic': 'https://www.hepsiburada.com/kozmetik-kisisel-bakim-urunleri-c-60001547',
            'potshop': 'https://www.hepsiburada.com/pet-shop-c-2147483616',
        }

    def product(self, url):
        """ Get product category """
        curl = Curl()
        body = curl.fetch('https://www.hepsiburada.com/' + url)
        soup = BeautifulSoup(body, "html.parser")
        categories = soup.findAll('span', attrs={'itemprop': 'title'})
        # category path
        category = ''
        i = 0
        for c in categories:
            c = c.text.encode('utf-8').strip()
            c = c.decode('utf-8').split('/////')
            if i != 0:
                category = category + ' ' + c[0].lower()
            i = i + 1

        # find category
        for k, v in self.categories.items():
            k = k.encode('utf-8').strip()
            k = k.decode('utf-8').split(',')
            if len(k) > 1:
                pos = category.find(k[0])
                pos2 = category.find(k[1])
                if pos > -1 and pos2 > -1:
                    return v
            else:
                pos = category.find(k[0])
                if pos > -1:
                    return v

        return 0

    def category(self, url, page, image_paths, mysql):
        """ Fetch all product in given url, and insert to database """

        print('Page: ' + str(page))
        print()
        print()
        print()

        curl = Curl()
        body = curl.fetch(url)
        soup = BeautifulSoup(body, "html.parser")
        products = soup.findAll('li', attrs={'class': 'search-item'})
        for product in products:
            try:
                soup = BeautifulSoup(product.encode('utf-8'), "html.parser")
                # title
                title = soup.find('h3', attrs={'class': 'product-title'})
                title = title.get('title').encode('utf-8').strip()
                title = title.decode('utf-8').split('/////')
                title = title[0]
                # link
                link = soup.find('a')
                link = link.get('href').encode('utf-8').strip()
                link = link.decode('utf-8')
                # photo
                photo = soup.find('img', attrs={'class': 'product-image'})
                photo = photo.get('src').encode('utf-8').strip()
                photo = photo.decode('utf-8').split("/")
                photo = "https://productimages.hepsiburada.net/s/" + photo[4] + "/200/" + photo[6]
                # old price
                try:
                    old_price = soup.find('del', attrs={'class': 'product-old-price'})
                    old_price = old_price.text.encode('utf-8').strip() \
                        .decode('utf8').replace(" TL", "").replace(".", "").replace(",", ".")
                except:
                    old_price = 0
                # new price
                try:
                    new_price = soup.find('span', attrs={'class': 'product-old-price'})
                    new_price = new_price.text.encode('utf-8').strip().decode('utf8') \
                        .replace(" TL", "").replace(".", "").replace(",", ".")
                except:
                    new_price = soup.find('span', attrs={'class': 'product-price'})
                    new_price = new_price.text.encode('utf-8').strip().decode('utf8') \
                        .replace(" TL", "").replace(".", "").replace(",", ".")
                # discount
                try:
                    discount = soup.find('div', attrs={'class': 'discount-badge'})
                    soup = BeautifulSoup(discount.encode('utf-8'), "html.parser")
                    discount = soup.find('span')
                    discount = discount.text.encode('utf-8').strip().decode('utf8').replace(" TL", "")
                except:
                    discount = 0
                # currency
                currency = 'TRY'
                # category
                category_id = self.product(link)
                if category_id <= 0:
                    continue
                # image path
                image_path = image_paths[category_id]

                # insert
                product_id = mysql.insertProduct(self.site_id, category_id, title, new_price, old_price, discount,
                                                 currency, link)
                if product_id:
                    curl.download(photo, Config.product_image_path() + '/' + image_path + '/' + str(product_id) + '.jpg')

                    print('Added: ' + str(product_id))
                    print('Category: ' + str(category_id))
                    print('Image Path: ' + str(image_path))
                    if os.path.exists(Config.product_image_path() + '/' + image_path + '/' + str(product_id) + '.jpg'):
                        print('Image is added.')
                    else:
                        print('Image is not added.')
                    print('Url: ' + link)
                    print()
                    print()
                    print()

                # sleep
                time.sleep(1)
            except:
                continue

    def fetch(self, category, page=1):
        """ fetch all categories with using given page and max page  """

        page = int(page)
        mysql = MySQL()
        image_paths = mysql.getImagePaths()

        for i in range(page, self.max_page):
            url = self.links[category] + '?sayfa=' + str(i)
            self.category(url, i, image_paths, mysql)