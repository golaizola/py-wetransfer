#!/usr/bin/python
# -*- coding: utf-8 -*-

from urlparse import urlparse, parse_qs
import urllib, urllib2, sys, json, re, getopt

DOWNLOAD_URL_PARAMS_PREFIX = 'downloads/'

def download(file_id, recipient_id, security_hash):
    url = "https://www.wetransfer.com/api/v1/transfers/{0}/download?recipient_id={1}&security_hash={2}&password=&ie=false".format(file_id, recipient_id, security_hash)
    r = urllib.urlopen(url).read()
    download_data = json.loads(r)

    print "Downloading {0}...".format(url)
    if download_data.has_key('direct_link'):
        content_info_string = parse_qs(urlparse(download_data['direct_link']).query)['response-content-disposition'][0]
        file_name = re.findall('filename="(.*?)"', content_info_string)[0]
        r = urllib.urlopen(download_data['direct_link'])
    else:
        file_name = download_data['fields']['filename']
        data = urllib.urlencode(download_data["fields"])
        req = urllib2.Request(download_data['formdata']['action'], data)
        r = urllib2.urlopen(req)

    output_file = open(file_name, 'w')
    output_file.write(r.read())
    output_file.close()
    print "Finished! {0}".format(file_name)


def extract_params(url):
    """
        Extracts params from url
    """
    params = url.split(DOWNLOAD_URL_PARAMS_PREFIX)[1].split('/')
    [file_id, recipient_id, security_hash] = ['', '', '']
    if len(params) > 2:
        #The url is similar to https://www.wetransfer.com/downloads/XXXXXXXXXX/YYYYYYYYY/ZZZZZZZZ
        [file_id, recipient_id, security_hash] = params
    else:
        #The url is similar to https://www.wetransfer.com/downloads/XXXXXXXXXX/ZZZZZZZZ
        #In this case we have no recipient_id
        [file_id, security_hash] = params

    return [file_id, recipient_id, security_hash]


def usage():
    print """
You should have a we transfer address similar to https://www.wetransfer.com/downloads/XXXXXXXXXX/YYYYYYYYY/ZZZZZZZZ

So execute:
    python wetransfer.py -u https://www.wetransfer.com/downloads/XXXXXXXXXXXXXXXXXXXXXXXXX/YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY/ZZZZZ

And download it! :)
"""
    sys.exit()


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "u:h", ['url', 'help'])
        url = None
        for opt, arg in opts:
            if opt in ('-u', '--url'):
                url = arg
            if opt in ('-h', '--help'):
                usage()

        if not url:
            usage()

        [file_id, recipient_id, security_hash] = extract_params(url)
        download(file_id, recipient_id, security_hash)

    except getopt.GetoptError:
        usage()
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
