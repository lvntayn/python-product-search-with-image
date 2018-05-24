# -*- coding: utf-8 -*-

import numpy as np
import scipy.misc
from skimage.feature import hog
from skimage import color


"""
    HOG is implemented for shape feature
"""


class ShapeFeature(object):
    def __init__(self):
        self.name = 'shape'

    def _HOG(self, img, n_bin):
        image = color.rgb2gray(img)
        fd = hog(image, orientations=8, pixels_per_cell=(2,2), cells_per_block=(1,1), block_norm='L2-Hys')
        bins = np.linspace(0, np.max(fd), n_bin + 1, endpoint=True)
        hist, _ = np.histogram(fd, bins=bins)

        hist = np.array(hist) / np.sum(hist)

        return hist

    def fire(self, image):
        """ count image histogram
        return a numpy array with size 10 * 6 * 6
        """

        if isinstance(image, np.ndarray):
            img = image.copy
        else:
            img = scipy.misc.imread(image, mode='RGB')

        height, width, channel = img.shape

        hist = np.zeros((6, 6, 10))
        height_slice = np.around(np.linspace(0, height, 7, endpoint=True)).astype(int)
        width_slice = np.around(np.linspace(0, width, 7, endpoint=True)).astype(int)

        for hs in range(len(height_slice) - 1):
            for ws in range(len(width_slice) - 1):
                # slice image to region
                img_r = img[height_slice[hs]:height_slice[hs + 1], width_slice[ws]:width_slice[ws + 1]]
                hist[hs][ws] = self._HOG(img_r, 10)

        # normalize
        hist /= np.sum(hist)
        return hist.flatten()