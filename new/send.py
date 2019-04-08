#!/usr/bin/env python
import requests

#http://docs.python-requests.org/en/latest/user/quickstart/#post-a-multipart-encoded-file

url = "http://177.104.60.13/up/bin/upload.py"
fin = open('P2.ipynb', 'rb')
files = {'file': fin, 'nome': 'Daniel M. Martin (teste)', 'RA': '1760938', 'turma': 'NC5'}
try:
    r = requests.post(url, files=files)
    print r.text
finally:
    fin.close()
