#!/usr/bin/env python
import cgi
import os
import sys
import json
import cgitb; cgitb.enable()
import hashlib
import time
from datetime import datetime as dt
import base64


def tstamp():
    ts = time.time()
    mili = int(round(time.time() * 1000)) - int(ts) * 1000
    return dt.fromtimestamp(ts).strftime('%Y%m%d%H%M%S') + ("%03d" % (mili,))


def get_hash(data):
    b = bytearray()
    b.extend(data)
    return base64.urlsafe_b64encode(hashlib.sha1(b).digest())


def get_filename(data, filename):
    t = tstamp()
    h = get_hash(data + t + filename)
    return t + '.' + h + '.' + filename, t, h


def process_upload(form):
    def fbuffer(f, chunk_size=16384):
        while True:
            chunk = f.read(chunk_size)
            if not chunk: break
            yield chunk

    # A nested FieldStorage instance holds the file
    fileitem = form['file']
    name = cgi.escape(form['nome'].value, True)
    RA = cgi.escape(form['RA'].value, True)
    turma = cgi.escape(form['turma'].value, True)

    # Test if the file was uploaded
    if fileitem.filename:

        # strip leading path from file name
        # to avoid directory traversal attacks
        fn = os.path.basename(fileitem.filename)
        nfn, t, h = get_filename(name + RA, fn)

        count = 0
        success = False
        with open('/var/www/html/up/files/' + nfn, 'wb') as f:
            for chunk in fbuffer(fileitem.file):
                count += 1
                if count > 2**11:
                    message = 'File limit of 32Mb exceeded. Upload failed.'
                    os.remove('/var/www/html/up/files/' + nfn)
                    break
                f.write(chunk)
            else:
                success = True
                #message = 'The file "' + fn + '" was uploaded successfully. Your submission code is: <b>' + h[:5] + '</b>'
                message = h[:5]


        with open('/var/www/html/up/files/index.csv', 'a') as g:
            ipaddr = cgi.escape(os.environ["REMOTE_ADDR"])
            g.write('"%s","%s","%s","%s","%s","%s","%s","%s","%s"\n' % (t, ipaddr, name, RA, turma, h[:5],
                    'success = ' + str(success), '16K blocks = ' + str(count), nfn))

    else:
        message = 'No file was uploaded'
    return message


def main():
    form = cgi.FieldStorage()

    with open("setup.json", "r") as setupfile:
        data = json.load(setupfile)

    t = tstamp()
    
    message = 'Nenhum upload pode ser feito neste momento.'
    for time_interval in data['upload_on']:
        r, s = time_interval
        if str(r) <= t <= str(s):
            print "Content-Type: text/text\n\n"
            print process_upload(form)
            sys.exit(0)

    print "Status: 403 Forbidden\r\n"
    print message
    

if __name__ == "__main__":
    main()
