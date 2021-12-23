#!/usr/bin/python3

import urllib.request as libreq
from urllib.error import HTTPError
import xmltodict
import sys
import re


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
    mkdwn = f"## {title}\n {auths}[![](https://img.shields.io/badge/arXiv-{arxivid}-00ff00)](https://arxiv.org/abs/{arxivid})\n\n{summ}"
    return mkdwn


if __name__ == "__main__":
    if sys.argv[0][-3:] == '.py':
        arxivid = sys.argv[1]
    else:
        arxivid = sys.argv[1]
    print(generateMkdwn(arxivid))
