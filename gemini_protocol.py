#!/usr/bin/env python3

import os
import socket
import ssl
import urllib.parse
import magic


def absolutise_url(base, relative):
    # Absolutise relative links
    if "://" not in relative:
        # Python's URL tools somehow only work with known schemes?
        base = base.replace("gemini://","http://")
        relative = urllib.parse.urljoin(base, relative)
        relative = relative.replace("http://", "gemini://")
    return relative

def gemini(url):
    status, mime, fp = 0,0,0
    success = True
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme != "gemini":
        if parsed_url.scheme == "file":
            try:
                fp = open(url.replace(parsed_url.scheme + "://", ""), "r")
                mime = magic.Magic(mime=True).from_file(url.replace(parsed_url.scheme + "://", ""))
                if url[-4:].lower == ".gmi":
                    mime = "text/gemini"
                status = "202"
            except Exception as err:
                print(err)
                success = False
        elif 1 != 1:
            pass
        else:
            print("Sorry, Gemini links only.")
            print("(Attempted link : " + url + ")")
            success = False
    else:
    	# Do the Gemini transaction
        try:
            while True:
                s = socket.create_connection((parsed_url.netloc, 1965))
                context = ssl.SSLContext()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                s = context.wrap_socket(s, server_hostname = parsed_url.netloc)
                s.sendall((url + '\r\n').encode("UTF-8"))
                # Get header and check for redirects
                fp = s.makefile("rb")
                header = fp.readline()
                header = header.decode("UTF-8").strip()
                status = header.split()[0]
                mime = header.split()[1]
                # Handle input requests
                if status.startswith("1"):
                    # Prompt
                    query = input("INPUT" + mime + "> ")
                    url += "?" + urllib.parse.quote(query) # Bit lazy...
                # Follow redirects
                elif status.startswith("3"):
                    url = absolutise_url(url, mime)
                    parsed_url = urllib.parse.urlparse(url)
                # Otherwise, we're done.
                else:
                    break
            # Fail if transaction was not successful
            if not status.startswith("2"):
                print("Error %s: %s" % (status, mime))
                success = False
        except Exception as err:
            print(err)
            success = False
    # Return information
    return [success, status, mime, fp]
