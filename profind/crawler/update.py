#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from profind.crawler.curl import Curl
from profind.database.mysql import MySQL


class UpdateAll(object):
    def __init__(self):
        # delay when fetching each product
        self.sleep = 1

    def update(self, mysql, product):
        url = product['ecommerce_url'] + '/' + product['link']

        curl = Curl()
        body = curl.fetch(url)
        pos = body.find("/404/")
        pos2 = body.find("hatasayfasi")
        pos3 = body.find("e=404")
        if pos > -1 or pos2 > -1 or pos3 > -1:
            mysql.removeProduct(product['id'])

    def run(self):
        """ fetch all categories with using given page and max page  """

        mysql = MySQL()
        last_product = mysql.getLastProduct()
        last_id = last_product['id']

        for i in range(1, last_id):
            id_list = [i]
            product = mysql.getProducts(id_list)
            if product:
                for row in product:
                    if row:
                        self.update(mysql, row)
                        time.sleep(1)
