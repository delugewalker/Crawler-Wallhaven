import requests
from lxml import etree
import os
import time

path = r'E:\Pictures\PictureSites\Wallhaven\toplist-2021-01-09-1M'

for oldname in os.listdir(path):
    name = oldname.split('-')
    if len(name) == 5:
        a, b = name[4].split('.')
        newname = a + '-' + name[2] + '-' + name[3] + '.' + b
        if not os.path.exists(os.path.join(path, newname)):
            os.rename(os.path.join(path, oldname), os.path.join(path, newname))
        else:
            os.remove(os.path.join(path, oldname))


