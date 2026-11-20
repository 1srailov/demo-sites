import os
"""Generate studio-type demo pages from the Hazal template's CSS."""
import json, re, sys, urllib.parse

BASE = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'hazal-fotografevi', 'index.html'), encoding='utf-8').read()
CSS = BASE[BASE.index('<style>'):BASE.index('</style>') + 8]
EXTRA_CSS = """
<style>
  .store{border-radius:12px;overflow:hidden;margin:-6px -6px 14px;aspect-ratio:16/9;background:#e9edf4}
  .store img{width:100%;height:100%;object-fit:cover;display:block}
  .store-cap{font-size:13px;color:var(--soft);margin:-6px 0 12px}
  .real-grid{columns:3 240px;column-gap:12px}
  .real-grid figure{break-inside:avoid;margin:0 0 12px;border-radius:12px;overflow:hidden;cursor:zoom-in;background:#e9edf4}
  .real-grid img{width:100%;height:auto;display:block}
  .lb{position:fixed;inset:0;z-index:100;background:rgba(15,18,28,.94);display:none;align-items:center;justify-content:center}
  .lb.open{display:flex}
  .lb img{max-width:92vw;max-height:86vh;object-fit:contain;border-radius:4px}
  .lb button{position:absolute;background:rgba(255,255,255,.12);border:0;color:#fff;width:48px;height:48px;border-radius:50%;font-size:26px;cursor:pointer}
  .lb .c{top:18px;right:18px}.lb .p{left:16px;top:50%}.lb .n{right:16px;top:50%}
</style>"""
WA_SVG = BASE[BASE.index('<svg viewBox="0 0 24 24" fill="currentColor">'):]
WA_SVG = WA_SVG[:WA_SVG.index('</svg>') + 6]
FAB_SVG = '<svg viewBox="0 0 24 24"><path d="' + re.search(r'<path d="([^"]+)"', WA_SVG).group(1) + '"/></svg>'
IMG = 'https://lh3.googleusercontent.com/'
ICONS = {
 'id': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="10" r="3"/><path d="M7 18c1-2.5 3-3.5 5-3.5s4 1 5 3.5"/></svg>',
 'baby': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="8" r="4"/><path d="M5 21c1.5-4 4-6 7-6s5.5 2 7 6"/></svg>',
 'family': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="8" cy="8" r="3"/><circle cx="16" cy="8" r="3"/><path d="M2.5 20c.8-3.2 3-5 5.5-5s4.7 1.8 5.5 5M10.5 20c.8-3.2 3-5 5.5-5s4.7 1.8 5.5 5"/></svg>',
 'print': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 9V3h12v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M6 14h12v7H6z"/></svg>',
 'copy': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"/></svg>',
 'heart': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 20s-7-4.5-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.5-7 10-7 10z"/></svg>',
 'paw': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="7" cy="9" r="1.8"/><circle cx="11" cy="6" r="1.8"/><circle cx="15" cy="6" r="1.8"/><circle cx="18" cy="10" r="1.8"/><path d="M8 17c0-3 2-5 4-5s4 2 4 5c0 1.7-1.6 2.5-4 2.5S8 18.7 8 17z"/></svg>',
 'cal': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/></svg>',
}
PH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-8 8"/></svg>'
DAYS = [('1','Pazartesi'),('2','Salı'),('3','Çarşamba'),('4','Perşembe'),('5','Cuma'),('6','Cumartesi'),('0','Pazar')]

def esc(s): return s.replace('&', '&amp;')

def build(d):
    wa = d['wa']; tel = d['tel']
    waq = lambda t: f"https://wa.me/{wa}?text={urllib.parse.quote(t)}"
    dir_url = 'https://www.google.com/maps/dir/?api=1&destination=' + urllib.parse.quote(d['maps_q'])
    hours_rows = '\n'.join(f'          <tr data-d="{k}"><td>{n}</td><td>{d["hours"].get(k, "Kapalı")}</td></tr>' for k, n in DAYS)
    sched = {k: [int(a[:2])*60+int(a[3:5]), int(b[:2])*60+int(b[3:5])] for k, v in d['hours'].items() for a, b in [v.split(' – ')]}
    svc = '\n'.join(
        f'      <div class="svc"><div class="icon">{ICONS[s["icon"]]}</div><h3>{s["t"]}</h3><p>{s["p"]}</p>'
        + (('<div class="tags">' + ''.join(f'<span>{t}</span>' for t in s['tags']) + '</div>') if s.get('tags') else '')
        + '</div>' for s in d['services'])
    if d.get('gallery'):
        gal = '<div class="real-grid">' + ''.join(f'<figure><img loading="lazy" src="{IMG}{g}=w900-h900-k-no" data-big="{IMG}{g}=w1600-h1600-k-no" alt="Çekim fotoğrafı"></figure>' for g in d['gallery']) + '</div>'
        gal_sub = d.get('gallery_sub', 'Stüdyomuzdan birkaç kare.')
    else:
        gal = '<div class="ph-grid">' + ''.join(f'<div class="ph">{PH}{x}</div>' for x in d['ph_labels']) + '</div>'
        gal_sub = 'Bu alana stüdyonuzdan ve çekimlerinizden fotoğraflar eklenecek.'
    revs = ''
    if d.get('reviews'):
        revs = '<div class="reviews">\n' + '\n'.join(f'      <div class="rev"><div class="stars">★★★★★</div><blockquote>“{q}”</blockquote><cite>{n} · Google yorumu</cite></div>' for q, n in d['reviews']) + '\n    </div>'
    store = ''
    if d.get('store'):
        store = f'<div class="store"><img src="{IMG}{d["store"]}=w900-h600-k-no" alt="{esc(d["name"])} dükkânı"></div>' + (f'<p class="store-cap">{d["store_cap"]}</p>' if d.get('store_cap') else '')
    rating_line = f'<strong>{d["rating"]}</strong> · {d["reviews_n"]} Google yorumu'
    cta2 = d.get('cta_wa_label', 'WhatsApp')
    html = f'''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow, noarchive">
<title>{esc(d["name"])} · {d["title_tail"]} (Örnek Tasarım)</title>
<meta name="description" content="{d["desc"]}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(d["name"])} · {d["area"]}">
<meta property="og:description" content="{d["desc"]}">
{f'<meta property="og:image" content="{IMG}{d["og"]}=w1200-h630-p-k-no">' if d.get("og") else ''}
<meta property="og:locale" content="tr_TR">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
{CSS}
{EXTRA_CSS}
</head>
<body>

<div class="demo-bar"><b>Örnek tasarım.</b> Bu sayfa {esc(d["name"])} için hazırlanmış bir demo çalışmadır, işletme adına yayınlanmamıştır.</div>

<header class="hero">
  <div class="hero-grid">
    <div>
      <div class="eyebrow">{d["area"]}</div>
      <h1>{d["h1"]}</h1>
      <p class="lead">{d["lead"]}</p>
      <div class="rating"><span class="stars">★★★★★</span><span>{rating_line}</span></div>
      <div class="btns">
        <a class="btn btn-wa" href="{waq(d["wa_text"])}" target="_blank" rel="noopener">
          {WA_SVG}
          {cta2}
        </a>
        <a class="btn btn-call" href="tel:{tel}">Hemen arayın</a>
        <a class="btn btn-dir" href="{dir_url}" target="_blank" rel="noopener">Yol tarifi</a>
      </div>
    </div>
    <div class="info-card">
      {store}
      <div class="status" id="status"><i></i><span>Çalışma saatleri</span></div>
      <div class="info-row"><div class="ic">📍</div><div><small>Adres</small>{d["addr_short"]}</div></div>
      <div class="info-row"><div class="ic">🕘</div><div><small>Çalışma saatleri</small>{d["hours_text"]}</div></div>
      <div class="info-row"><div class="ic">📞</div><div><small>Telefon</small><a href="tel:{tel}">{d["phone"]}</a></div></div>
    </div>
  </div>
</header>

<section id="hizmetler">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Hizmetler</div>
      <h2>Neler yapıyoruz?</h2>
    </div>
    <div class="services">
{svc}
    </div>
    <p class="note">{d["note_lead"]} <a href="{waq(d["note_wa_text"])}" target="_blank" rel="noopener">WhatsApp'tan yazın</a>.</p>
  </div>
</section>

<section id="galeri" style="padding-top:0">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Galeri</div>
      <h2>Stüdyomuzdan kareler</h2>
      <p>{gal_sub}</p>
    </div>
    {gal}
  </div>
</section>

<section class="reviews-bg" id="yorumlar">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Yorumlar</div>
      <h2>Müşterilerimiz ne diyor?</h2>
    </div>
    {revs}
    <p class="g-src">Google'da {d["reviews_n"]} yorum, ortalama puan {d["rating"]} · <a href="https://maps.google.com/?cid={d["cid"]}" target="_blank" rel="noopener">Tüm yorumları Google'da okuyun</a></p>
  </div>
</section>

<section id="konum">
  <div class="wrap">
    <div class="sec-head">
      <div class="eyebrow">Konum</div>
      <h2>Bizi nasıl bulursunuz?</h2>
    </div>
    <div class="loc">
      <div class="map"><iframe loading="lazy" title="{esc(d["name"])} konumu" src="https://www.google.com/maps?q={urllib.parse.quote(d["maps_q"])}&z=16&output=embed"></iframe></div>
      <div class="hours">
        <h3>Çalışma saatleri</h3>
        <table id="hoursTable">
{hours_rows}
        </table>
        <p class="addr"><b>Adres</b><br>{d["addr_full"]}</p>
        <div class="btns">
          <a class="btn btn-wa" href="{waq(d["wa_text"])}" target="_blank" rel="noopener">{cta2}</a>
          <a class="btn btn-dir" href="{dir_url}" target="_blank" rel="noopener">Yol tarifi al</a>
        </div>
      </div>
    </div>
  </div>
</section>

<footer>© {esc(d["name"])} · {d["area"]}<br>Örnek tasarım, işletme adına yayınlanmamıştır.</footer>

<a class="fab" href="{waq(d["wa_text"])}" target="_blank" rel="noopener" aria-label="WhatsApp">
  {FAB_SVG}
</a>
<div class="lb" id="lb"><button class="c" aria-label="Kapat">×</button><button class="p" aria-label="Önceki">‹</button><img id="lbImg" alt="Büyük fotoğraf"><button class="n" aria-label="Sonraki">›</button></div>

<script>
(function(){{
  var S={json.dumps(sched)};
  var parts=new Intl.DateTimeFormat('en-GB',{{timeZone:'Europe/Istanbul',weekday:'short',hour:'2-digit',minute:'2-digit',hour12:false}}).formatToParts(new Date());
  var get=function(t){{return (parts.find(function(p){{return p.type===t;}})||{{}}).value;}};
  var days={{Sun:0,Mon:1,Tue:2,Wed:3,Thu:4,Fri:5,Sat:6}};
  var d=days[get('weekday')],m=parseInt(get('hour'),10)*60+parseInt(get('minute'),10);
  var r=S[String(d)],open=!!r&&m>=r[0]&&m<r[1];
  var st=document.getElementById('status');
  st.className='status '+(open?'open':'closed');
  st.querySelector('span').textContent=open?'Şu an açık':'Şu an kapalı';
  var row=document.querySelector('#hoursTable tr[data-d="'+d+'"]');if(row)row.className='today';
  var imgs=[].slice.call(document.querySelectorAll('.real-grid img')),lb=document.getElementById('lb'),big=document.getElementById('lbImg'),i=0,x0=null;
  if(!imgs.length)return;
  function show(n){{i=(n+imgs.length)%imgs.length;big.src=imgs[i].getAttribute('data-big');}}
  function close(){{lb.classList.remove('open');document.body.style.overflow='';}}
  imgs.forEach(function(im,n){{im.parentNode.addEventListener('click',function(){{show(n);lb.classList.add('open');document.body.style.overflow='hidden';}});}});
  lb.querySelector('.c').onclick=close;
  lb.querySelector('.p').onclick=function(e){{e.stopPropagation();show(i-1);}};
  lb.querySelector('.n').onclick=function(e){{e.stopPropagation();show(i+1);}};
  lb.addEventListener('click',function(e){{if(e.target===lb)close();}});
  document.addEventListener('keydown',function(e){{if(!lb.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(i-1);if(e.key==='ArrowRight')show(i+1);}});
  lb.addEventListener('touchstart',function(e){{x0=e.touches[0].clientX;}},{{passive:true}});
  lb.addEventListener('touchend',function(e){{if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>50)show(i+(dx<0?1:-1));x0=null;}});
}})();
</script>
</body>
</html>
'''
    return html

if __name__ == '__main__':
    cfg = json.load(open(sys.argv[1], encoding='utf-8'))
    out = sys.argv[2]
    open(out, 'w', encoding='utf-8').write(build(cfg))
    print('wrote', out)
