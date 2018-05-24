# Python - Product Search Engine With Image

## Introduction
> The product search engine(Profind) is the mobile application that automatically collects prices and images of products in shopping sites, and it provides easier tool to find similar products of uploaded images by users.

> Demo Pages - https://github.com/lvntayn/react-native-search-with-image/tree/master/demo

> Mobile Application - https://github.com/lvntayn/react-native-search-with-image

## Features
- Similarity comparison of product images
- Collects products from hepsiburada, trendyol and markafoni
- Stores product meta information in database
- Stores product images in server
- 4 image feature extraction method are implemented

## Installation
Edit profind/config.py file and import db/profind.sql to database
```bash
git clone https://github.com/lvntayn/python-product-search-with-image.git profind
cd profind
python profind.py
```

## Crawler
> Crawler is a generic term for any program (such as a robot or spider) used to automatically discover and scan websites by following links from one webpage to another. Google (n.d.). Profind crawler walks through pre-defined e-commerce sites and stored the meta information and photos of the products there on the Profind server.

```bash
python crawler.py {integration_name} {category_name} {initial_page}
```
- integration_name: integration class name. ex: Hepsiburada
- category_name: category of integrated site. ex: electronic, clothing
- initial_page: initial page of integrated site. ex: 1
- If crawler is required to update all stored products, it is enough “python crawler.py update” to run it.

## Engine
> Engine returns search requests from the mobile application and finds the most similar products to the uploaded photo and returns products that are in response to search requests. Content based Image Retrieval (CBIR) algorithm is used for visual comparison of images of the products in the database. A content-based image retrieval forms the data contained in picture information and makes an deliberation of its substance in terms of visual traits. Any inquiry operations bargain exclusively with this deliberation instead of with the picture itself. In this way, each picture embedded into the database is analyzed, and a compact representation of its substance is put away in a include vector, or signature.

```bash
python evalutation.py
```

Implemented Feature Extraction Methods: 
- Color Based Feature Extraction (RGB Histogram)
- Texture Based Feature Extraction (Gabor Filters)
- Shape Based Feature Extraction (HOG)
- Deep Learning Method (VGG 19)


## Authors
**lvntayn**
- https://github.com/lvntayn
