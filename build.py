#!/usr/bin/env python3
"""Assemble Chesham Taxis sub-pages: wrap per-page <main> content in the shared shell."""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
PHONE_DISPLAY = "01494 000000"
PHONE_TEL = "+441494000000"
EMAIL = "bookings@cheshamtaxis.co.uk"

# slug -> (Title, meta description, nav-active-key)
PAGES = {
 "about-us":       ("About Us", "Meet Chesham Taxis — your friendly, reliable local taxi service across Chesham and the Chilterns.", "about"),
 "taxi":           ("Our Taxis", "Explore the Chesham Taxis fleet — saloons, estates, executive cars and people carriers for every journey.", "taxi"),
 "services":       ("Our Services", "Airport transfers, local rides, school runs, corporate accounts and more from Chesham Taxis.", "services"),
 "pricing":        ("Pricing & Fares", "Clear, fair, fixed-price taxi fares across Chesham, Buckinghamshire and beyond. No surge pricing.", "pricing"),
 "reviews":        ("Reviews", "See what Chesham locals say about their rides with Chesham Taxis.", "reviews"),
 "drivers":        ("Our Drivers", "DBS-checked, licensed, local drivers — and how to join the Chesham Taxis team.", "drivers"),
 "cars-for-rental":("Cars for Rental", "Flexible self-drive car rental from Chesham Taxis — daily, weekly and monthly.", "taxi"),
 "contact-us":     ("Contact & Book", "Book a taxi or get a quote from Chesham Taxis. Call, message or book online 24/7.", "contact"),
}

NAVLINKS = [
 ("Home","index.html","home"),
 ("About","about-us.html","about"),
 ("Our Taxis","taxi.html","taxi"),
 ("Services","services.html","services"),
 ("Pricing","pricing.html","pricing"),
 ("Reviews","reviews.html","reviews"),
]

def nav(active):
    def linktag(label, href, key):
        cls = ' class="active"' if key == active else ''
        return f'<a href="./{href}"{cls}>{label}</a>'
    links = "".join(linktag(label, href, key) for label, href, key in NAVLINKS)
    mlinks = "".join(f'<a href="./{href}">{label}</a>' for label,href,key in NAVLINKS)
    phone_svg='<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
    return f'''<header class="nav">
 <div class="container nav-in">
  <a class="brand" href="./index.html" aria-label="Chesham Taxis home"><img src="./assets/logo-horizontal-light.png" alt="Chesham Taxis"></a>
  <nav class="nav-links">{links}</nav>
  <div class="nav-cta">
   <a class="nav-phone" href="tel:{PHONE_TEL}">{phone_svg}{PHONE_DISPLAY}</a>
   <a class="btn btn-accent" href="./contact-us.html">Book your ride</a>
  </div>
  <button class="nav-toggle" aria-label="Open menu" onclick="document.getElementById('mnav').classList.toggle('open')">
   <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
  </button>
 </div>
 <div class="nav-mobile" id="mnav">{mlinks}<a class="btn btn-accent" href="./contact-us.html">Book your ride</a></div>
</header>'''

def footer():
    ig='<svg viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.6 0 4.9.07 1.2.05 1.8.25 2.2.42.6.22 1 .48 1.4.9.4.4.7.8.9 1.4.2.4.4 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c0 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .4-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2 0-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c0-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 3.2A6.6 6.6 0 1 0 18.6 12 6.6 6.6 0 0 0 12 5.4zm0 10.9A4.3 4.3 0 1 1 16.3 12 4.3 4.3 0 0 1 12 16.3zm6.8-11.1a1.5 1.5 0 1 0 1.5 1.5 1.5 1.5 0 0 0-1.5-1.5z"/></svg>'
    fb='<svg viewBox="0 0 24 24"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9 1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.3v7A10 10 0 0 0 22 12z"/></svg>'
    wa='<svg viewBox="0 0 24 24"><path d="M.1 24l1.7-6.2A11.9 11.9 0 1 1 12 24a11.9 11.9 0 0 1-5.7-1.5L.1 24zM6.6 20l.4.2A9.9 9.9 0 1 0 3.6 17l.2.4-1 3.6 3.8-1zM17.5 14.3c-.1-.2-.5-.4-1-.6s-1.5-.7-1.7-.8-.4-.1-.5.2-.6.8-.8.9-.3.2-.5 0a8 8 0 0 1-2.4-1.5 9 9 0 0 1-1.7-2.1c-.2-.3 0-.4.1-.6l.4-.4.3-.5v-.5l-.7-1.8c-.2-.5-.4-.4-.5-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.9 11.9 0 0 0 4.6 4 5.3 5.3 0 0 0 3.2.7 2.7 2.7 0 0 0 1.8-1.3 2.2 2.2 0 0 0 .2-1.3z"/></svg>'
    return f'''<footer class="foot">
 <div class="container">
  <div class="foot-top">
   <div class="foot-brand">
    <img src="./assets/logo-horizontal-light.png" alt="Chesham Taxis">
    <p>Your friendly, reliable local taxi service across Chesham, Amersham and the Chilterns — 24 hours a day, every day.</p>
    <div class="foot-social" style="margin-top:18px">
     <a href="#" aria-label="WhatsApp">{wa}</a><a href="#" aria-label="Facebook">{fb}</a><a href="#" aria-label="Instagram">{ig}</a>
    </div>
   </div>
   <div><h4>Company</h4><ul>
    <li><a href="./about-us.html">About us</a></li>
    <li><a href="./drivers.html">Our drivers</a></li>
    <li><a href="./reviews.html">Reviews</a></li>
    <li><a href="./contact-us.html">Contact</a></li>
   </ul></div>
   <div><h4>Services</h4><ul>
    <li><a href="./services.html">Airport transfers</a></li>
    <li><a href="./services.html">Local &amp; town rides</a></li>
    <li><a href="./taxi.html">Our taxis</a></li>
    <li><a href="./cars-for-rental.html">Cars for rental</a></li>
   </ul></div>
   <div><h4>Get in touch</h4><ul>
    <li><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a></li>
    <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
    <li>Chesham, Buckinghamshire</li>
    <li>Open 24/7, 365 days</li>
   </ul></div>
  </div>
  <div class="foot-bottom">
   <span>© 2026 Chesham Taxis. All rights reserved.</span>
   <span>Licensed by Buckinghamshire Council · Fully insured</span>
  </div>
 </div>
</footer>'''

SCRIPTS = '''<script>
// mobile menu auto-close + reveal on scroll
document.querySelectorAll('.nav-mobile a').forEach(a=>a.addEventListener('click',()=>document.getElementById('mnav').classList.remove('open')));
const io=new IntersectionObserver((es)=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
</script>'''

def head(title, desc, slug):
    return f'''<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Chesham Taxis</title>
<meta name="description" content="{desc}">
<link rel="icon" href="./assets/logo-bird.png" type="image/png">
<meta property="og:title" content="{title} · Chesham Taxis">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#1E4927">
<link rel="stylesheet" href="./assets/site.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"TaxiService","name":"Chesham Taxis","areaServed":"Chesham, Buckinghamshire","telephone":"{PHONE_TEL}","email":"{EMAIL}","url":"https://cheshamtaxis.co.uk","availableLanguage":"English"}}</script>
</head><body>'''

def build_home():
    cpath=os.path.join(ROOT,"content","index.html")
    if not os.path.exists(cpath):
        print("  SKIP index (no content)"); return
    main=open(cpath,encoding="utf-8").read().strip()
    title="Chesham Taxis — Local Taxis &amp; Airport Transfers in Chesham"
    desc="Friendly, reliable 24/7 taxis across Chesham, Amersham and the Chilterns. Fixed fares, airport transfers, local rides and executive cars. Call 01494 000000."
    h=head(title,desc,"index").replace(f"<title>{title} · Chesham Taxis</title>", f"<title>{title}</title>")
    html=h+nav("home")+"\n"+main+"\n"+footer()+SCRIPTS+"\n</body></html>"
    open(os.path.join(ROOT,"index.html"),"w",encoding="utf-8").write(html)
    print(f"  built index.html ({len(html)//1024}kb)")

def build():
    build_home()
    cdir=os.path.join(ROOT,"content")
    built=[]
    for slug,(title,desc,active) in PAGES.items():
        cpath=os.path.join(cdir,f"{slug}.html")
        if not os.path.exists(cpath):
            print(f"  SKIP {slug} (no content yet)"); continue
        main=open(cpath,encoding="utf-8").read().strip()
        html=head(title,desc,slug)+nav(active)+"\n"+main+"\n"+footer()+SCRIPTS+"\n</body></html>"
        out=os.path.join(ROOT,f"{slug}.html")
        open(out,"w",encoding="utf-8").write(html)
        built.append(slug)
        print(f"  built {slug}.html ({len(html)//1024}kb)")
    print(f"DONE: {len(built)} pages")
    return built

if __name__=="__main__":
    build()
