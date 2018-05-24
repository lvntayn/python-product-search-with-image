#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import time
from profind.crawler.curl import Curl
from profind.database.mysql import MySQL
from profind.config import Config
import os


class Trendyol(object):
    def __init__(self):

        # site id
        self.site_id = 2

        # max page
        self.max_page = 3000

        # delay when fetching each product
        self.sleep = 1

        # e-commerce site categories and our category id in database
        self.categories = {
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
            'kozmetik': 26,
            'parfüm': 26,
            'bakım': 26,
            'makyaj': 26,
            'ev,mobilya': 27,
            'ev,tekstil': 28,
            'ev,dekorasyon': 29,
            'ev,banyo': 30,
            'ev': 27,
            'bebek,oyuncak': 33,
            'bebek,giyim': 34,
            'bebek,aksesuar': 35,
            'bebek': 32,
            'çocuk,oyuncak': 33,
            'çocuk,giyim': 34,
            'çocuk,aksesuar': 35,
            'çocuk': 32
        }

        # category links
        self.links = {
            'women': 'https://www.trendyol.com/kadin?siralama=6&qs=navigation',
            'men': 'https://www.trendyol.com/erkek?siralama=6&qs=navigation',
            'baby': 'https://www.trendyol.com/cocuk?siralama=6&qs=navigation',
            'home': 'https://www.trendyol.com/ev--yasam?siralama=6&qs=navigation'
        }

    def product(self, url):
        """ Get product category """
        category = url.lower()
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

    def category(self, category, url, page, image_paths, mysql):
        """ Fetch all product in given url, and insert to database """

        print('Page: ' + str(page))
        print()
        print()
        print()

        curl = Curl()
        body = curl.fetch(url)
        soup = BeautifulSoup(body, "html.parser")
        products = soup.findAll('li', attrs={'class': 'product-card-wrapper'})
        for product in products:
            try:
                soup = BeautifulSoup(product.encode('utf-8'), "html.parser")
                # title
                title = soup.find('img', attrs={'class': 'product-image'})
                title = title.get('title').encode('utf-8').strip()
                title = title.decode('utf-8').split('/////')
                title = title[0]
                # link
                link = soup.find('a', attrs={'class': 'product-detail-link'})
                link = link.get('href').encode('utf-8').strip()
                link = link.decode('utf-8')
                # photo
                photo = soup.find('img', attrs={'class': 'product-image'})
                photo = photo.get('src').encode('utf-8').strip()
                if photo.decode('utf-8') == '/Content/images/defaultThumb.jpg':
                    photo = soup.find('img', attrs={'class': 'product-image'})
                    photo = photo.get('data-original').encode('utf-8').strip()
                photo = photo.decode('utf-8').split("https://img-trendyol.mncdn.com/")
                photo = "https://img-trendyol.mncdn.com/mnresize/200/200/" + photo[1]
                # old price
                try:
                    old_price = soup.find('span', attrs={'class': 'product-market-price'})
                    old_price = old_price.text.encode('utf-8').strip() \
                        .decode('utf8').replace(" TL", "").replace(".", "").replace(",", ".")
                except:
                    old_price = 0

                # new price
                try:
                    new_price = soup.find('span', attrs={'class': 'product-sale-price'})
                    new_price = new_price.text.encode('utf-8').strip().decode('utf8') \
                        .replace(" TL", "").replace(".", "").replace(",", ".")
                except:
                    new_price = 0
                # discount
                try:
                    discount = soup.find('div', attrs={'class': 'discountBox'})
                    soup = BeautifulSoup(discount.encode('utf-8'), "html.parser")
                    discount = soup.find('span')
                    discount = discount.text.encode('utf-8').strip().decode('utf8').replace(" TL", "").replace("%", "")
                except:
                    discount = 0
                # currency
                currency = 'TRY'
                # category
                category_id = self.product(title)
                if category_id <= 0:
                    if category == 'women':
                        category_id = 11
                    elif category == 'men':
                        category_id = 16
                    elif category == 'baby':
                        category_id = 32
                    else:
                        category_id = 27

                # image path
                image_path = image_paths[category_id]

                # insert
                product_id = mysql.insertProduct(self.site_id, category_id, title, new_price, old_price, discount,
                                                 currency, link)
                if product_id:
                    curl.download(photo,
                                  Config.product_image_path() + '/' + image_path + '/' + str(product_id) + '.jpg')

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
                time.sleep(self.sleep)
            except:
                continue


    def fetch(self, category, page=1):
        """ fetch all categories with using given page and max page  """

        page = int(page)
        mysql = MySQL()
        image_paths = mysql.getImagePaths()

        for i in range(page, self.max_page):
            url = self.links[category] + '&pi=' + str(i)
            self.category(category, url, i, image_paths, mysql)


