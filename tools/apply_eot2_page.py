"""One-time edit (2026-11-25): move the lot catalogue off the home page into its own
"Echoes of Time II" page, and show the event cover on the home page as the link to it.
After this, index.html is the single source: run tools/build_eot2_page.py to regenerate
echoes-of-time-2.html whenever index.html changes."""
import re, sys
p = 'index.html'
s = open(p, encoding='utf-8').read()
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count: sys.exit(f'expected {count}, found {n}: {old[:80]!r}')
    s = s.replace(old, new)

s = s.replace('Echoes of Time 2', 'Echoes of Time II')
rep('<html lang="en">', '<html lang="en" class="p-home">')

# hero: lot slideshow -> event cover linking to the lot page
s, n = re.subn(r'<figure class="show" style="margin:0" id="show".*?</figure>', '''<a class="eot-cover" href="echoes-of-time-2.html">
    <img src="img/eot2/cover.jpg" alt="Echoes of Time II catalogue cover" width="900" height="1275" decoding="async">
    <span class="eot-cap"><span>Echoes of Time II · 21 November 2026</span><b>See the lots</b></span>
  </a>''', s, count=1, flags=re.S)
if n != 1: sys.exit('hero figure not found')
rep("  const box=$('show'),slides=", "  if(!$('show'))return;\n  const box=$('show'),slides=")

# links to the catalogue now go to its page
rep('<nav id="nav"><a href="#recap">Recap</a><a href="#auction">The lots</a>', '<nav id="nav"><a href="#recap">Recap</a><a href="echoes-of-time-2.html">The lots</a>')
rep('<a class="cta ghost" href="#auction">Browse the lots</a>', '<a class="cta ghost" href="echoes-of-time-2.html">Browse the lots</a>')
rep('<p class="note">The lots offered that day remain in the catalogue below, with their photographs and descriptions.</p>',
    '<p class="note">The lots offered that day, with their photographs and descriptions, are in the Echoes of Time II lot section.</p>\n  <div class="ctas" style="margin-top:16px"><a class="cta ghost" href="echoes-of-time-2.html">See the Echoes of Time II lots</a></div>')

# lot page header (shown only on echoes-of-time-2.html)
rep('<section id="auction">', '''<div class="eot-head">
  <a class="eot-back" href="./">&#8249; VietAuction home</a>
  <div class="eot-hd">
    <img src="img/eot2/cover.jpg" alt="Echoes of Time II catalogue cover" width="900" height="1275">
    <div><div class="eyebrow">Auction lots</div><h1>Echoes of Time II</h1><p>21 November 2026 · La Vela Saigon Hotel, Ho Chi Minh City</p></div>
  </div>
</div>
<section id="auction">''')

# old lot links (#VA-...) on the home page move to the lot page
rep("function openFromHash(){const id=", "function openFromHash(){if(document.documentElement.classList.contains('p-home')&&/^#VA-\\d+/.test(location.hash)){location.replace('echoes-of-time-2.html'+location.hash);return}const id=")
rep("document.title=META[lang].t;", "document.title=document.documentElement.classList.contains('p-eot2')?L2('Echoes of Time II · The lots · VietAuction','Echoes of Time II · Các lô · VietAuction','Echoes of Time II · 출품작 · VietAuction'):META[lang].t;")

ADD = '''Object.assign(VI,{"See the lots":"Xem các lô","Echoes of Time II catalogue cover":"Bìa catalogue Echoes of Time II","The lots offered that day, with their photographs and descriptions, are in the Echoes of Time II lot section.":"Các lô được đưa ra đấu giá hôm đó, kèm hình ảnh và mô tả, có trong mục các lô Echoes of Time II.","See the Echoes of Time II lots":"Xem các lô Echoes of Time II","‹ VietAuction home":"‹ Trang chủ VietAuction","Auction lots":"Các lô đấu giá","21 November 2026 · La Vela Saigon Hotel, Ho Chi Minh City":"21 tháng 11 năm 2026 · Khách sạn La Vela Saigon, TP. Hồ Chí Minh"});
Object.assign(KO,{"See the lots":"출품작 보기","Echoes of Time II catalogue cover":"Echoes of Time II 도록 표지","The lots offered that day, with their photographs and descriptions, are in the Echoes of Time II lot section.":"이날 출품된 작품은 사진, 설명과 함께 Echoes of Time II 출품작 페이지에서 보실 수 있습니다.","See the Echoes of Time II lots":"Echoes of Time II 출품작 보기","‹ VietAuction home":"‹ VietAuction 홈","Auction lots":"경매 출품작","21 November 2026 · La Vela Saigon Hotel, Ho Chi Minh City":"2026년 11월 21일 · 라벨라 사이공 호텔, 호치민시"});
'''
rep("/* Recap photos from 21 November 2026.", ADD + "/* Recap photos from 21 November 2026.")

rep('/* recap */', '''/* page split: home (p-home) vs Echoes of Time II lot page (p-eot2) */
.p-home #auction,.p-home .band:has(+#auction),.p-home .eot-head{display:none}
.p-eot2 .hero,.p-eot2 .next,.p-eot2 #recap,.p-eot2 #about,.p-eot2 #heritage,.p-eot2 #impact,.p-eot2 #register,.p-eot2 .band{display:none}
.p-eot2 #auction{margin-top:0;padding-top:28px}.p-eot2 #auction>.eyebrow{display:none}
.eot-cover{display:block;position:relative;max-width:440px;justify-self:center;width:100%;text-decoration:none;color:#fff;box-shadow:0 18px 40px rgba(20,30,60,.22);transition:transform .3s,box-shadow .3s}
.eot-cover:hover{transform:translateY(-3px);box-shadow:0 24px 50px rgba(20,30,60,.3)}
.eot-cover img{display:block;width:100%;height:auto}
.eot-cap{position:absolute;left:0;right:0;bottom:0;display:flex;justify-content:space-between;align-items:center;gap:12px;padding:14px 18px;background:linear-gradient(transparent,rgba(10,18,40,.85));font-size:.8rem;letter-spacing:.06em}
.eot-cap b{font-weight:600;text-transform:uppercase;letter-spacing:.1em;border-bottom:1px solid #d9b46a;padding-bottom:2px}
.eot-head{padding-top:28px}
.eot-back{color:var(--muted);text-decoration:none;font-size:.9rem}
.eot-back:hover{color:var(--fg)}
.eot-hd{display:flex;gap:28px;align-items:center;margin-top:20px}
.eot-hd img{width:120px;height:auto;box-shadow:0 10px 24px rgba(20,30,60,.2)}
.eot-hd h1{font-family:var(--display);font-size:clamp(2rem,5vw,3.2rem);margin:6px 0 4px;line-height:1.05}
.eot-hd p{margin:0;color:var(--muted)}
@media (max-width:560px){.eot-hd img{width:84px}.eot-hd{gap:18px}}
/* recap */''')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
