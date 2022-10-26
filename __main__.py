#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time, sys, os, re
import urllib
import requests
from fake_useragent import UserAgent
import random

# pip3 install gTTS pygame
from gtts import gTTS
from io import BytesIO
from pygame import mixer

def fix_text(text):
    text = text.replace(chr(160), ' ') # replace weird spaces
    text = text.replace(chr(8226), ' ') # replaces '•'
    text = text.replace('’', "'")
    text = text.replace('\n', '  ')
    text = text.replace('        ', '  ').strip()
    return text

def get_proxy():
    """Get a random proxy IP address from sslproxies.org"""
    proxies_req = urllib.request.Request('https://www.sslproxies.org/')
    ua = UserAgent()
    proxies_req.add_header('User-Agent', ua.random)

    try:
        proxies_result = urllib.request.urlopen(
            proxies_req).read().decode('utf8')
        time.sleep(0.5)

        ip_start = proxies_result.find("UTC.") + 4
        ip_end = proxies_result.find("</textarea></div>")
        ip_string = proxies_result[ip_start:ip_end]

        # filter out invalid or empty proxy IP items in arr
        ips = ip_string.split("\n")
        ips = filter(None, ips)
        ips = filter(len, ips)
        ips = filter(lambda item: item, ips)
        proxies = list(filter(None, ips))

        # get random proxy
        proxy_index = random.randint(0, len(proxies) - 1)
        return proxies[proxy_index]

    except Exception as err:
        print(err)

def text_to_speech():
    """Create a Google Text-to-Speech MP3 file using a proxy IP address"""
    rando_proxy = get_proxy()
    print(f"\nrandom proxy: '{rando_proxy}'")

    # set random proxy IP and port as the OS environment
    os.environ["http_proxy"] = f"http://{rando_proxy}"
    os.environ["https_proxy"] = f"http://{rando_proxy}"

    # get the text from a text file in the same dir
    with open('input.txt') as f:
        lines = f.readlines()
    lines = '  '.join(lines)    
    lines = fix_text(lines)

    try:
        output = f'spoken-text-{int(time.time())}.mp3'
        mixer.init()
        sound = BytesIO()

        # pass something like 'com.au' to the optional 'tld' arg for a different speaker
        tts = gTTS(lines, lang='en')
        tts.save(output)
        tts.write_to_fp(sound)
        print(f"\x1b[32mMP3 file {output} created.\x1b[37m")
    except Exception as err:
        print(err)
        print("\x1b[31mFailed to create MP3 file from text\x1b[37m")


if __name__ == '__main__':
    text_to_speech()