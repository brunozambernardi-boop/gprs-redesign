#!/usr/bin/env python3
"""Builds the static GPRS redesign preview. Content comes only from the current site
(greatpyreneesrescuesociety.org, audited Nov 23 2026). Yellow [..] marks = info the org must supply."""
import json, re, html, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RG = "https://gprs.rescuegroups.org"
L = dict(
  apply=RG+"/forms/form?formid=6206", contract=RG+"/forms/form?formid=6216",
  foster_app=RG+"/forms/form?formid=6281", foster_contract=RG+"/forms/form?formid=1686",
  volunteer=RG+"/forms/form?formid=6272", surrender=RG+"/forms/form?formid=2015",
  hw=RG+"/forms/form?formid=5452", forms=RG+"/forms", alldogs=RG+"/animals/browse?Species=Dog",
  paypal="https://www.paypal.com/donate/?hosted_button_id=TGUHEX5CQDQXJ",
  amazon="https://www.amazon.com/hz/wishlist/ls/1N7H1YOJ8RPEN",
  merch="https://www.bonfire.com/store/gprs/", fb="https://www.facebook.com/rescuegreatpyrs",
  ig="https://www.instagram.com/GreatPyreneesRescueSocietyinc/", yt="https://www.youtube.com/@gprspyrs",
  email="info@greatpyreneesrescuesociety.org", natpyr="https://nationalpyr.org/contacts/",
  bluebonnet="https://www.bluebonnetanimalrescue.org/", akc="https://www.akc.org/dog-breeds/great-pyrenees/",
  trupanion="http://trupanion.go2cloud.org/aff_c?offer_id=2&aff_id=2433", peaceable="https://www.peaceablepaws.com",
)
def ph(t): return f'<span class="ph">[{t}]</span>'
EXT = 'target="_blank" rel="noopener"'

dogs = json.load(open(os.path.join(ROOT, "tools/dogs.json")))
def short_age(a):
    m = re.match(r"(\d+) Years?", a); 
    if m: return f"{m.group(1)} yr" + ("s" if m.group(1)!="1" else "")
    m = re.match(r"(\d+) Months?", a)
    return f"{m.group(1)} mo" if m else a
def state(loc):
    m = re.search(r"\b([A-Z]{2})\b \d{5}", loc); return m.group(1) if m else ""
def clean_desc(d):
    t = (d.get("desc2") or "").lstrip(". ").strip()
    if not t:
        t = re.sub(r"\*\*\s*Tune in.*?(\*\*|$)", "", d["desc"], flags=re.S|re.I).strip()
    if len(t) < 40: t = f"Read {d['name'].split(',')[0]}'s full story, photos and adoption details on their profile. More to come"
    return t
clean = []
for d in dogs:
    clean.append(dict(id=d["id"], name=d["name"], breed=re.sub(r" \((long|medium|short) coat\)","",d["breed"]),
      sex=d["sex"], age=short_age(d["age"]), group=d["ageGroup"], fee=d["fee"], weight=d["weight"].replace(" Pounds"," lbs"),
      loc=re.sub(r" \d{5}$","",d["location"]) if state(d["location"]) else "", st=state(d["location"]),
      pyr="Great Pyrenees" in d["breed"], img=f"img/dogs/{d['id']}.jpg",
      url=f"{RG}/animals/detail?AnimalID={d['id']}", desc=clean_desc(d)))
open(os.path.join(ROOT,"assets/dogs.js"),"w").write("window.GPRS_DOGS="+json.dumps(clean)+";\nwindow.GPRS_DOGS_UPDATED='Nov 23, 2026';\n")

def dog_card(d, lazy=True):
    tags = f'<span class="tag">{d["group"] or "Adult"}</span><span class="tag">{d["sex"]}</span>'
    if "bonded" in d["name"].lower(): tags += '<span class="tag red">Bonded pair</span>'
    meta = " · ".join(x for x in [d["breed"], d["age"], d["weight"], d["loc"]] if x)
    return f'''<article class="dog"><a href="{d["url"]}" {EXT} tabindex="-1" aria-hidden="true"><img src="{d["img"]}" alt="{html.escape(d["name"])}, {html.escape(d["breed"])}" {'loading="lazy"' if lazy else ''} width="400" height="400"></a>
<div class="body"><div class="tags">{tags}</div><h3>{html.escape(d["name"])}</h3><div class="meta">{html.escape(meta)}</div>
<p>{html.escape(d["desc"][:170].rsplit(" ",1)[0])}…</p><div class="actions"><a class="btn btn-primary btn-sm" href="{d["url"]}" {EXT}>Meet {html.escape(d["name"].split(",")[0])}</a></div></div></article>'''

NAV = [("index.html","Home"),("adopt.html","Adopt"),("process.html","How to adopt"),("foster.html","Foster"),
       ("volunteer.html","Volunteer"),("breed.html","The breed"),("about.html","About"),("contact.html","Contact")]
def page(fn, title, desc, body):
    nav = "".join(f'<li><a href="{h}"{" aria-current=page" if h==fn else ""}>{t}</a></li>' for h,t in NAV)
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:image" content="img/og-logo.jpg"><meta property="og:type" content="website">
<link rel="icon" href="img/favicon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"NGO","name":"Great Pyrenees Rescue Society","alternateName":"GPRS","foundingDate":"2006","email":"{L['email']}","address":{{"@type":"PostalAddress","addressLocality":"Spring","addressRegion":"TX","postalCode":"77388","addressCountry":"US"}},"sameAs":["{L['fb']}","{L['ig']}","{L['yt']}"]}}</script>
</head><body><a class="skip" href="#main">Skip to content</a>
<div class="topbar">Watch our dogs <b>live on Facebook every Sunday at 3pm CT</b>. <a href="{L['fb']}" {EXT}>Tune in →</a></div>
<header class="site"><div class="wrap nav"><a class="brand" href="index.html"><img src="img/logo.png" alt="" width="52" height="52"><span><b>Great Pyrenees<br>Rescue Society</b><small>Est. 2006 · 501(c)(3) · Texas</small></span></a>
<button class="menu-toggle" aria-expanded="false" aria-controls="menu">Menu</button>
<ul class="menu" id="menu">{nav}<li><a class="btn btn-donate btn-sm" href="donate.html">Donate</a></li></ul></div></header>
<main id="main">{body}</main>
<footer class="site"><div class="wrap"><div class="fgrid">
<div><div class="fbrand"><img src="img/logo.png" alt="" width="56" height="56"><b>Great Pyrenees<br>Rescue Society</b></div>
<p>A volunteer-run, foster-based 501(c)(3) rescue saving Great Pyrenees in Texas since 2006. 100% of donations go to the dogs.</p>
<p>EIN: {ph("Add EIN")}</p>
<div class="social"><a href="{L['fb']}" {EXT}>Facebook</a><a href="{L['ig']}" {EXT}>Instagram</a><a href="{L['yt']}" {EXT}>YouTube</a></div></div>
<div><h4>Adopt</h4><ul><li><a href="adopt.html">Available dogs</a></li><li><a href="process.html">Adoption process</a></li><li><a href="{L['apply']}" {EXT}>Adoption application</a></li><li><a href="breed.html">About the breed</a></li></ul></div>
<div><h4>Help</h4><ul><li><a href="foster.html">Foster</a></li><li><a href="volunteer.html">Volunteer</a></li><li><a href="donate.html">Donate</a></li><li><a href="{L['merch']}" {EXT}>Merch store</a></li><li><a href="{L['forms']}" {EXT}>All forms</a></li></ul></div>
<div><h4>Contact</h4><ul><li><a href="mailto:{L['email']}">{L['email']}</a></li><li>Spring, TX 77388</li><li><a href="{L['fb']}" {EXT}>Message us on Facebook</a></li><li><a href="contact.html#surrender">Owner surrender</a></li></ul></div>
</div><div class="legal"><span>© 2026 Great Pyrenees Rescue Society. Spay and neuter your pets.</span><span>Dog listings powered by RescueGroups.org</span></div></div></footer>
<script>const t=document.querySelector('.menu-toggle'),m=document.getElementById('menu');t.addEventListener('click',()=>{{const o=m.classList.toggle('open');t.setAttribute('aria-expanded',o)}});</script>
</body></html>'''

def write(fn, title, desc, body):
    open(os.path.join(ROOT, fn), "w").write(page(fn, title, desc, body))

by = {d["id"]: d for d in clean}
featured = [by[i] for i in ["21177255","22486521","22151962","17373586","21270007","15785859"]]
FEES = sorted({int(x) for d in dogs for x in re.findall(r"\$(\d+)", d["fee"])})
FEE_RANGE = f"${FEES[0]}–${FEES[-1]}"
N = len(clean)

ADOPT_STEPS = f'''<ol class="steps">
<li><h3>Apply online</h3><p>Four short sections: about you, your home, yard and vet, your pets, and the dog you love. A volunteer contacts you within 3–4 days.</p></li>
<li><h3>Let's talk</h3><p>A screener reviews your application, talks with you about possible matches, and lets you know if you're approved.</p></li>
<li><h3>Sign the contract</h3><p>Once approved, you complete the adoption contract. We email an invoice for the adoption fee. Pay by card, PayPal, Zelle or Venmo.</p></li>
<li><h3>Bring your Pyr home</h3><p>Local pickup, or we arrange transport with an experienced pet transport provider. You can also arrange your own.</p></li></ol>'''

# ---------------- HOME ----------------
write("index.html", "Great Pyrenees Rescue Society | Adopt a Gentle Giant in Texas",
 "Volunteer-run, foster-based 501(c)(3) rescue saving Great Pyrenees from Texas shelters since 2006. Adopt, foster, volunteer or donate.", f'''
<section class="hero"><div class="wrap hero-grid"><div>
<span class="eyebrow">Rescuing Great Pyrenees since 2006</span>
<h1>Every gentle giant deserves a soft place to land.</h1>
<p class="lead">We pull Great Pyrenees from kill shelters across Central Texas, South Texas and Greater Houston, care for them in loving foster homes, and match them with families in Texas and the West.</p>
<div class="btns"><a class="btn btn-primary" href="adopt.html">Meet the dogs</a><a class="btn btn-ghost" href="foster.html">Become a foster</a></div>
<ul class="trust-row"><li>501(c)(3) nonprofit</li><li>100% volunteer-run</li><li>100% of donations go to the dogs</li></ul>
</div><figure class="hero-photo"><img src="img/hero-sir-kingsley.jpg" alt="Sir Kingsley, a white Great Pyrenees, smiling outdoors" width="1000" height="1148" fetchpriority="high">
<figcaption><b>Sir Kingsley</b>Looking for his family. <a href="{by['21177255']['url']}" {EXT}>Meet him →</a></figcaption></figure></div></section>

<section class="alt" aria-labelledby="impact"><div class="wrap">
<div class="section-head"><span class="eyebrow">Our impact</span><h2 id="impact">Founded in 2006. Still saving lives every week.</h2></div>
<div class="stats">
<div class="stat"><b>{N}</b><span>dogs available for adoption right now</span></div>
<div class="stat"><b>2006</b><span>the year Malise Saucier founded GPRS</span></div>
<div class="stat"><b>{ph("Add number")}</b><span>dogs rescued and adopted since 2006</span></div>
<div class="stat"><b>{ph("Add number")}</b><span>active foster homes in TX and the Pacific NW</span></div>
</div></div></section>

<section aria-labelledby="feat"><div class="wrap">
<div class="section-head"><span class="eyebrow">Available now</span><h2 id="feat">Meet a few of our dogs</h2><p class="lead">Every dog lives in a foster home, so we can tell you how they really are with people, other dogs and everyday life.</p></div>
<div class="dogs">{"".join(dog_card(d) for d in featured)}</div>
<div class="btns"><a class="btn btn-primary" href="adopt.html">See all {N} dogs</a><a class="btn btn-ghost" href="{L['apply']}" {EXT}>Start an application</a></div></div></section>

<section class="sand" aria-labelledby="how"><div class="wrap">
<div class="section-head"><span class="eyebrow">How adoption works</span><h2 id="how">Four simple steps to your new best friend</h2><p class="lead">Adoption fees are {FEE_RANGE} and are listed on each dog's profile. Every dog is vaccinated, including rabies, and spayed or neutered.</p></div>
{ADOPT_STEPS}<div class="btns"><a class="btn btn-primary" href="{L['apply']}" {EXT}>Apply to adopt</a><a class="btn btn-ghost" href="process.html">Process and FAQ</a></div></div></section>

<section aria-labelledby="breed"><div class="wrap split">
<img src="img/puppy-banner.jpg" alt="A fluffy white Great Pyrenees puppy lying in the grass" width="540" height="400">
<div><span class="eyebrow">Is a Pyr right for you?</span><h2 id="breed">The Gentle Giant</h2>
<p>Great Pyrenees are wonderful, loyal family dogs: even-tempered, affectionate, and especially fond of children. They are also independent thinkers who need consistent training. Before you fall in love, here's what to know:</p>
<ul class="checks"><li>They shed all year, and they can shed a lot.</li><li>They bark. They were bred to guard livestock.</li><li>They like to roam, so secure fencing is a must. Most of our dogs need a 6-foot fence.</li><li>They live about 10–12 years and weigh 85–110+ lbs as adults.</li></ul>
<a class="btn btn-ghost" href="breed.html">Read the breed guide</a></div></div></section>

<section class="alt" aria-labelledby="help"><div class="wrap">
<div class="section-head center"><span class="eyebrow">Can't adopt right now?</span><h2 id="help">There are many ways to save a Pyr</h2><p class="lead">There are far more Great Pyrenees in Texas shelters than we have room for. Fosters, volunteers and donors are how we say yes to more of them.</p></div>
<div class="grid g3">
<div class="card"><div class="icon" aria-hidden="true">🏡</div><h3>Foster</h3><p>The most valuable thing you can do. We can't pull a dog from a shelter without a foster home. We cover vet care, vaccinations and medications.</p><a href="foster.html">Learn about fostering →</a></div>
<div class="card"><div class="icon" aria-hidden="true">🤝</div><h3>Volunteer</h3><p>Help with transport, dog walking or grooming in Spring, TX, or pick a remote role like shelter liaison, grant writing or listings.</p><a href="volunteer.html">See volunteer roles →</a></div>
<div class="card"><div class="icon" aria-hidden="true">❤️</div><h3>Donate</h3><p>Nine times out of ten, a new dog needs medical care. Every dollar goes straight to the dogs.</p><a href="donate.html">Ways to give →</a></div>
</div></div></section>

<section aria-labelledby="stories"><div class="wrap">
<div class="section-head"><span class="eyebrow">Happy tails</span><h2 id="stories">From shelter to sofa</h2></div>
<div class="grid g3">
<div class="card"><p>“{ph("Add a real quote from an adopter, with their permission")}”</p><p class="muted">— {ph("Adopter first name, city, dog's name")}</p></div>
<div class="card"><p>“{ph("Add a real quote from a foster family")}”</p><p class="muted">— {ph("Foster first name, city")}</p></div>
<div class="card"><p>“{ph("Add a real quote from an adopter in the Pacific NW")}”</p><p class="muted">— {ph("Adopter first name, city, dog's name")}</p></div>
</div></div></section>

<section aria-label="Donate"><div class="wrap"><div class="band red">
<div><h2>Your gift becomes vet care, food and a ride to safety.</h2><p>We're an all-volunteer organization, so 100% of donations go directly to the dogs in our care.</p></div>
<div class="btns" style="margin:0"><a class="btn btn-light" href="{L['paypal']}" {EXT}>Donate with PayPal</a><a class="btn btn-ghost" style="border-color:#fff;color:#fff" href="donate.html">Other ways to give</a></div>
</div></div></section>
''')

# ---------------- ADOPT ----------------
write("adopt.html", "Adopt a Great Pyrenees | Available Dogs | GPRS",
 f"Browse {N} Great Pyrenees and Pyr mixes available for adoption from Great Pyrenees Rescue Society.", f'''
<section class="page-hero"><div class="wrap"><span class="eyebrow">Available dogs</span><h1>Find your Pyr-fect match</h1>
<p class="lead">Each dog has a personality and preferences of their own, so we match dogs with families thoughtfully. Browse below, then open a profile for the full story, photos and adoption fee.</p>
<div class="btns"><a class="btn btn-primary" href="{L['apply']}" {EXT}>Start your application</a><a class="btn btn-ghost" href="process.html">How adoption works</a></div></div></section>
<section style="padding-top:20px"><div class="wrap">
<div class="notice">Listings come from our RescueGroups.org database (snapshot from <span id="upd"></span>). For live, up-to-the-minute availability, see the <a href="{L['alldogs']}" {EXT}>full list</a>. {ph("Developer: connect the RescueGroups API so this page updates automatically")}</div>
<form class="filters" id="filters" onsubmit="return false"><label>Search<input id="q" type="search" placeholder="Name or breed"></label>
<label>Age<select id="age"><option value="">Any age</option><option>Baby</option><option>Young</option><option>Adult</option><option>Senior</option></select></label>
<label>Sex<select id="sex"><option value="">Any</option><option>Female</option><option>Male</option></select></label>
<label>Breed<select id="pyr"><option value="">All dogs</option><option value="1">Great Pyrenees &amp; Pyr mixes</option><option value="0">Other breeds</option></select></label>
<label>Located in<select id="st"><option value="">Anywhere</option></select></label><span class="count" id="count" aria-live="polite"></span></form>
<div class="dogs" id="dogs"></div>
<noscript><p>See all dogs on <a href="{L['alldogs']}">our RescueGroups listing</a>.</p></noscript>
</div></section>
<section class="sand"><div class="wrap split"><img src="img/foster-puppy.jpg" alt="A happy Great Pyrenees puppy on a hammock" loading="lazy">
<div><span class="eyebrow">Not sure yet?</span><h2>Try foster-to-adopt</h2><p>If you're not sure you're ready to adopt permanently, you can foster first. The dog lives with you until they're adopted, and if you fall in love, you can apply to adopt them before anyone else is approved.</p><a class="btn btn-ghost" href="foster.html">Learn about fostering</a></div></div></section>
<script src="assets/dogs.js"></script>
<script>
const D=window.GPRS_DOGS,el=id=>document.getElementById(id),esc=s=>s.replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]));
el('upd').textContent=window.GPRS_DOGS_UPDATED;
[...new Set(D.map(d=>d.st).filter(Boolean))].sort().forEach(s=>el('st').insertAdjacentHTML('beforeend',`<option>${{s}}</option>`));
function card(d){{const tags=`<span class="tag">${{d.group||'Adult'}}</span><span class="tag">${{d.sex}}</span>`+(/bonded/i.test(d.name)?'<span class="tag red">Bonded pair</span>':'');
const meta=[d.breed,d.age,d.weight,d.loc].filter(Boolean).join(' · ');const fee=d.fee?` · Fee ${{esc(d.fee)}}`:'';
return `<article class="dog"><a href="${{d.url}}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true"><img src="${{d.img}}" alt="${{esc(d.name)}}, ${{esc(d.breed)}}" loading="lazy" width="400" height="400"></a><div class="body"><div class="tags">${{tags}}</div><h3>${{esc(d.name)}}</h3><div class="meta">${{esc(meta)}}${{fee}}</div><p>${{esc(d.desc.slice(0,160).replace(/\\s\\S*$/,''))}}…</p><div class="actions"><a class="btn btn-primary btn-sm" href="${{d.url}}" target="_blank" rel="noopener">Meet ${{esc(d.name.split(',')[0])}}</a></div></div></article>`}}
function render(){{const q=el('q').value.toLowerCase(),a=el('age').value,s=el('sex').value,p=el('pyr').value,st=el('st').value;
const r=D.filter(d=>(!q||(d.name+' '+d.breed).toLowerCase().includes(q))&&(!a||d.group===a)&&(!s||d.sex===s)&&(!p||String(+d.pyr)===p)&&(!st||d.st===st));
el('dogs').innerHTML=r.map(card).join('')||'<p>No dogs match those filters. Try widening your search.</p>';el('count').textContent=r.length+' of '+D.length+' dogs';}}
el('filters').addEventListener('input',render);render();
</script>''')

# ---------------- PROCESS / FAQ ----------------
write("process.html", "How to Adopt | Adoption Process & FAQ | GPRS",
 "The Great Pyrenees Rescue Society adoption process: apply, talk with a screener, sign the contract, bring your Pyr home.", f'''
<section class="page-hero"><div class="wrap"><span class="eyebrow">Adoption process</span><h1>How to adopt from GPRS</h1>
<p class="lead">Thank you for wanting to adopt a Great Pyrenees rescue. When you adopt a Pyr, you're adding a valuable member to your family. We'd love to get to know you before moving forward.</p></div></section>
<section style="padding-top:10px"><div class="wrap">{ADOPT_STEPS}
<div class="btns"><a class="btn btn-primary" href="{L['apply']}" {EXT}>Fill out the adoption application</a></div></div></section>
<section class="alt"><div class="wrap split" style="align-items:start">
<div><span class="eyebrow">Before you apply</span><h2>What to expect</h2>
<ul class="checks">
<li><b>Fees:</b> {FEE_RANGE} depending on the dog (bonded pairs are listed together). The exact fee is on each dog's profile.</li>
<li><b>Fencing:</b> We require secure, visible fencing. Most of our dogs need a 6-foot fence. Pyrs naturally roam.</li>
<li><b>Renters:</b> We'll ask for your landlord's contact details and approval for a large-breed dog.</li>
<li><b>Vet reference:</b> Have your veterinarian's name and phone number ready.</li>
<li><b>Vetting included:</b> Vaccinations, including rabies, plus spay or neuter.</li>
<li><b>Payment:</b> Credit card or PayPal through the invoice link. Zelle and Venmo also accepted. Ask your screener.</li></ul></div>
<div class="card"><h3>After you submit</h3><p>Click "Complete the Form" at the bottom of the application. You'll land on your My Rescue page, where you can review and print your application, and you'll receive a confirmation email.</p>
<p>A volunteer will contact you within <b>3 to 4 days</b>. Please check your spam or junk folder in case our email gets misdirected.</p>
<p class="callout"><b>Please don't fill out the adoption contract until a screener tells you to.</b> When you're approved, use the <a href="{L['contract']}" {EXT}>adoption contract</a>.</p></div>
</div></section>
<section><div class="narrow"><span class="eyebrow">FAQ</span><h2>Common questions</h2>
<details class="faq"><summary>I have certain preferences. Can you help me find the right dog?</summary><div class="a">Yes. While every dog is adoptable, every dog is different, with their own personality and preferences. That's why we match certain dogs with certain owners. Browse our <a href="adopt.html">available dogs</a> for details on each one, and tell your screener what you're looking for.</div></details>
<details class="faq"><summary>Do you have puppies or younger dogs?</summary><div class="a">We have both <a href="{RG}/animals/browse?special=puppy" {EXT}>puppies</a> and <a href="{RG}/animals/browse?special=teens" {EXT}>teens</a>. Puppies haven't fully developed their personalities yet. Just like children, they grow and change. A teen dog gives you the playfulness of a puppy with a better sense of who they are.</div></details>
<details class="faq"><summary>Why do Pyrenees puppies need an adult dog in the home?</summary><div class="a">Great Pyrenees learn their role from other dogs, not from people. Older dogs teach appropriate dog interaction and socialization, including that biting hurts. Without proper socialization as puppies, they can become very difficult teens and adults.</div></details>
<details class="faq"><summary>Can I foster to adopt?</summary><div class="a">Yes. As a foster, the dog stays with you until someone adopts them. If you decide you want to keep your foster dog, contact us as soon as possible so you can apply before anyone else is approved. <a href="foster.html">Learn about fostering</a>.</div></details>
<details class="faq"><summary>I don't live in Texas. Can I still adopt?</summary><div class="a">Yes. We transport and adopt dogs to Washington, Oregon, Idaho, California, New Mexico and Arizona, along with Texas. We're happy to arrange transport through one of our experienced pet transport providers, and many of our dogs have already traveled to the Pacific Northwest. You're also welcome to arrange your own transport.</div></details>
<details class="faq"><summary>Can I adopt a livestock guardian dog from you?</summary><div class="a">No. Our Pyrenees and Pyr mixes were surrendered because they weren't good with livestock, or were strays found wandering away from their livestock, so we can't safely place them in livestock homes. Our dogs live in foster homes where they learn to be house dogs. For a working dog, we highly recommend <a href="{L['bluebonnet']}" {EXT}>Bluebonnet Animal Rescue</a>, a Texas rescue that specializes in livestock guardian dogs for hobby farms and small livestock homes.</div></details>
<details class="faq"><summary>What about pet insurance?</summary><div class="a">Your current site links to Trupanion pet insurance, but that affiliate link is broken. {ph("Add an updated Trupanion or other pet-insurance referral link, or remove this question")}</div></details>
</div></section>
<section><div class="wrap"><div class="band"><div><h2>Ready to meet your gentle giant?</h2><p>Browse the dogs, then start your application.</p></div>
<div class="btns" style="margin:0"><a class="btn btn-light" href="adopt.html">See available dogs</a><a class="btn btn-ghost" style="border-color:#fff;color:#fff" href="{L['apply']}" {EXT}>Apply now</a></div></div></div></section>''')

# ---------------- FOSTER ----------------
write("foster.html", "Foster a Great Pyrenees | GPRS",
 "Fostering is the most valuable thing you can do in rescue. GPRS covers vet care, vaccinations and medications.", f'''
<section class="page-hero"><div class="wrap split"><div><span class="eyebrow">Foster</span><h1>Foster a dog. Save a life.</h1>
<p class="lead">Fostering is the single most valuable thing you can do in rescue. We can only save these majestic dogs if we have a temporary home for them while we find their permanent one.</p>
<div class="btns"><a class="btn btn-primary" href="{L['foster_app']}" {EXT}>Apply to foster</a><a class="btn btn-ghost" href="#faq">Foster FAQ</a></div></div>
<img src="img/foster-puppy.jpg" alt="A smiling Great Pyrenees puppy in a foster home's backyard" width="960" height="540"></div></section>
<section class="alt"><div class="wrap"><div class="section-head"><h2>Why it matters</h2>
<p class="lead">When you open your home to a desperate dog, you give them love and security. In return, you get to watch them grow, gain confidence and bloom into a great companion. You started out rescuing the dog, but often it's the dog that rescues you.</p>
<p>It isn't always easy, and sometimes it's downright inconvenient. But when you see them walk off into the sunset with their new family, it's always worth it.</p></div>
<div class="grid g4">
<div class="card"><div class="icon" aria-hidden="true">🩺</div><h3>Vet care covered</h3><p>All vaccinations including rabies, spay/neuter, and approved treatment at GPRS vets.</p></div>
<div class="card"><div class="icon" aria-hidden="true">💊</div><h3>Medications provided</h3><p>Any medications the dog is on when it arrives are provided by GPRS.</p></div>
<div class="card"><div class="icon" aria-hidden="true">🥣</div><h3>Food if you need it</h3><p>Pyrs have slow metabolisms and eat less than you'd think. Food can be provided if you require it.</p></div>
<div class="card"><div class="icon" aria-hidden="true">📞</div><h3>Real support</h3><p>Your contract includes phone numbers to call. Our dog coordinator is there if problems come up.</p></div>
</div></div></section>
<section><div class="wrap"><div class="section-head"><h2>How fostering works</h2></div><ol class="steps">
<li><h3>Apply</h3><p>Fill out the foster application so we can learn about your family and home.</p></li>
<li><h3>Get matched</h3><p>We match you with a foster dog that suits your family and home.</p></li>
<li><h3>Sign the contract</h3><p>Once approved, complete the <a href="{L['foster_contract']}" {EXT}>foster contract</a>. The dog remains GPRS's while in your care.</p></li>
<li><h3>Love them forward</h3><p>The dog lives with you as family until we find their permanent home.</p></li></ol></div></section>
<section class="sand" id="faq"><div class="narrow"><h2>Foster FAQ</h2>
<details class="faq"><summary>What do I feed a foster dog?</summary><div class="a">If you have other dogs, you can feed your foster the same food. Great Pyrenees are giant breed dogs with surprisingly slow metabolisms, so they usually need less food than people imagine. It's better to feed an adult twice a day rather than all at once. Food can be provided if you need it.</div></details>
<details class="faq"><summary>Are shots and medical care included?</summary><div class="a">Yes. Your foster dog gets all vaccinations, including rabies, and is spayed or neutered at GPRS vets, paid for by GPRS. Any medications the dog is on when it comes to you are provided.</div></details>
<details class="faq"><summary>What if my foster dog develops a medical problem?</summary><div class="a">Call our dog coordinator. They'll decide with you whether the dog needs to see one of our approved vets, and direct you to the closest one. Once the dog has been seen and treatment is approved by GPRS, we pay for it.</div></details>
<details class="faq"><summary>What if I want to adopt my foster dog?</summary><div class="a">Contact us as soon as possible so you can apply before anyone else is approved. We'll remove the dog from the website, you complete the adoption contract and pay the adoption fee, and your new baby becomes yours.</div></details>
<details class="faq"><summary>Where do you need fosters?</summary><div class="a">We have foster homes in Texas and the Pacific Northwest (Oregon and Washington). The need in Texas is greatest. Many times we can't pull a dog from a shelter without a foster home lined up.</div></details>
</div></section>
<section><div class="wrap"><div class="band"><div><h2>We need more people to step up.</h2><p>The same fosters care for dogs over and over again. Too many Pyrs in Texas shelters wait for someone to say yes. Will you?</p></div><div class="btns" style="margin:0"><a class="btn btn-light" href="{L['foster_app']}" {EXT}>Apply to foster</a></div></div></div></section>''')

# ---------------- VOLUNTEER ----------------
roles = [("Shelter Liaison","5–10 hrs/wk","Call shelters about dogs in danger and keep the group updated on their status."),
("Foster Liaison","5–10 hrs/wk","Keep tabs on fosters and their needs. Help track vetting, collect dog photos, and find out what adopters need to know."),
("Vet Liaison","1–2 hrs/wk","Contact vet offices to explore relationships and discounted pricing."),
("Adopter Liaison","10+ hrs/wk","Check in with adoptive families, provide support and resources, and share updates and pictures."),
("Transport Coordinator","3–5 hrs/wk","Coordinate transport of dogs to airports and other locations for out-of-state adoptions."),
("Volunteer Coordinator","3–5 hrs/wk","Arrange volunteers for events and to help foster homes with many dogs."),
("Public Relations","3–5 hrs/wk","Community outreach and education through events, advertising and media."),
("Website Coordinator","1–3 hrs/wk","Maintain the website front page by posting new stories and other tasks."),
("Internet Research","5–10 hrs/wk","Research medical conditions, medicine costs, dog supplies and other topics."),
("Listing Coordinator","3–5 hrs/wk","Polish write-ups from fosters and coordinate listings with our pet portal updater."),
("Fundraiser","5–10 hrs/wk","Come up with creative ideas to raise money, then put them into action."),
("Grant Writer","1–3 hrs/wk","Complete grant applications to agencies that fund rescue work."),
("Pet Supplier Liaison","3–5 hrs/wk","Contact pet companies for donations or discounts on flea and worm treatments, crates, food and more.")]
write("volunteer.html", "Volunteer | Great Pyrenees Rescue Society",
 "Volunteer with GPRS in Spring, Texas or remotely: transport, dog walking, grooming, shelter liaison, grant writing and more.", f'''
<section class="page-hero"><div class="wrap"><span class="eyebrow">Get involved</span><h1>Lend a hand to a Gentle Giant</h1>
<p class="lead">Even if now isn't the right time to bring home a Pyr of your own, there are so many ways to help, and many of them can be done remotely. Bring your talents, gain experience, and help a dog's dream of a permanent home come true.</p>
<div class="btns"><a class="btn btn-primary" href="{L['volunteer']}" {EXT}>Fill out the volunteer form</a></div></div></section>
<section style="padding-top:10px"><div class="wrap split" style="align-items:start"><div><h2>Hands-on in Spring, Texas</h2><p>Want to work directly with our beautiful Great Pyrenees? We have positions right here in Spring, TX:</p>
<ul class="checks"><li>Pet transport</li><li>Dog walking</li><li>Kennel duty</li><li>Grooming and bathing</li></ul></div>
<div class="card"><h3>Remote or near you</h3><p>Whether you live far away or nearby, we have volunteer work in Texas and remote options, from liaison roles to creative and marketing work.</p><p>Fill out our form and we'll get back to you about what's available.</p><a class="btn btn-primary btn-sm" href="{L['volunteer']}" {EXT}>Volunteer form</a></div></div></section>
<section class="alt"><div class="wrap"><div class="section-head"><h2>Open roles</h2><p class="lead">Time estimates are per week.</p></div>
<div class="grid g3">{"".join(f'<div class="role"><span class="hrs">{h}</span><h3>{n}</h3><p>{d}</p></div>' for n,h,d in roles)}</div></div></section>
<section><div class="wrap"><div class="band"><div><h2>Upcoming events</h2><p>Watch our dogs live on Facebook every Sunday at 3pm CT. Past episodes are on YouTube. {ph("Add upcoming adoption events, dates and locations")}</p></div>
<div class="btns" style="margin:0"><a class="btn btn-light" href="{L['fb']}" {EXT}>Facebook Live</a><a class="btn btn-ghost" style="border-color:#fff;color:#fff" href="{L['yt']}" {EXT}>YouTube</a></div></div></div></section>''')

# ---------------- DONATE ----------------
write("donate.html", "Donate | Great Pyrenees Rescue Society",
 "100% of donations go directly to the dogs. Donate via PayPal, our Amazon wish list, or our merch store.", f'''
<section class="page-hero"><div class="wrap"><span class="eyebrow">Donate</span><h1>Every penny goes to the dogs.</h1>
<p class="lead">Nine times out of ten, a Great Pyrenees coming into our program needs medical attention. Sometimes it's just shots or spay/neuter. Sometimes the vet bills are astronomical. We're all-volunteer, so 100% of your donation goes directly to the dogs in our care.</p>
<div class="btns"><a class="btn btn-donate" href="{L['paypal']}" {EXT}>Donate with PayPal</a></div>
<p class="muted" style="margin-top:14px">Great Pyrenees Rescue Society is a 501(c)(3) nonprofit. EIN {ph("Add EIN")}. Donations are tax-deductible to the extent allowed by law. {ph("Confirm wording with your accountant")}</p></div></section>
<section style="padding-top:10px"><div class="wrap"><div class="grid g3">
<div class="give"><div class="icon" aria-hidden="true">💳</div><h3>Give money</h3><p>A one-time gift through PayPal (card or PayPal balance) goes to vet care, food and transport.</p><a class="btn btn-donate btn-sm" href="{L['paypal']}" {EXT}>Donate via PayPal</a></div>
<div class="give"><div class="icon" aria-hidden="true">📦</div><h3>Send supplies</h3><p>Shop our Amazon wish list for the supplies our foster dogs need most.</p><a class="btn btn-primary btn-sm" href="{L['amazon']}" {EXT}>Amazon wish list</a></div>
<div class="give"><div class="icon" aria-hidden="true">👕</div><h3>Wear the mission</h3><p>Merch purchases fund supplies and medical care, and help start conversations about Pyr rescue.</p><a class="btn btn-primary btn-sm" href="{L['merch']}" {EXT}>Merch store</a></div>
</div></div></section>
<section class="alt"><div class="wrap"><div class="section-head"><h2>What your gift does</h2><p class="lead">{ph("Optional: add real examples, e.g. '$X covers a dog's vaccinations', using your actual costs")}</p></div>
<div class="stats"><div class="stat"><b>{ph("$ amount")}</b><span>{ph("what it covers")}</span></div><div class="stat"><b>{ph("$ amount")}</b><span>{ph("what it covers")}</span></div><div class="stat"><b>{ph("$ amount")}</b><span>{ph("what it covers")}</span></div><div class="stat"><b>{ph("$ amount")}</b><span>{ph("what it covers")}</span></div></div>
<p class="muted" style="margin-top:18px">Transparency: {ph("Link your annual report, Form 990, or Candid/GuideStar profile")}</p></div></section>
<section><div class="wrap"><div class="section-head"><h2>More ways to help</h2></div><div class="grid g3">
<div class="card"><h3>Spread the word</h3><p>Follow us on <a href="{L['fb']}" {EXT}>Facebook</a> and <a href="{L['ig']}" {EXT}>Instagram</a>, share our posts, and encourage others to donate. One of your friends might be looking for a Pyr.</p></div>
<div class="card"><h3>Give your time</h3><p>We rely 100% on volunteers. See our <a href="volunteer.html">volunteer opportunities</a>.</p></div>
<div class="card"><h3>Be a hero</h3><p>Feeling heroic? <a href="foster.html">Foster a dog</a> and save a life directly.</p></div>
</div><p class="lead" style="margin-top:30px">Together, we can change the future, one Great Pyrenees at a time. Thank you for being a Great Pyrenees hero.</p></div></section>''')

# ---------------- BREED ----------------
write("breed.html", "About the Great Pyrenees | Breed Facts & Training Tips | GPRS",
 "Great Pyrenees facts: shedding, barking, temperament, size, lifespan, and positive training tips from GPRS.", f'''
<section class="page-hero"><div class="wrap"><span class="eyebrow">The breed</span><h1>Is a Great Pyrenees right for you?</h1>
<p class="lead">Known as the Gentle Giant, the Great Pyrenees is a loyal, even-tempered family dog who loves attention, especially from children. They're also intelligent, independent and willful. If you want an off-leash companion who follows every command, a Pyr probably isn't for you.</p></div></section>
<section style="padding-top:10px"><div class="wrap"><div class="grid g4">
<div class="card"><h3>Size</h3><p>Males 27–32 in, 100–110 lbs. Females 25–29 in, 85–100 lbs.</p></div>
<div class="card"><h3>Lifespan</h3><p>About 10–12 years, with few major genetic problems.</p></div>
<div class="card"><h3>Shedding</h3><p>Year-round, and a lot. Regular brushing helps, but it never stops.</p></div>
<div class="card"><h3>Barking</h3><p>Yes, often. They were bred to guard livestock and react to unusual noises.</p></div>
</div></div></section>
<section class="alt"><div class="narrow prose">
<h2>Temperament</h2><p>Confident, gentle and affectionate. Territorial and protective of their flock or family when necessary, but generally calm, patient and tolerant. They're strong-willed, independent and somewhat reserved, yet attentive, fearless and loyal to their charges, human and animal.</p>
<h2>Are they aggressive guard dogs?</h2><p>No. They normally accept anyone you invite into your home, though their size can intimidate first-time visitors. Properly socialized Pyrs aren't attack dogs and are usually very responsible with their guarding instincts, though they do have guardian instincts against predators.</p>
<h2>They roam</h2><p>Pyrs have a natural tendency to roam, so when they're outside, all gates must be closed and locked. That's why we require secure fencing.</p>
<h2>Puppies need adult dogs</h2><p>Pyrs learn their role from other dogs, not from people. Even livestock guarding is taught by older dogs. They're not "people pleasers" like Retrievers or Labs. Without proper socialization as puppies, they can become very difficult teens and adults.</p>
<h2>What they look like</h2><img src="img/breed-diagram.jpg" alt="Diagram of Great Pyrenees physical features" loading="lazy" style="border-radius:16px;margin:10px 0 20px">
<p><b>Head:</b> skull width and length about equal. Rich dark brown almond-shaped eyes with black rims, and a black nose and lips. <b>Ears:</b> small to medium blunted triangles, carried low and blending into the ruff. <b>Tail:</b> carried low at rest, over the back or low in motion. A "shepherd's crook" kink is acceptable. <b>Coat:</b> double-coated, with a flat, thick, coarse outer coat and a woolly undercoat that grows in the fall and sheds in spring. <b>Color:</b> all white, or white with markings of gray, badger, reddish brown or tan.</p>
<p>Read more from the <a href="{L['akc']}" {EXT}>American Kennel Club</a>.</p>
<h2 id="training">Training tips</h2>
<ul class="checks">
<li><b>Get a professional.</b> Find a certified trainer or behaviorist familiar with livestock guardian or large breeds who uses only positive reinforcement. <a href="{L['peaceable']}" {EXT}>Peaceable Paws</a> has articles and trainer referrals.</li>
<li><b>Use a harness, not a collar.</b> A sturdy, well-fitted no-pull harness protects their strong necks. Never use prong or shock collars. They can trigger instinctive defensive behavior.</li>
<li><b>Be consistent.</b> Set clear rules and respond to unwanted behavior the same way every single time.</li>
<li><b>Meet on neutral territory.</b> Introduce new dogs on leash, in a calm, secure area where neither dog has established boundaries.</li>
<li><b>Stay calm.</b> Use a calm voice and slow movements, ignore jumping, and redirect with commands.</li></ul>
</div></section>
<section><div class="wrap"><div class="band"><div><h2>Sound like your kind of dog?</h2><p>Meet the Pyrs and Pyr mixes waiting in foster homes right now.</p></div><div class="btns" style="margin:0"><a class="btn btn-light" href="adopt.html">See available dogs</a></div></div></div></section>''')

# ---------------- ABOUT ----------------
write("about.html", "About Us | Great Pyrenees Rescue Society",
 "Founded in 2006 by Malise Saucier, GPRS is a volunteer-run, foster-based 501(c)(3) rescue for Great Pyrenees in Texas.", f'''
<section class="page-hero"><div class="wrap split"><div><span class="eyebrow">About us</span><h1>Saving Great Pyrenees whose lives are in danger</h1>
<p class="lead">Based in Texas, Great Pyrenees Rescue Society is a volunteer-run, foster-based 501(c)(3) animal rescue dedicated to the rescue, rehabilitation and adoption of Great Pyrenees dogs.</p></div>
<img src="img/dogs/22486521.jpg" alt="Angel Marie, a white Great Pyrenees, among blue hydrangeas" width="640" height="567"></div></section>
<section class="alt"><div class="narrow prose">
<h2>Our story</h2><p>GPRS was founded by <b>Malise Saucier in 2006</b> as a coalition of rescuers placing Great Pyrenees and Pyr mixes across the country, with rescues in several states where shelter kill rates are high for the breed.</p>
<p>Most of our dogs come from kill shelters in Central Texas, South Texas and the Greater Houston area. They go to foster homes in Texas and the Pacific Northwest, where they're evaluated and rehabilitated until we find them a permanent home. We have a long history of successful adoptions in Texas and the Northwest, supported by a monthly transport from Texas to the Pacific NW.</p>
<p>We adopt to families in Texas, Washington, Oregon, Idaho, California, New Mexico and Arizona.</p>
<div class="callout">There are far more wonderful, majestic, deserving Great Pyrenees in Texas than we have room for. The only way we can save them is with your help: foster homes, donations, volunteers, and families ready to adopt.</div>
<h2>How we work</h2>
<ul class="checks"><li><b>Foster-based:</b> no kennels. Every dog lives in a home, so we know them well.</li><li><b>All-volunteer:</b> 100% of donations go directly to the dogs.</li><li><b>Fully vetted:</b> vaccinations, rabies, and spay/neuter before adoption.</li><li><b>Transparent:</b> 501(c)(3) nonprofit, EIN {ph("Add EIN")}. {ph("Link Form 990 / Candid profile")}</li></ul>
<h2>Our team</h2><p>{ph("Add board members and key volunteers: names, roles, short bios and photos (with permission). Showing real people is one of the biggest trust builders for a rescue.")}</p>
<h2>Spay and neuter</h2><p>Don't be part of the problem. Be part of the solution. If you need help with spay or neuter, we have programs that can help. <a href="contact.html">Contact us</a> for more information.</p>
</div></section>
<section><div class="wrap"><div class="grid g3">
<div class="card"><h3>Adopt</h3><p>{N} dogs are waiting in foster homes right now.</p><a href="adopt.html">Meet them →</a></div>
<div class="card"><h3>Foster</h3><p>The single most valuable thing you can do in rescue.</p><a href="foster.html">Learn more →</a></div>
<div class="card"><h3>Donate</h3><p>Every dollar goes to vet care, food and transport.</p><a href="donate.html">Give today →</a></div></div></div></section>''')

# ---------------- CONTACT ----------------
write("contact.html", "Contact | Great Pyrenees Rescue Society",
 "Contact Great Pyrenees Rescue Society in Spring, TX: email, Facebook, owner surrender and shelter dog reports.", f'''
<section class="page-hero"><div class="wrap"><span class="eyebrow">Contact</span><h1>We'd love to hear from you</h1>
<p class="lead">We're all volunteers, so email or Facebook Messenger is the fastest way to reach us.</p></div></section>
<section style="padding-top:10px"><div class="wrap grid g3">
<div class="card"><div class="icon" aria-hidden="true">✉️</div><h3>Email</h3><p><a href="mailto:{L['email']}">{L['email']}</a></p><p class="muted">Typical reply time: {ph("e.g. 2–3 days")}</p></div>
<div class="card"><div class="icon" aria-hidden="true">💬</div><h3>Facebook</h3><p>Send us a message on <a href="{L['fb']}" {EXT}>Facebook</a>. Watch our dogs live every Sunday at 3pm CT.</p></div>
<div class="card"><div class="icon" aria-hidden="true">📍</div><h3>Mailing address</h3><p>Great Pyrenees Rescue Society<br>{ph("Street or PO Box")}<br>Spring, TX 77388</p><p class="muted">Phone: {ph("Add phone number, if any")}</p></div>
</div></section>
<section class="alt"><div class="narrow">
<h2 id="surrender">Need to surrender your Pyr?</h2>
<p>We have foster homes in Texas, Oregon and Washington that can take owner surrenders. Fill out the <a href="{L['surrender']}" {EXT}>owner surrender form</a> with everything about your Great Pyrenees, and a volunteer will contact you if a foster home is open. If you can keep your Pyr for a little while, that helps while we look for an open foster.</p>
<p>Outside those states? See the list of Pyr rescues at <a href="{L['natpyr']}" {EXT}>National Pyrs</a>.</p>
<div class="btns"><a class="btn btn-primary" href="{L['surrender']}" {EXT}>Owner surrender form</a></div>
<h2 id="shelter" style="margin-top:2em">Know of a Pyr in a shelter?</h2>
<p>We have limited volunteers and can't call about every shelter dog in Texas. Before sending us a dog, please:</p>
<ol><li>Call the shelter or person who posted it and ask whether the dog is already safe (adopted, reclaimed or on a rescue hold).</li>
<li>Find out if the dog is good with other dogs, cats and kids, if that's known.</li>
<li>Post the dog on your Facebook page and ask for a foster home. Often we can't pull a dog without one.</li>
<li>Ask people to fill out our <a href="{L['foster_app']}" {EXT}>foster application</a>.</li></ol>
<p>If a dog isn't in Texas, Washington, Oregon or Idaho, we can't help, but <a href="{L['natpyr']}" {EXT}>National Pyrs</a> lists rescues in other states.</p>
<p>The simple, painful truth is that we don't have enough foster homes for every dog in a shelter. Please consider <a href="foster.html">fostering</a>.</p>
<h2 style="margin-top:2em">All forms</h2>
<ul class="checks"><li><a href="{L['apply']}" {EXT}>Adoption application</a></li><li><a href="{L['contract']}" {EXT}>Adoption contract</a> (only when instructed)</li><li><a href="{L['foster_app']}" {EXT}>Foster application</a></li><li><a href="{L['foster_contract']}" {EXT}>Foster contract</a></li><li><a href="{L['volunteer']}" {EXT}>Volunteer application</a></li><li><a href="{L['surrender']}" {EXT}>Owner surrender</a></li><li><a href="{L['hw']}" {EXT}>HW+ treatment contract</a></li></ul>
</div></section>''')
print("built", N, "dogs, fees", FEE_RANGE)
