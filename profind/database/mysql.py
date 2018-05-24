#!/usr/bin/python
# -*- coding: utf-8 -*-

import pymysql
import os
from profind.config import Config
from werkzeug.contrib.cache import SimpleCache

class MySQL(object):
    connection = False

    @staticmethod
    def conn(self):
        """ Returns cursor of MySQL connection """
        if not self.connection:
            self.connection = pymysql.connect(host=Config.databaseHost(),
                                              unix_socket=Config.databaseSocket(),
                                              user=Config.databaseUser(),
                                              passwd=Config.databasePassword(),
                                              db=Config.database(),
                                              autocommit=True,
                                              cursorclass=pymysql.cursors.DictCursor)

        return self.connection.cursor()

    def unicodeToLatin(self, name):

        # unicodes
        unicodes = [
            '\u011f', '\u011e', '\u0131', '\u0130', '\u00f6', '\u00d6', '\u00fc', '\u00dc', '\u015f',
            '\u015e', '\u00e7', '\u00c7',
        ]
        unicodes_o = [
            '{u011f}', '{u011e}', '{u0131}', '{u0130}', '{u00f6}', '{u00d6}', '{u00fc}', '{u00dc}',
            '{u015f}', '{u015e}', '{u00e7}', '{u00c7}',
        ]
        for i in range(0, len(unicodes)):
            name = name.replace(unicodes[i], unicodes_o[i])

        return name

    def latinToUnicode(self, name):

        # unicodes
        unicodes = [
            '{u011f}', '{u011e}', '{u0131}', '{u0130}', '{u00f6}', '{u00d6}', '{u00fc}', '{u00dc}',
            '{u015f}', '{u015e}', '{u00e7}', '{u00c7}',
        ]
        unicodes_o = [
            'ğ', 'Ğ', '{u0131}', 'ı', 'ö', 'Ö', 'ü', 'Ü', 'ş', 'Ş', 'ç', 'Ç',
        ]
        for i in range(0, len(unicodes)):
            name = name.replace(unicodes[i], unicodes_o[i])

        return name

    def insertProduct(self, ecommerce_site_id, category_id, name, price, old_price, discount, currency, link):
        """ Insert product """
        try:
            product = self.getProduct(link)
            if product:
                self.updateProduct(ecommerce_site_id, category_id, name, price, old_price, discount, currency, link)
                return product['id']
            else:
                name = self.unicodeToLatin(name)
                with MySQL.conn(MySQL) as cursor:
                    sql = ("INSERT INTO `products` (ecommerce_site_id, "
                           "category_id, name, price, "
                           "old_price, discount, currency, link) VALUES "
                           "('" + str(ecommerce_site_id) + "', '" + str(category_id) + "', '" + str(name) + "', '" + str(
                        price) + "', '" + str(old_price) + "', '" + str(discount) + "', '" + str(currency) + "', '" + str(
                        link) + "');")
                    cursor.execute(sql)
                    return cursor.lastrowid
        except:
            return False

    def updateProduct(self, ecommerce_site_id, category_id, name, price, old_price, discount, currency, link):
        """ Insert product """
        try:
            name = self.unicodeToLatin(name)
            with MySQL.conn(MySQL) as cursor:
                sql = ("UPDATE `products` SET "
                        "ecommerce_site_id = '" + str(ecommerce_site_id) + "', "
                        "category_id = '" + str(category_id) + "', "
                        "name = '" + str(name) + "', "
                        "price = '" + str(price) + "', "
                        "old_price = '" + str(old_price) + "', "
                        "discount = '" + str(discount) + "', "
                        "currency = '" + str(currency) + "', "
                        "updated_at = CURRENT_TIMESTAMP "
                        "WHERE link='"+link+"'")
                cursor.execute(sql)
        except:
            return False

    def removeProduct(self, id):
        try:
            with MySQL.conn(MySQL) as cursor:
                sql = ("DELETE FROM `products` WHERE id="+str(id))
                cursor.execute(sql)
        except:
            return False

    def getProduct(self, link):
        """ Get product with link """
        try:
            with MySQL.conn(MySQL) as cursor:
                sql = ("SELECT * FROM `products` WHERE link = '" + link + "' ORDER BY id ASC LIMIT 1")
                cursor.execute(sql)
                for row in cursor:
                    if row:
                        return row
                return False
        except:
            return False

    def getLastProduct(self):
        """ Get old product """
        try:
            with MySQL.conn(MySQL) as cursor:
                sql = ("SELECT * FROM `products` WHERE id > 0 ORDER BY id DESC LIMIT 1")
                cursor.execute(sql)
                for row in cursor:
                    if row:
                        return row
                return False
        except:
            return False

    def getProducts(self, id_list):
        """ Get products """
        try:
            if len(id_list) == 1:
                id_list = str(id_list[0])
            else:
                id_list = ', '.join(id_list)
            with MySQL.conn(MySQL) as cursor:
                sql = ("SELECT products.*, ecommerce_sites.name AS ecommerce_name, "
                       "ecommerce_sites.url AS ecommerce_url FROM `products` INNER JOIN ecommerce_sites "
                       "ON products.ecommerce_site_id=ecommerce_sites.id WHERE products.id IN (" + id_list + ")")
                cursor.execute(sql)
                return cursor
        except:
            return False

    def getImagePaths(self, create=True):
        cache = SimpleCache()
        if not create:
            rv = cache.get('image-paths')
            if rv is not None:
                return rv
        try:
            with MySQL.conn(MySQL) as cursor:
                categories = {}
                sql = "SELECT id, category_id, alias FROM `categories` WHERE id > 0 ORDER BY id ASC"
                cursor.execute(sql)
                for row in cursor:
                    idx = row['id']
                    category_id = row['category_id']
                    alias = row['alias']
                    if category_id == 0:
                        categories[idx] = alias
                    else:
                        categories[idx] = categories[category_id] + '/' + alias
                    if create:
                        if not os.path.exists(Config.product_image_path() + '/' + categories[idx]):
                            os.makedirs(Config.product_image_path() + '/' + categories[idx])

                cache.set('image-paths', categories, timeout=60*60*24*365)
                return categories
        except:
            return False

