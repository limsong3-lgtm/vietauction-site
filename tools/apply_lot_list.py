"""Apply the final lot list to index.html.

Source: Google Sheet "Auction Work File 11/21", tab "Final Lot List"
(certificate #, category, titles EN/VN, era, origin EN, height, width, weight, lot # in column AK),
copied into tools/final_lot_list.tsv.

What it does:
- only the lots in the TSV are public (every other lot goes into HIDDEN_LOTS)
- each public lot gets its lot number (field "l") and the sheet's title, era, origin, size, weight
- the lot cards are rebuilt from the data, sorted by lot number inside each kind of object

Run: python3 tools/apply_lot_list.py   (from the repo root)
"""
import csv, html, json, re

# Lim confirmed on 2026-11-12 that these two jade pieces are Chinese; the sheet still says Vietnam.
ORIGIN_OVERRIDE = {'SG260617BJTA06': 'China', 'SG260617ATXA01': 'China'}
# Korean titles for lots whose English title changed in the sheet
KO_TITLE = {
    'SG260617EHFA04': '희귀 중국 백유 주자',
    'SG260617VFGA04': "일본 청화 '매화' 장경병",
    'SG261006VSDA01': '중국 청대 청화 유개병',
}
# sheet category -> (site type, slug used for the vessel icon and the group id)
CATS = {'Plate': ('Plate', 'plate'), 'Bowl': ('Bowl', 'bowl'), 'Vase': ('Vase', 'vase'), 'Pot': ('Pot', 'pot'),
        'Ewer': ('Ewer', 'ewer'), 'Jar': ('Jar', 'jar'), 'Lidded Box': ('Lidded Box', 'box'), 'Jarlet': ('Jarlet', 'jarlet'),
        'Censer': ('Other', 'other')}
# group order and headings on the page: (group id, type, heading)
GROUPS = [('plate', 'Plate', 'Plates'), ('bowl', 'Bowl', 'Bowls'), ('vase', 'Vase', 'Vases'), ('pot', 'Pot', 'Pots'),
          ('ewer', 'Ewer', 'Ewers'), ('jar', 'Jar', 'Jars'), ('lidded-box', 'Lidded Box', 'Lidded boxes'),
          ('cup', 'Cup', 'Cups'), ('jarlet', 'Jarlet', 'Jarlets'), ('figurine', 'Figurine', 'Figurines'),
          ('other', 'Other', 'Other works')]


def ordinal(n):
    return n + ('st' if n.endswith('1') and n != '11' else 'th')


def era(r):
    parts = r.split('-')
    return '–'.join(ordinal(p) for p in parts) + ' c.', list(range(int(parts[0]), int(parts[-1]) + 1))


def size(h, w):
    cm = lambda v: '%g' % (int(v.replace(',', '')) / 10)
    return 'H ' + cm(h) + (' × Ø ' + cm(w) if w else '') + ' cm'


def grab(src, name):
    i = src.index(name + '=') + len(name) + 1
    val, n = json.JSONDecoder().raw_decode(src[i:])
    return val, i, i + n


src = open('index.html', encoding='utf-8').read()
lots, a, b = grab(src, 'const ALL_LOTS')
by_cert = {x['c'][0]: x for x in lots}
photos, _, _ = grab(src, 'const PHOTOS')

public = []
for row in csv.reader(open('tools/final_lot_list.tsv', encoding='utf-8'), delimiter='\t'):
    cert, cat, n, v, e, o, h, w, ln, g, lot = row
    x = by_cert[cert]
    x['t'], x['s'] = CATS[cat]
    x['n'] = n.strip().rstrip(',').strip()
    x['v'] = v.strip().rstrip(',').strip()
    x['e'], x['cn'] = era(e)
    x['o'] = ORIGIN_OVERRIDE.get(cert, o)
    x['d'] = size(h, w)
    x['g'] = g.replace(',', '') + ' g'
    x['l'] = int(lot)
    if cert in KO_TITLE:
        x['kt'] = KO_TITLE[cert]
    public.append(x)
public_ids = {x['id'] for x in public}
assert len(public) == len(public_ids) == len({x['l'] for x in public})
for x in lots:
    if x['id'] not in public_ids:
        x.pop('l', None)

# public lots first, in lot order (the drawer and hero read from this list)
lots.sort(key=lambda x: (x['id'] not in public_ids, x.get('l', 0)))
src = src[:a] + json.dumps(lots, ensure_ascii=False) + src[b:]
hidden = [x['id'] for x in lots if x['id'] not in public_ids]
_, a, b = grab(src, 'const HIDDEN_LOTS')
src = src[:a] + json.dumps(hidden) + src[b:]

# rebuild the chips and the lot cards
esc = lambda s: html.escape(s, quote=True)
chips, cats = [], []
for gid, typ, head in GROUPS:
    items = sorted((x for x in public if x['t'] == typ), key=lambda x: x['l'])
    if not items:
        continue
    chips.append(f'    <a href="#c-{gid}">{head}<b>{len(items)}</b></a>')
    cards = []
    for x in items:
        pic = (photos.get(x['id']) or [{}])[0].get('thumb')
        ph = (f'<div class="ph has-photo"><img src="{esc(pic)}" alt="{esc(x["n"])}" loading="lazy" decoding="async">'
              if pic else f'<div class="ph"><svg class="vessel" viewBox="0 0 100 100" aria-hidden="true"><use href="#v-{x["s"]}"/></svg>')
        cards.append(f'<button class="card" data-id="{x["id"]}">{ph}<span class="pg">Lot {x["l"]}</span></div>'
                     f'<div class="cb"><h4>{esc(x["n"])}</h4><div class="tags"><span class="tag">{esc(x["e"])}</span>'
                     f'<span class="tag">{esc(x["o"])}</span></div><div class="dim">{esc(x["d"])}</div>'
                     f'<div class="id">{x["id"]}</div><div class="more">View details and photos</div></div></button>')
    cats.append(f'  <div class="cat" id="c-{gid}"><h3>{head} <small>{len(items)} lots</small></h3><div class="grid">{"".join(cards)}</div></div>')

src = re.sub(r'(<div class="chips" style="margin-top:16px">\n).*?(\n\n  </div>)',
             lambda m: m.group(1) + '\n'.join(chips) + m.group(2), src, count=1, flags=re.S)
src = re.sub(r'(<div class="nomatch" id="nm" hidden>[^\n]*\n).*?(\n\n</section>)',
             lambda m: m.group(1) + '\n'.join(cats) + m.group(2), src, count=1, flags=re.S)

open('index.html', 'w', encoding='utf-8').write(src)
print(len(public), 'public lots,', len(hidden), 'hidden')
