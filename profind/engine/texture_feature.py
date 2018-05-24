# -*- coding: utf-8 -*-

import numpy as np
import scipy.misc
from skimage.filters import gabor_kernel
import multiprocessing
from skimage import color
from scipy import ndimage as ndi

"""
    Gabor filter is implemented for texture feature
"""

theta = 4
frequency = (0.1, 0.5, 0.8)
sigma = (1, 3, 5)
bandwidth = (0.3, 0.7, 1)


def make_gabor_kernel(theta, frequency, sigma, bandwidth):
    kernels = []
    for t in range(theta):
        t = t / float(theta) * np.pi
        for f in frequency:
            if sigma:
                for s in sigma:
                    kernel = gabor_kernel(f, theta=t, sigma_x=s, sigma_y=s)
                    kernels.append(kernel)
            if bandwidth:
                for b in bandwidth:
                    kernel = gabor_kernel(f, theta=t, bandwidth=b)
                    kernels.append(kernel)
    return kernels


gabor_kernels = make_gabor_kernel(theta, frequency, sigma, bandwidth)
if sigma and not bandwidth:
    assert len(gabor_kernels) == theta * len(frequency) * len(sigma), "kernel nums error in make_gabor_kernel()"
elif not sigma and bandwidth:
    assert len(gabor_kernels) == theta * len(frequency) * len(bandwidth), "kernel nums error in make_gabor_kernel()"
elif sigma and bandwidth:
    assert len(gabor_kernels) == theta * len(frequency) * (
        len(sigma) + len(bandwidth)), "kernel nums error in make_gabor_kernel()"
elif not sigma and not bandwidth:
    assert len(gabor_kernels) == theta * len(frequency), "kernel nums error in make_gabor_kernel()"


class TextureFeature(object):
    def __init__(self):
        self.name = 'texture'

    def _gabor(self, image, kernels=make_gabor_kernel(theta, frequency, sigma, bandwidth), normalize=True):
        pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

        img = color.rgb2gray(image)

        results = []
        feat_fn = self._power
        for kernel in kernels:
            results.append(pool.apply_async(self._worker, (img, kernel, feat_fn)))
        pool.close()
        pool.join()

        hist = np.array([res.get() for res in results])

        if normalize:
            hist = hist / np.sum(hist, axis=0)

        return hist.T.flatten()

    def _feats(self, image, kernel):
        '''
          arguments
            image : ndarray of the image
            kernel: a gabor kernel
          return
            a ndarray whose shape is (2, )
        '''
        feats = np.zeros(2, dtype=np.double)
        filtered = ndi.convolve(image, np.real(kernel), mode='wrap')
        feats[0] = filtered.mean()
        feats[1] = filtered.var()
        return feats

    def _power(self, image, kernel):
        """
          arguments
            image : ndarray of the image
            kernel: a gabor kernel
          return
            a ndarray whose shape is (2, )
        """
        image = (image - image.mean()) / image.std()  # Normalize images for better comparison.
        f_img = np.sqrt(ndi.convolve(image, np.real(kernel), mode='wrap') ** 2 +
                        ndi.convolve(image, np.imag(kernel), mode='wrap') ** 2)
        feats = np.zeros(2, dtype=np.double)
        feats[0] = f_img.mean()
        feats[1] = f_img.var()
        return feats

    def _worker(self, img, kernel, feat_fn):
        try:
            ret = feat_fn(img, kernel)
        except:
            ret = np.zeros(2)
        return ret

    def fire(self, image):
        """ count image histogram
        return a numpy array with size len(gabor_kernels)
        """

        if isinstance(image, np.ndarray):
            img = image.copy
        else:
            img = scipy.misc.imread(image, mode='RGB')

        hist = self._gabor(img, kernels=gabor_kernels)

        # normalize
        hist = hist / np.sum(hist, axis=0)

        return hist.flatten()
