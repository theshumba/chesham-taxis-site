#!/usr/bin/env python3
"""Clean re-localise + rebrand of the Framer homepage from the pristine original.
Fixes the backtick over-capture bug that corrupted the .mjs hydration bundle."""
import os, re, ssl, json, urllib.request, urllib.parse, html as H
from collections import deque

ROOT = os.path.expanduser("~/Documents/GitHub/chesham-taxis-site")
PRISTINE = os.path.expanduser("~/Downloads/rido-template_framer_website.html")
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE
HOST = "https://framerusercontent.com"

# BACKTICK-SAFE url regex (added ` to the exclusion set) + stop at HTML entity tails
RAW = re.compile(r'https://framerusercontent\.com/[^"\'\s)\\<>`]+')
REL_MJS = re.compile(r'"(\./[^"]+\.mjs)"')

def clean(u):
    for ent in ('&#34;','&#39;','&quot;','&apos;','&gt;','&lt;','&#x22;','&#x27;'):
        i=u.find(ent)
        if i!=-1: u=u[:i]
    return u

def fetch(u): return u.replace('&amp;','&')
def local_rel(u):
    p=urllib.parse.urlparse(fetch(u)).path.lstrip('/').split('?')[0]
    return os.path.join("assets",p)

def download(u, force=False):
    lp=local_rel(u); ap=os.path.join(ROOT,lp)
    if os.path.exists(ap) and not force:
        return ap
    os.makedirs(os.path.dirname(ap),exist_ok=True)
    req=urllib.request.Request(fetch(clean(u)),headers={'User-Agent':'Mozilla/5.0'})
    open(ap,'wb').write(urllib.request.urlopen(req,context=ctx,timeout=40).read())
    return ap

html = open(PRISTINE, encoding='utf-8').read()

# ---- 1) crawl + ensure all assets local; FORCE-refresh text modules (mjs/json) ----
seen=set(); q=deque()
for m in RAW.findall(html):
    c=clean(m)
    if c not in seen: seen.add(c); q.append(c)
fresh_text=0; total=0
while q:
    u=q.popleft(); total+=1
    is_text = local_rel(u).endswith((".mjs",".css",".json"))
    ap=download(u, force=is_text)            # re-download text fresh (mjs were corrupted)
    if is_text: fresh_text+=1
    if local_rel(u).endswith((".mjs",".css",".json")):
        try: txt=open(ap,encoding='utf-8',errors='ignore').read()
        except: txt=''
        for nu in RAW.findall(txt):
            c=clean(nu)
            if c not in seen: seen.add(c); q.append(c)
        base=fetch(u).rsplit('/',1)[0]+'/'
        for rel in REL_MJS.findall(txt):
            nu=urllib.parse.urljoin(base, rel)
            if nu.startswith(HOST) and nu not in seen: seen.add(nu); q.append(nu)
print(f"assets ensured: {total} (fresh text modules: {fresh_text})")

# ---- 2) rebrand helpers (safe; applied to HTML always, to JS only in string content) ----
COLORS=[("0, 153, 255","11, 122, 55"),("0,153,255","11,122,55"),
        ("21, 9, 148","0, 91, 38"),("21,9,148","0,91,38")]
HEX=[(r'#0099ff','#0B7A37'),(r'#09f\b','#0B7A37'),(r'#150994','#005B26')]
def recolor(t):
    for a,b in COLORS: t=t.replace(a,b)
    for p,b in HEX: t=re.sub(p,b,t,flags=re.I)
    return t

# ---- 3) rewrite URLs INSIDE fresh text modules (backtick-safe) + rebrand ----
mod_fixed=0
for dp,_,fs in os.walk(os.path.join(ROOT,"assets")):
    for f in fs:
        if not f.endswith((".mjs",".css",".json")): continue
        fp=os.path.join(dp,f)
        try: t=open(fp,encoding='utf-8').read()
        except: continue
        orig=t
        if "framerusercontent.com" in t:
            for u in sorted({clean(x) for x in RAW.findall(t)}, key=len, reverse=True):
                tgt=os.path.join(ROOT,local_rel(u))
                rel=os.path.relpath(tgt, os.path.dirname(fp))
                if not rel.startswith('.'): rel='./'+rel
                t=t.replace(u,rel)
        t=recolor(t).replace("Rido","Chesham Taxis")
        if t!=orig:
            open(fp,'w',encoding='utf-8').write(t); mod_fixed+=1
print(f"modules rewritten (backtick-safe): {mod_fixed}")

# ---- 4) rewrite index.html URLs -> local (attribute URLs are quote-delimited; safe) ----
for u in sorted({clean(x) for x in RAW.findall(html)}, key=len, reverse=True):
    html=html.replace(u, "./"+local_rel(u))
# strip external analytics / phone-home
html=re.sub(r'<script[^>]*events\.framer\.com[^>]*>.*?</script>','',html,flags=re.S)
html=re.sub(r'<script[^>]*googletagmanager\.com[^>]*>.*?</script>','',html,flags=re.S)
html=re.sub(r'<script[^>]*src="https://events\.framer\.com[^"]*"[^>]*></script>','',html)

# ---- 5) rebrand text + colors + contact + logo + links (HTML) ----
html=html.replace("Rido","Chesham Taxis")
html=html.replace("rido-template.framer.website","cheshamtaxis.co.uk")
html=html.replace("+1 (800) 123-4567","01494 000000")
html=recolor(html)
# header logo -> horizontal light logo
html=html.replace("./assets/images/o2X2GkTAaY19FYAVBB1g740rNhQ.svg","./assets/logo-horizontal-light.png")
# decode entity-encoded inline <script> JS/JSON (download corrupted them)
html=re.sub(r'(<script(?![^>]*\bsrc=)[^>]*>)(.*?)(</script>)', lambda m: m.group(1)+H.unescape(m.group(2))+m.group(3), html, flags=re.S)
# decode entity-quotes inside <style> so fonts load on first paint
def fix_style(m): return m.group(0).replace('&#34;','"').replace('&#39;',"'")
html=re.sub(r'<style[^>]*>.*?</style>', fix_style, html, flags=re.S)
# inject logo sizing override + wire sub-page links
override='''<style id="chesham-logo-fix">
a:has(img[src*="logo-horizontal-light"]){width:172px!important;height:38px!important;flex:none!important}
.framer-yfdmof-container:has(img[src*="logo-horizontal-light"]){width:172px!important;height:38px!important}
img[src*="logo-horizontal-light"]{object-fit:contain!important;object-position:left center!important;width:100%!important;height:100%!important}
</style></head>'''
html=html.replace("</head>",override,1)
for s in ["about-us","taxi","services","pricing","reviews","drivers","contact-us"]:
    html=html.replace(f'href="./{s}"', f'href="./{s}.html"')

# static-safe: prevent broken hydration from wiping SSR content + reveal entrance states
html=re.sub(r'<script[^>]*type="module"[^>]*>.*?</script>','',html,flags=re.S)
html=re.sub(r'<script[^>]*type="module"[^>]*/?>','',html)
html=html.replace('</head>','<style id="force-reveal">[style*="opacity:0"],[style*="opacity: 0"]{opacity:1!important;transform:none!important}</style></head>',1)
open(os.path.join(ROOT,"index.html"),"w",encoding='utf-8').write(html)
print("index.html rebuilt:", len(html), "bytes")
print("remaining external framer urls in html:", len(set(RAW.findall(html))))
