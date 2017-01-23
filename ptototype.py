#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup
import mechanize
import time
import hashlib
import re
import base64


def getMobilePhone():
    url = 'http://uae.souq.com/ae-en/mobile-phone/l/'
    openUrl = requests.get( url )
    openrawdata = openUrl.content
    opensoup = BeautifulSoup( openrawdata )

    urls = []

    for l in opensoup.findAll('li', {'class':'columns'}):
        url = l.find('h6',{'class':'result-item-title'}).find('a').get('href')
        urls.append(url)
    return urls

urls = getMobilePhone()

def getProductDetails(url):
    openUrl = requests.get( url )
    openrawdata = openUrl.content
    opensoup = BeautifulSoup( openrawdata )

    data = []

    title = opensoup.find('div', {'class':'product-title'}).find('h1')
    desc = opensoup.find('div', {'id':'description-full'}).find('p')
    price = opensoup.find('h3', {'class':'price'}).text

    brandCategory = []
    for i in opensoup.findAll('div', {'class':'small-12 columns product-title'}):
         data = {
            'brand':i.find('span').findAll('a')[0].text,
            'category':i.find('span').findAll('a')[1].text
         }
         brandCategory.append(data)


    info = []
    
    for c in opensoup.findAll('div', {'class':'level-1 item-connection'}):
        i = c.find('span', {'class':'value'}).text
    data = {
        'color':i[0],
        'ram':i[1]
    }
    info.append(data)
    print info

    images = []
    for i in opensoup.findAll('div', {'class':'img-bucket'}):
        image = i.find('img').get('src')
        if 'http://cf1.s3.souqcdn.com/public/style/img/blank.gif' in image:
            pass
        else:
            images.append( i.find('img').get('src') ) 


    product = {
        'title':title.text,
        'desc':desc.text,
        'price':price
    }
    #data.append(product)

    return product

getProductDetails(urls[0])

# productData = []

# for i in range(len(urls)):
#     productData.append( getProductDetails(urls[i]) )
# print productData
