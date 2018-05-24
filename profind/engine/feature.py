# -*- coding: utf-8 -*-

import os
from six.moves import cPickle
from profind.config import Config
from profind.engine.image_collection import ImageCollection
import dill


class Feature(object):
    def sample(self, image, cls1, cls2, feature_object):
        """ create image sample """

        idx = image.split('/')[-1]
        idx = idx.split('.')[0]
        sample_cache = '{}-{}-{}-{}'.format(feature_object.name+'-based', idx, cls1, cls2)

        try:
            samples = cPickle.load(
                open(os.path.join(Config.engine_cache_path() + '/single', sample_cache), "rb", True))
            return samples
        except:
            samples = []
            histogram = feature_object.fire(image)
            samples.append({
                'img': idx,
                'cls1': cls1,
                'cls2': cls2,
                'hist': histogram
            })

            cPickle.dump(samples,
                         open(os.path.join(Config.engine_cache_path() + '/single', sample_cache), "wb", True))

            return samples

    def samples(self, feature_object):
        """ create samples of all collection """
        db = ImageCollection()
        sample_cache = "{}-{}".format(feature_object.name+'-based', 'all-products')

        try:
            samples = cPickle.load(
                open(os.path.join(Config.engine_cache_path(), sample_cache), "rb", True))
            return samples
        except:
            samples = []

            i = 0
            data = db.get_collection()
            for d in data.itertuples():
                try:
                    cls1, cls2, img = getattr(d, "cls1"), getattr(d, "cls2"), getattr(d, "img")
                    image = Config.product_image_path()
                    if len(cls1) > 0:
                        image = image + '/' + cls1
                    if len(cls2) > 0:
                        image = image + '/' + cls2
                    image = image + '/' + img
                    samples.append(self.sample(image, cls1, cls2, feature_object))
                    i = i + 1
                    print(i)
                except:
                    continue
            with open(Config.engine_cache_path()+'/'+sample_cache, 'wb') as fp:
                dill.dump(samples, fp)

            return samples
