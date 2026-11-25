"""Regenerate echoes-of-time-2.html (the Echoes of Time II lot page) from index.html.
Run from the repo root after any change to index.html: python3 tools/build_eot2_page.py"""
import re
s = open('index.html', encoding='utf-8').read()
s = s.replace('<html lang="en" class="p-home">', '<html lang="en" class="p-eot2">', 1)
s = s.replace('<title>VietAuction · Antique ceramic auctions in Vietnam</title>', '<title>Echoes of Time II · The lots · VietAuction</title>', 1)
s = s.replace('<a href="#">VietAuction</a>', '<a href="./">VietAuction</a>', 1)
# home-page sections are hidden here, so nav links to them go back to the home page
s = re.sub(r'href="#(recap|about|heritage|impact|register)"', r'href="./#\1"', s)
s = s.replace('href="echoes-of-time-2.html"', 'href="#auction"')
open('echoes-of-time-2.html', 'w', encoding='utf-8').write(s)
print('wrote echoes-of-time-2.html')
