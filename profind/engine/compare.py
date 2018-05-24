# -*- coding: utf-8 -*-
import numpy as np

from profind.config import Config
from profind.engine.feature import Feature


class Compare(object):
    def distance(self, hist1, hist2):
        return np.sum(np.absolute(hist1 - hist2))

    def find(self, img, cls1, cls2, feature_object):
        """ Find similar images """
        depth = Config.compareDepth()

        feature = Feature()
        query = feature.sample(img, cls1, cls2, feature_object)
        query = query[0]

        result = []
        samples = feature.samples(feature_object)
        for sample in samples:
            sample = sample[0]
            result.append({
                'idx': sample['img'],
                'cls1': sample['cls1'],
                'cls2': sample['cls2'],
                'dis': self.distance(query['hist'], sample['hist'])
            })

        result = sorted(result, key=lambda x: x['dis'])
        if depth and depth <= len(result):
            result = result[:depth]

        return result
