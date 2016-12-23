#coding=utf-8
import random
proxies=[

    'http://125.88.74.122:83',
    'http://171.8.79.143:8080',
    'http://115.159.48.84:80'
]

proxy={
    'http':proxies[random.randint(0,len(proxies)-1)]
}