"""Post-auction update (Nov 2026): close registration, add Echoes of Time 2 recap, announce Hanoi March 2027.
Run once from the repo root: python3 tools/apply_post_auction.py"""
import re, sys
p = 'index.html'
s = open(p, encoding='utf-8').read()

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        sys.exit(f'expected {count} match(es), found {n}: {old[:80]!r}')
    s = s.replace(old, new)

# meta
rep('<meta name="description" content="Echoes of Time 2, 21 November 2026: Vietnamese and Chinese antique ceramics, appraised, numbered and catalogued. Browse the lots and register to bid.">',
    '<meta name="description" content="Echoes of Time 2 took place on 21 November 2026 in Ho Chi Minh City. Our next auction of Vietnamese and Chinese antique ceramics will be in Hanoi in March 2027.">')
rep('<meta property="og:title" content="Echoes of Time 2 · VietAuction, 21 November 2026">',
    '<meta property="og:title" content="VietAuction · Next auction in Hanoi, March 2027">')
rep('<meta property="og:description" content="Vietnamese and Chinese antique ceramics, appraised, numbered and catalogued. Browse the lots and register to bid.">',
    '<meta property="og:description" content="Thank you for joining Echoes of Time 2 on 21 November 2026. Our next auction will be in Hanoi in March 2027, details coming soon.">')
rep("d:'Echoes of Time 2, 21 November 2026: Vietnamese and Chinese antique ceramics, appraised, numbered and catalogued. Browse the lots and register to bid.'",
    "d:'Echoes of Time 2 took place on 21 November 2026 in Ho Chi Minh City. Our next auction of Vietnamese and Chinese antique ceramics will be in Hanoi in March 2027.'")
rep("d:'Echoes of Time 2, 2026년 11월 21일: 감정을 거쳐 번호가 부여되고 도록에 수록된 베트남·중국 고도자기. 출품작을 둘러보고 응찰 등록을 하세요.'",
    "d:'Echoes of Time 2 경매가 2026년 11월 21일 호치민시에서 열렸습니다. 베트남·중국 고도자기 다음 경매는 2027년 3월 하노이에서 열립니다.'")
rep("d:'Echoes of Time 2, ngày 21 tháng 11 năm 2026: gốm sứ cổ Việt Nam và Trung Hoa, được giám định, đánh số và lập danh mục. Xem các lô và đăng ký đấu giá.'",
    "d:'Echoes of Time 2 đã diễn ra ngày 21 tháng 11 năm 2026 tại TP. Hồ Chí Minh. Phiên đấu giá gốm sứ cổ Việt Nam và Trung Hoa tiếp theo sẽ diễn ra tại Hà Nội vào tháng 3 năm 2027.'")

# nav + hero
rep('<nav id="nav"><a href="#auction">The lots</a>', '<nav id="nav"><a href="#recap">Recap</a><a href="#auction">The lots</a>')
rep('<div class="ctas"><a class="cta" href="#register">Register to bid</a><a class="cta ghost" href="#auction">Browse the lots</a></div>',
    '<div class="ctas"><a class="cta" href="#recap">See the auction recap</a><a class="cta ghost" href="#auction">Browse the lots</a></div>')

rep('<a class="cta sm" href="#register">Register to bid</a>', '<a class="cta sm" href="#contact" data-contact-link>Hanoi · March 2027</a>')

# next-auction strip
rep('''<div class="next">
  <div class="l"><div class="lab">Next auction</div><div class="nm">Echoes of Time 2</div></div>
  <dl><dt>Date</dt><dd>21 November 2026</dd><dt>Venue</dt><dd>La Vela Saigon Hotel, 25th floor</dd><dt>Lots</dt><dd>67 ceramics</dd></dl>
  <a class="cta" href="#register">Register to bid</a>
</div>''', '''<div class="next">
  <div class="l"><div class="lab">Next auction</div><div class="nm">Hanoi · March 2027</div></div>
  <dl><dt>Date</dt><dd>March 2027</dd><dt>Venue</dt><dd>Hanoi</dd></dl>
  <a class="cta" href="#contact" data-contact-link>Hear about it first</a>
</div>

<section id="recap">
  <div class="eyebrow">Echoes of Time 2 · 21 November 2026</div>
  <h2>Thank you for joining Echoes of Time 2</h2>
  <p>On 21 November 2026, collectors and guests gathered on the 25th floor of La Vela Saigon Hotel in Ho Chi Minh City for Echoes of Time 2. Thank you to everyone who came to view the pieces, placed a bid and shared the day with us.</p>
  <div class="recap-grid" id="recap-grid" hidden></div>
  <p class="note">The lots offered that day remain in the catalogue below, with their photographs and descriptions.</p>
</section>''')

# syncPublicCounts: next-auction rows
s, n = re.subn(r"  if\(dds\[0\]\)dds\[0\]\.textContent=L2\('21 November 2026'.*?\n  if\(dds\[1\]\).*?\n  if\(dds\[2\]\).*?\n",
    "  if(dds[0])dds[0].textContent=L2('March 2027, exact date coming soon','Tháng 3 năm 2027, ngày cụ thể sẽ sớm được công bố','2027년 3월, 정확한 날짜는 곧 안내 예정');\n"
    "  if(dds[1])dds[1].textContent=L2('Hanoi, venue coming soon','Hà Nội, địa điểm sẽ sớm được công bố','하노이, 장소는 곧 안내 예정');\n", s, flags=re.S)
if n != 1: sys.exit('syncPublicCounts rows not found')

# registration section -> closed notice
s, n = re.subn(r'<section id="register">.*?</section>', '''<section id="register">
  <div class="eyebrow">Registration</div>
  <h2>Registration for Echoes of Time 2 is closed</h2>
  <p>The auction took place on 21 November 2026. Our next auction will be held in Hanoi in March 2027. The date, venue and lots will be announced here soon. To hear first about the Hanoi auction, contact our team.</p>
  <div class="ctas" style="margin-top:20px"><a class="cta" href="#contact" data-contact-link>Contact our team</a></div>
</section>''', s, count=1, flags=re.S)
if n != 1: sys.exit('register section not found')

# lot sheet: drop "Register to bid on this lot"
rep('''<div><button class="cta" id="rg">${L2('Register to bid on this lot','Đăng ký đấu giá lô này','이 출품작 응찰 등록')}</button></div>''', '')
s, n = re.subn(r"\n  \$\('rg'\)\.onclick=.*?\n", "\n", s, count=1)
if n != 1: sys.exit('rg handler not found')

# registration JS: form is gone
s, n = re.subn(r"\n/\* registration \*/\n\$\('rf'\)\.addEventListener.*?\nif\(REG_ENDPOINT\)\$\('demo'\)\.hidden=true;\n", "\n", s, count=1, flags=re.S)
if n != 1: sys.exit('registration JS not found')
rep("if(!REG_ENDPOINT&&CONTACT.phone){const t=", "if(!REG_ENDPOINT&&CONTACT.phone&&$('demo')){const t=")

# recap photos + translations, inserted after the contact painter
ADD = r'''
/* ---- post-auction update (Nov 2026): Echoes of Time 2 recap, registration closed, Hanoi March 2027 ---- */
/* Recap photos from 21 November 2026. Add files under img/recap/ and list them here; the grid stays hidden while the list is empty. */
const RECAP_PHOTOS=[];
(function(){const g=$('recap-grid');if(!g||!RECAP_PHOTOS.length)return;
  g.innerHTML=RECAP_PHOTOS.map(p=>`<figure><a href="${esc(p.full||p.src)}" target="_blank" rel="noopener"><img src="${esc(p.src)}" alt="${esc(p.alt||'')}" loading="lazy" decoding="async"></a></figure>`).join('');g.hidden=false;})();
Object.assign(VI,{"Recap":"Nhìn lại","See the auction recap":"Xem lại phiên đấu giá","Next auction":"Phiên đấu giá tiếp theo","Hanoi · March 2027":"Hà Nội · Tháng 3 năm 2027","Hear about it first":"Nhận thông tin sớm nhất","Thank you for joining Echoes of Time 2":"Cảm ơn quý vị đã đến với Echoes of Time 2","On 21 November 2026, collectors and guests gathered on the 25th floor of La Vela Saigon Hotel in Ho Chi Minh City for Echoes of Time 2. Thank you to everyone who came to view the pieces, placed a bid and shared the day with us.":"Ngày 21 tháng 11 năm 2026, các nhà sưu tầm và khách mời đã cùng có mặt tại tầng 25 khách sạn La Vela Saigon, TP. Hồ Chí Minh, cho phiên đấu giá Echoes of Time 2. Xin cảm ơn tất cả quý vị đã đến chiêm ngưỡng hiện vật, tham gia đấu giá và đồng hành cùng chúng tôi trong ngày hôm ấy.","The lots offered that day remain in the catalogue below, with their photographs and descriptions.":"Các lô được đưa ra đấu giá hôm đó vẫn có trong danh mục bên dưới, kèm hình ảnh và mô tả.","Registration":"Đăng ký","Registration for Echoes of Time 2 is closed":"Đăng ký tham gia Echoes of Time 2 đã kết thúc","The auction took place on 21 November 2026. Our next auction will be held in Hanoi in March 2027. The date, venue and lots will be announced here soon. To hear first about the Hanoi auction, contact our team.":"Phiên đấu giá đã diễn ra vào ngày 21 tháng 11 năm 2026. Phiên đấu giá tiếp theo của chúng tôi sẽ được tổ chức tại Hà Nội vào tháng 3 năm 2027. Ngày, địa điểm và danh sách các lô sẽ sớm được công bố tại đây. Để nhận thông tin sớm nhất về phiên đấu giá tại Hà Nội, vui lòng liên hệ đội ngũ của chúng tôi.","Contact our team":"Liên hệ đội ngũ"});
Object.assign(KO,{"Recap":"현장 스케치","See the auction recap":"경매 현장 보기","Next auction":"다음 경매","Hanoi · March 2027":"하노이 · 2027년 3월","Hear about it first":"가장 먼저 소식 받기","Thank you for joining Echoes of Time 2":"Echoes of Time 2에 함께해 주셔서 감사합니다","On 21 November 2026, collectors and guests gathered on the 25th floor of La Vela Saigon Hotel in Ho Chi Minh City for Echoes of Time 2. Thank you to everyone who came to view the pieces, placed a bid and shared the day with us.":"2026년 11월 21일, 호치민시 라벨라 사이공 호텔 25층에서 Echoes of Time 2 경매가 열렸습니다. 작품을 감상하고 응찰에 참여하며 이날을 함께해 주신 모든 분께 감사드립니다.","The lots offered that day remain in the catalogue below, with their photographs and descriptions.":"이날 출품된 작품은 사진, 설명과 함께 아래 도록에서 계속 보실 수 있습니다.","Registration":"등록","Registration for Echoes of Time 2 is closed":"Echoes of Time 2 응찰 등록이 마감되었습니다","The auction took place on 21 November 2026. Our next auction will be held in Hanoi in March 2027. The date, venue and lots will be announced here soon. To hear first about the Hanoi auction, contact our team.":"경매는 2026년 11월 21일에 진행되었습니다. 다음 경매는 2027년 3월 하노이에서 열릴 예정입니다. 일정, 장소 및 출품작은 곧 이곳에서 안내해 드리겠습니다. 하노이 경매 소식을 가장 먼저 받으시려면 담당자에게 문의해 주세요.","Contact our team":"담당자에게 문의"});
'''
rep("paintContact();document.addEventListener('va-lang',paintContact);", "paintContact();document.addEventListener('va-lang',paintContact);" + ADD)

# css
rep('/* contact + footer */', '''/* recap */
.recap-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin:28px 0 8px}
.recap-grid figure{margin:0;aspect-ratio:3/2;overflow:hidden;background:var(--photo)}
.recap-grid img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .4s}
.recap-grid a:hover img{transform:scale(1.03)}
.recap-grid figure:first-child{grid-column:span 2;grid-row:span 2}
@media (max-width:560px){.recap-grid figure:first-child{grid-column:auto;grid-row:auto}}
/* contact + footer */''')

open(p, 'w', encoding='utf-8').write(s)
print('ok')
