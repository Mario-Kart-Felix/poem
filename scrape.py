"""
double check:
    sql database.ext == mdf
breaks:
    missing comma:
        ea interchange format_3
        matlab
    extra comma:
        Huskygram, Poem, or Singer embroidery
dupes:
    BZ2
    SXC
"""

import os, json

from bs4 import BeautifulSoup
from sl4ng import show, pop, getsource, regenerator, multisplit, flat
import requests, pyperclip as pc

"Description,Header (hex),Extension,FileClass,Header_offset,Trailer (hex)"
def scrapetxt(path):
    with open(path, 'r') as fob:
        for line in fob.readlines():
            # print(line)
            yield line.strip().split(',')


    

def by_ext(path):
    d = {}
    for data in scrapetxt(path):
        desc, head, ext, kind, offset, tail = data
        d[ext] = {
            'offset': int(offset),
            'head': [int(i, 16) for i in head.split()],
            'tail': ([int(i, 16) for i in head.split()], [])['null' in tail],
            'kind': kind,
            'desc': desc,
        }
    return d




if __name__ == '__main__':
    path = r'.\FileSigs_20200424-gary_version\file_sigs_RAW.txt'
    name = 'magic_numbers-by_ext.json'
    with open(name, 'w') as fob:
        json.dump(by_ext(path), fob, sort_keys=True)
        os.startfile(name)
    
    be = by_ext(path)
    m = regenerator(flat(map(multisplit('|'), be)))
    duped = filter(lambda x: m.count(x) > 1, m)
    duped = {
        i: [be[key]['head'] for key in be if i in key] for i in duped
    }
    for key, val in duped.items():
        if all(val.count(i)==len(val) for i in val):
            print(key)
            
    
