#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import cgi
import os
import sys
import json
import cgitb; cgitb.enable()


def get_row(RA, submission_code):
    with open ('/var/www/html/up/files/index.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter = ',', quotechar = '"')
        for row in reader:
            # t, ip, name, ra, turma, code, succ, blocks, basename = row
            if str(row[3]).strip() == str(RA).strip() and str(row[5]).strip() == str(submission_code).strip():
                return row
            
    return None
            

def main():
    with open("setup.json", "r") as setupfile:
        data = json.load(setupfile)

    form = cgi.FieldStorage()
    qRA = cgi.escape(form['RA'].value, True)
    qCode = cgi.escape(form['code'].value, True)
    
    row = get_row(qRA, qCode)
    if not row:
        print "Status: 404 Not Found\r\n"
        print "Arquivo nao encontrado."
        return
        
    t, ip, name, ra, turma, code, succ, blocks, basename = row
    fullname = '/var/www/html/up/files/' + basename

    if not os.path.isfile(fullname):
        print "Status: 404 Not Found\r\n"

        print "Arquivo nao encontrado."
        return

    if t > data['download_after']:
        print "Status: 403 Forbidden\r\n"
        print "Arquivo nao pode ser baixado ainda."
        return
        
    print "Content-Type: application/octet-stream"
    print "Content-Disposition: attachment; filename=" + basename
    print
    
    with open(fullname, "rb") as f:
        while True:
            buffer = f.read(4096)
            if not buffer: break
            sys.stdout.write(buffer)
    

if __name__ == "__main__":
    main()


#    print "Content-Type: text/html; charset=utf-8\r\n\r\n"
#    print 'Content-Description: File Transfer'
#    print 'Content-Type: application/octet-stream' 
#    print 'Content-Disposition: attachment; filename=' + get_filename(RA, submission_code)
#    print 'Content-Transfer-Encoding: binary');
#    print 'Expires: 0'
