#!/usr/bin/python3

import urllib.request as libreq
from urllib.error import HTTPError
import xmltodict
import sys
import re
import time


def generateMkdwn(arxivid: str) -> str:
    url = f"https://export.arxiv.org/api/query?id_list={arxivid}"
    try:
        with libreq.urlopen(url) as u:
            r = u.read()
    except HTTPError as err:
        if err.code == 400:
            print("Wrong arXiv id")
        else:
            raise
    dr = xmltodict.parse(r)
    title = dr['feed']['entry']['title'].replace('\n', ' ')
    title = re.sub(' +', ' ', title)
    summ = dr['feed']['entry']['summary'].replace('\n', ' ')
    summ = re.sub(' +', ' ', summ)
    authlist = dr['feed']['entry']['author']
    if len(authlist) == 1:
        auths = authlist['name'] + ', '
    else:
        auths = ''
        for a in authlist:
            au = a['name']
            au = re.sub(' +', ' ', au)
            auths += au + ', '
    mkdwn = f'---\nlayout: post\ntitle: "{title}"\ndate: {time.strftime("%Y-%m-%d %H:%M:%S")}\ncategories: blog\ntags: [,arXiv]\n---\n\n**{auths}**\n[![arXiv:{arxivid}](https://img.shields.io/badge/arXiv-{arxivid}-00ff00)](https://arxiv.org/abs/{arxivid})\n\n*Abstract:*\n{summ}'
    return mkdwn


def escape(text: str) -> str:
    newtext = ''
    opendollar = False
    for c in text:
        if c == '$':
            if opendollar:
                newtext += r'\\)'
                opendollar = False
            else:
                newtext += r'\\('
                opendollar = True
        elif (c == '\\') and opendollar:
            newtext += r'\\'
        elif (c == '_') and opendollar:
            newtext += r'\_'
        elif (c == '{') and opendollar:
            newtext += r'\{'
        elif (c == '}') and opendollar:
            newtext += r'\}'
        elif (c == '*') and opendollar:
            newtext += r'\*'
        else:
            newtext += c
    return newtext

if __name__ == "__main__":
    if sys.argv[0][-3:] == '.py':
        arxivid = sys.argv[1]
    else:
        arxivid = sys.argv[1]
    print(escape(generateMkdwn(arxivid)))
