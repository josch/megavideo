#!/usr/bin/python
# -*- coding: utf8 -*-

from xml.etree.ElementTree import parse
from urllib import urlopen
import sys

if len(sys.argv) != 2:
    sys.exit("give the id as an argument")

mid = sys.argv[1]

# parse xml
doc = parse(urlopen("http://www.megavideo.com/xml/videolink.php?v="+mid))
row = doc._root._children[0]

# get variables
un = row.attrib['un']
k1 = row.attrib['k1']
k2 = row.attrib['k2']
title = row.attrib['title']
server = row.attrib['s']

# convert each hex value into binary number string, padded to length four
dlhash = list(''.join([bin(int(c, 16))[2:].rjust(4, "0") for c in un]))
rand = list()

# fill list with pseudo random numbers
for i in xrange(384):
    k1 = (int(k1)*11 + 77213)%81371
    k2 = (int(k2)*17 + 92717)%192811
    rand.append((k1+k2)%128)

# swap certain values
for i in xrange(256, -1, -1):
    j = rand[i]
    k = i%128
    tmp = dlhash[j]
    dlhash[j] = dlhash[k]
    dlhash[k] = tmp

# xor with last random number bit
for i in xrange(128):
    dlhash[i] = str(int(dlhash[i]) ^ (rand[i+256] & 1))

# split list into strings of length four
dlhash = [''.join(dlhash[i:i+4]) for i in range(0,128,4)]
# convert binary to hex
dlhash = ''.join([hex(int(c,2))[2:] for c in dlhash])

print "wget http://www"+server+".megavideo.com/files/"+dlhash+"/"+title+".flv"
