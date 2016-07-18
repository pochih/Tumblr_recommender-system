#!/usr/bin/env python

# Python bindings to the Google search engine
# Copyright (c) 2009-2013, Mario Vilas
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright notice,
#       this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice,this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

__all__ = ['search']

import os
import os.path
import re
import sys
import time

if sys.version_info[0] > 2:
    from http.cookiejar import LWPCookieJar
    from urllib.request import Request, urlopen
    from urllib.parse import quote_plus, urlparse, parse_qs
else:
    from cookielib import LWPCookieJar
    from urllib import quote_plus
    from urllib2 import Request, urlopen
    from urlparse import urlparse, parse_qs

# Lazy import of BeautifulSoup.
BeautifulSoup = None

# URL templates to make Google searches.
url_home          = "http://demo.caffe.berkeleyvision.org/"
url_search        = "http://demo.caffe.berkeleyvision.org/classify_url?imageurl=%(query)s"

# Cookie jar. Stored at the user's home folder.
home_folder = os.getenv('HOME')
if not home_folder:
    home_folder = os.getenv('USERHOME')
    if not home_folder:
        home_folder = '.'   # Use the current folder on error.
cookie_jar = LWPCookieJar(os.path.join(home_folder, '.google-cookie'))
try:
    cookie_jar.load()
except Exception:
    pass

# Request the given URL and return the response page, using the cookie jar.
def get_page(url):
    """
    Request the given URL and return the response page, using the cookie jar.

    @type  url: str
    @param url: URL to retrieve.

    @rtype:  str
    @return: Web page retrieved for the given URL.

    @raise IOError: An exception is raised on error.
    @raise urllib2.URLError: An exception is raised on error.
    @raise urllib2.HTTPError: An exception is raised on error.
    """
    request = Request(url)
    request.add_header('User-Agent',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)')
    
    while True:
        try:
            cookie_jar.add_cookie_header(request)
            response = urlopen(request)
            cookie_jar.extract_cookies(response, request)
            break
        except:
            time.sleep(2)
            print url + "Error"
            continue

    html = response.read()
    response.close()
    cookie_jar.save()
    return html

# Filter links found in the Google result pages HTML code.
# Returns None if the link doesn't yield a valid result.

# Returns a generator that yields URLs.
def search(query, tld='com', lang='en', num=10, start=0, stop=None, pause=2):

    # Lazy import of BeautifulSoup.
    # Try to use BeautifulSoup 4 if available, fall back to 3 otherwise.
    global BeautifulSoup
    if BeautifulSoup is None:
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            from BeautifulSoup import BeautifulSoup

    # Set of hashes for the results found.
    # This is used to avoid repeated results.
    # Prepare the search string.
    query = quote_plus(query)

    # Grab the cookie from the home page.
    get_page(url_home % vars())

    # Prepare the URL of the first request.
    if start:
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
    else:
        if num == 10:
            url = url_search % vars()
        else:
            url = url_search_num % vars()

    # Loop until we reach the maximum result, if any (otherwise, loop forever).
    # Request the Google Search results page.
    html = get_page(url)
        # Parse the response and process every anchored URL.
    soup = BeautifulSoup(html, "lxml")

    anchors = None
    if soup.find(id='myTabContent'):
        anchors = soup.find(id='myTabContent').findAll('a')
    if not anchors:
        return []
    scores = [re.findall("[.\d]+", str(span))[0] for span in soup.find(id='myTabContent').findAll('span')]

    imageTag = []

    counter = 0
    for a in anchors:
        # Get the URL from the anchor tag.
        try:
            for link in a:
                #print "%s" %link
                imageTag.append((link, scores[counter]))
                counter += 1

        except KeyError:
            continue
    return imageTag

def parser(query):
    from optparse import OptionParser, IndentedHelpFormatter

    class BannerHelpFormatter(IndentedHelpFormatter):
        "Just a small tweak to optparse to be able to print a banner."
        def __init__(self, banner, *argv, **argd):
            self.banner = banner
            IndentedHelpFormatter.__init__(self, *argv, **argd)
        def format_usage(self, usage):
            msg = IndentedHelpFormatter.format_usage(self, usage)
            return '%s\n%s' % (self.banner, msg)

    # Parse the command line arguments.
    formatter = BannerHelpFormatter(
        "Python script to use the Google search engine\n"
        "By Mario Vilas (mvilas at gmail dot com)\n"
        "https://github.com/MarioVilas/google\n"
    )
    parser = OptionParser(formatter=formatter)
    parser.set_usage("%prog [options] query")
    parser.add_option("--tld", metavar="TLD", type="string", default="com",
                      help="top level domain to use [default: com]")
    parser.add_option("--lang", metavar="LANGUAGE", type="string", default="en",
                      help="produce results in the given language [default: en]")
    parser.add_option("--num", metavar="NUMBER", type="int", default=10,
                      help="number of results per page [default: 10]")
    parser.add_option("--start", metavar="NUMBER", type="int", default=0,
                      help="first result to retrieve [default: 0]")
    parser.add_option("--stop", metavar="NUMBER", type="int", default=0,
                      help="last result to retrieve [default: unlimited]")
    parser.add_option("--pause", metavar="SECONDS", type="float", default=2,
                      help="pause between HTTP requests [default: 2]")
    (options, args) = parser.parse_args()
    if not query:
        parser.print_help()
        sys.exit(2)
    
    params = [(k,v) for (k,v) in options.__dict__.items() if not k.startswith('_')]
    params = dict(params)

    # Run the query.
    imageTag = search(query, **params)
    return imageTag

def OCR(url):
    # parse url
    path = url.split('/')
    filename = path[len(path)-1]
    print " [ImageUtil.OCR] Retrieve", filename

    # fetch url
    import urllib
    urllib.urlretrieve(url, filename)

    # do OCR
    from subprocess import call
    if os.path.isfile(filename):
        with open('result.txt', 'w') as f:
            call(["pytesseract", filename], stdout=f)
    else:
        return []

    # read OCR's result
    result = open('result.txt', 'r').read().split()

    # rm temporary file
    os.remove('result.txt')
    os.remove(filename)

    return result

if __name__ == "__main__":
    query = sys.argv[1]
    tags = parser(query)
    print tags