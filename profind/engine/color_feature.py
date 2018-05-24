# -*- coding: utf-8 -*-

import numpy as np
import scipy.misc
import itertools


class ColorFeature(object):
    def __init__(self):
        self.name = 'color'

    def count_histogram(self, image, bins, channel):
        img = image.copy()
        # permutation of bins
        bins_idx = {key: idx for idx, key in
                    enumerate(itertools.product(np.arange(12), repeat=channel))}
        hist = np.zeros(12 ** channel)

        # cluster every pixels
        for idx in range(len(bins) - 1):
            img[(image >= bins[idx]) & (image < bins[idx + 1])] = idx

        # add pixels into bins
        height, width, _ = img.shape
        for h in range(height):
            for w in range(width):
                b_idx = bins_idx[tuple(img[h, w])]
                hist[b_idx] += 1

        return hist

    def fire(self, image):
        """ count image color histogram
        return a numpy array with size 3 * 3 * (12 ** channel)
        """

        if isinstance(image, np.ndarray):
            img = image.copy
        else:
            img = scipy.misc.imread(image, mode='RGB')

        height, width, channel = img.shape

        # slice bins equally for each channel
        bins = np.linspace(0, 256, 13, endpoint=True)

        hist = np.zeros((3, 3, 12 ** channel))
        height_slice = np.around(np.linspace(0, height, 4, endpoint=True)).astype(int)
        width_slice = np.around(np.linspace(0, width, 4, endpoint=True)).astype(int)

        for hs in range(len(height_slice) - 1):
            for ws in range(len(width_slice) - 1):
                # slice image to region
                img_r = img[height_slice[hs]:height_slice[hs + 1], width_slice[ws]:width_slice[ws + 1]]
                hist[hs][ws] = self.count_histogram(img_r, bins, channel)

        # normalize
        hist /= np.sum(hist)
        return hist.flatten()