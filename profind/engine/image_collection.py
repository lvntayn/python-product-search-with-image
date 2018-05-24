# -*- coding: utf-8 -*-

from profind.config import Config
import os
import pandas as pd


class ImageCollection(object):
    def __init__(self):
        self.product_path = Config.product_image_path()
        self.collection_csv_path = Config.image_collection_path()
        self.set_collection()
        self.collection = pd.read_csv(self.collection_csv_path)

    def set_collection(self, force=False):
        """ creates CSV collection file """
        if os.path.exists(self.collection_csv_path) and not force:
            return

        with open(self.collection_csv_path, 'w', encoding='UTF-8') as f:
            product_path_length = len(self.product_path.split('/'))
            f.write("cls1,cls2,img")
            for root, _, files in os.walk(self.product_path, topdown=False):
                img_class = root.split('/')
                if len(img_class) == product_path_length:
                    img_class1 = img_class[-1]
                    img_class2 = ''
                else:
                    img_class1 = img_class[-2]
                    img_class2 = img_class[-1]
                for name in files:
                    if not name.endswith('.jpg'):
                        continue
                    f.write("\n{},{},{}".format(img_class1, img_class2, name))

    def get_collection(self):
        """ get collection """
        return self.collection

    def get_length(self):
        """ get colection length """
        return len(self.collection)
