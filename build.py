#!/usr/bin/env python3
"""Builds The Brue Yard site.

Run `python3 build.py` after editing content here or in src/partials/.
It writes every page as plain HTML plus assets/data.js, so the site itself
needs no build step to run: open index.html or serve the folder.
"""
import json, re, html
from pathlib import Path

HERE = Path(__file__).parent
P = lambda name: (HERE / 'src' / 'partials' / f'{name}.html').read_text()
e = html.escape

# =====================================================================
# Data (single source for pages and for assets/data.js)
# =====================================================================
CLOSED = ["2026-12-24", "2026-12-25", "2026-12-26", "2027-01-01"]
SEASON_END = "2027-02-28"

PHOTOS = {
 'hero':     ('photo-1690798646116-fe4f5a0e2f1b', 'Kristina Kutleša', 'https://unsplash.com/photos/a-sculpture-in-a-park-surrounded-by-trees-cxPmPNHk5Ew', 'A sculpture standing in open grass, framed by trees'),
 'echoes':   ('photo-1771612559799-76daebaf37e4', 'R_ INVSCIMENTO', 'https://unsplash.com/photos/two-abstract-sculptures-in-a-grassy-park-setting-ulYHhAT0JoM', 'Two abstract sculptures in a grassy setting'),
 'preview':  ('photo-1759882607916-8119897a8262', 'Felicia Montenegro', 'https://unsplash.com/photos/modern-geometric-sculpture-on-brick-wall-background-p8ToWZwJq68', 'A geometric sculpture against an old brick wall'),
 'twilight': ('photo-1444080748397-f442aa95c3e5', 'Ryan Hutton', 'https://unsplash.com/photos/worms-eye-view-of-trees-during-night-time-Jztmx9yqjBw', 'Treetops against a night sky full of stars'),
 'matinee':  ('photo-1465847899084-d164df4dedc6', 'Larisa Birta', 'https://unsplash.com/photos/people-playing-violin-inside-dim-room-slbOcNlWNHA', 'Musicians playing violins in a dimly lit room'),
 'clay':     ('photo-1589051088132-06f36a22012a', 'Anne Nygård', 'https://unsplash.com/photos/hands-shaping-ceramic-bowl-rim-G4IB-r6nsJI', 'Hands covered in wet clay shaping the rim of a bowl'),
 'rewilding':('photo-1492789005862-689be487dff9', 'Jez Timms', 'https://unsplash.com/photos/body-of-water-surrounded-with-grass-and-trees-during-daytime-SEJO1i-YwGU', 'Still water edged with long grass and trees'),
 'folk':     ('photo-1519139270028-ab664cf42264', 'Kael Bloom', 'https://unsplash.com/photos/person-playing-stringed-instrument-0Fko0cLI2VQ', 'A musician playing a stringed instrument'),
 'barn':     ('photo-1767447612728-30dd863a8c9c', 'Julia Fiander', 'https://unsplash.com/photos/sheep-grazing-near-a-stone-barn-in-a-green-field-eaqXTZQtF7M', 'Sheep grazing beside a stone barn in a green field'),
 'meadow':   ('photo-1674991469416-16680c23e7e3', 'Ben Tovee', 'https://unsplash.com/photos/a-field-of-tall-dry-grass-with-trees-in-the-background-VQ4MF632-Hc', 'Tall autumn grass with trees beyond'),
 'stonewall':('photo-1768573490160-fa6629effe62', 'T', 'https://unsplash.com/photos/dark-wooden-planks-on-stone-wall-with-grassy-background-qgQJsKZ2Nvc', 'Dark timber boarding on a stone wall'),
 'river':    ('photo-1708624329681-f5fd84d1c58f', 'Julia Fiander', 'https://unsplash.com/photos/a-river-running-through-a-lush-green-forest-TjP6EmZQrWo', 'A shallow river running between green banks'),
 'vessels':  ('photo-1631125915902-d8abe9225ff2', 'Yana Hurska', 'https://unsplash.com/photos/3-brown-clay-vases-on-white-concrete-table-zeGT9j4ltRA', 'Three terracotta vessels on a pale table'),
 'somerset': ('photo-1601142917255-1c16c3e0ae06', 'Haydon', 'https://unsplash.com/photos/green-trees-on-hill-under-white-sky-during-daytime-9n1BygTOb4E', 'Wooded hills and fields in the Somerset countryside'),
 'fields':   ('photo-1636636875194-aa25135bf5c0', 'John-Mark Strange', 'https://unsplash.com/photos/a-view-of-a-field-with-trees-and-hills-in-the-distance-Qu8cQ1V6ZxM', 'Pasture with trees and hills in the distance'),
}

CATS = {'exhibition': ('Exhibitions', 'Exhibition'), 'performance': ('Performances', 'Performance · Music'),
        'workshop': ('Workshops', 'Workshop · Family'), 'walk': ('Outdoor Walks', 'Outdoor · Tour'), 'talk': ('Talks', 'Talk · Lecture')}
ACCESS = {'stepfree': 'Step-free', 'bsl': 'BSL interpreted', 'relaxed': 'Relaxed', 'audio': 'Audio described'}

EVENTS = [
 dict(id='echoes', slug='echoes-across-the-valley', photo='echoes', cat='exhibition', title='Echoes Across the Valley',
      desc='Bronze, stone and topography across the Threshing Barn and North Meadow, with new commissions on the River Brue.',
      when='Daily · 10:00–17:00', where='The Threshing Barn & North Meadow', price='£12.50 · Under 25s free',
      access=['stepfree', 'audio'], slots=['10:30', '12:00', '14:00', '15:30'], **{'from': '2026-10-24'}, to=SEASON_END, skipClosed=True,
      body='Timed entry keeps the Threshing Barn calm, so book a slot and stay as long as you like. The meadow is open until dusk, and the audio guide covers both the barn and the river path.'),
 dict(id='preview', slug='hard-hat-preview', photo='preview', cat='talk', title='Hard-Hat Preview: Installing the Echoes',
      desc='Walk the Threshing Barn with the install crew while the bronzes are craned into place. Short, standing tour.',
      when='Install week · 11:00 & 14:00', where='The Threshing Barn', price='£12.50 · Under 25s free',
      access=['stepfree'], slots=['11:00', '14:00'], **{'from': '2026-10-19'}, to='2026-10-23',
      body='This is the only week you can see the works before the exhibition opens. The crew stop the lift while you are in the barn, so you can ask about every strap, plinth and spirit level.'),
 dict(id='twilight', slug='twilight-meadow-walk', photo='twilight', cat='walk', title='Autumn Twilight Meadow Walk & Astronomy',
      desc='A guided dusk walk past the river commissions, ending with telescopes on the North Meadow with Bruton Astronomical Society.',
      when='Friday evenings · 17:30–19:30', where='North Meadow trail, meet at the Yard gate', price='£12.50 · Under 25s free',
      access=['relaxed', 'audio'], slots=['17:30'], **{'from': '2026-10-23'}, to='2026-12-18', dows=[5],
      body='On a clear night the meadow is one of the darkest spots near Bruton. Expect Saturn, the Andromeda galaxy and, in December, the Geminid meteor shower. Hot drinks are served at the telescopes.'),
 dict(id='matinee', slug='acoustic-matinee', photo='matinee', cat='performance', title='Acoustic Matinee: The Somerset String Ensemble',
      desc='An hour of chamber music in the Community Barn, from Purcell to new pieces written for the exhibition.',
      when='Sundays · 15:00', where='The Community Barn', price='£12.50 · Under 25s free',
      access=['stepfree'], slots=['15:00'], **{'from': '2026-10-25'}, to=SEASON_END, dows=[0], skipClosed=True,
      body='The ensemble is a string quartet of players from Bath, Frome and Wells. Each programme is different, and the running order goes up in the barn a week ahead.'),
 dict(id='clay', slug='family-clay-workshop', photo='clay', cat='workshop', title='Plein-Air Clay & Terracotta Workshop for Families',
      desc='Model river stones and small figures from local clay, then fire them in the courtyard kiln. Ages 5–12 with an adult.',
      when='Saturdays · 10:30 & 13:30', where='The Pottery Shed, South Courtyard', price='£12.50 · Under 25s free',
      access=['bsl', 'stepfree'], slots=['10:30', '13:30'], **{'from': '2026-10-24'}, to=SEASON_END, dows=[6], skipClosed=True,
      body='Under 25s go free, so most families pay for one adult ticket. Each child takes home what they make once it has been fired, usually the following Saturday.'),
 dict(id='rewilding', slug='rewilding-the-brue', photo='rewilding', cat='talk', title='Rewilding the Brue: Conservation Talk & Tea',
      desc='Ecologists from the Somerset Wildlife Trust on otters, water voles and the new wet meadow, with tea and cake from 13:30.',
      when='Wednesdays · 14:00', where='The Granary Room', price='£12.50 · Under 25s free',
      access=['relaxed', 'stepfree'], slots=['14:00'], **{'from': '2026-10-21'}, to=SEASON_END, dows=[3], skipClosed=True,
      body='The wet meadow was dug in 2024 to slow floodwater above the town. The talks follow what has moved in since, with a different speaker each month.'),
 dict(id='folk', slug='winter-folk-night', photo='folk', cat='performance', title='Barn Sessions: Winter Folk Night',
      desc='Monthly evening of Somerset songs and tunes by lamplight, with a BSL interpreter on stage for every set.',
      when='Monthly Thursdays · 19:30', where='The Community Barn', price='£12.50 · Under 25s free',
      access=['bsl', 'stepfree'], slots=['19:30'], dates=['2026-11-12', '2026-12-10', '2027-01-14', '2027-02-11'],
      body='Guests this season include singers from the Somerset Levels and a fiddle trio from Frome. Seating is unreserved, so arrive early for the front benches.'),
]
EXTRA = {
 'echoes': dict(more="The exhibition fills the Threshing Barn and carries on outside along the North Meadow. Allow time for both: the meadow route is 1.2 km on mown paths and takes about 40 minutes at a gentle pace.", duration="Allow 1½–2 hours", suitable="All ages", bring="Boots for the meadow after rain", accessnote="Step-free barn. Audio-described tour on the first Sunday of each month."),
 'preview': dict(more="The technicians and curators show how a two-tonne bronze is lifted into a Grade II barn without touching the oak roof. Hard hats and hi-vis are provided. Groups of twelve.", duration="45 minutes", suitable="Ages 12+", bring="Closed-toe shoes", accessnote="Step-free route. Standing tour, with stools on request."),
 'twilight': dict(more="Walk the river path at dusk with a guide, past all four commissions, then settle on the North Meadow for telescopes with Bruton Astronomical Society. If heavy rain cancels the walk, we email you by 15:00.", duration="2 hours", suitable="Ages 8+", bring="Warm layers. We lend red-filter torches.", accessnote="Relaxed pace with audio description throughout. Uneven ground."),
 'matinee': dict(more="The Somerset String Ensemble play an hour of chamber music, from Purcell to two new pieces written in response to the exhibition. Tea and cake in the Granary afterwards.", duration="60 minutes, no interval", suitable="All ages. Babes in arms welcome.", bring="Nothing. Cushions provided.", accessnote="Step-free, hearing loop, wheelchair spaces on the front row."),
 'clay': dict(more="Families work with clay dug from the Brue banks. Children model river stones, small figures or a pot, and we fire them in the courtyard kiln for collection the following weekend.", duration="90 minutes", suitable="Ages 5–12 with an adult", bring="Clothes that can get muddy. Aprons provided.", accessnote="BSL interpreter at every session. Step-free courtyard."),
 'rewilding': dict(more="Ecologists from the Somerset Wildlife Trust report on the otters, water voles and kingfishers returning to the new wet meadow, then take questions over tea. An optional short walk to the scrape follows.", duration="75 minutes with tea", suitable="Adults and older children", bring="Binoculars, if you have them", accessnote="Relaxed session in a step-free room with seating throughout."),
 'folk': dict(more="A monthly evening of Somerset songs and tunes by lamplight in the Community Barn, with a different guest each month and a short floor-singers’ spot. The bar opens at 19:00.", duration="2 hours with interval", suitable="All ages. Under 14s with an adult.", bring="A song, if you’d like a floor spot", accessnote="BSL interpreter on stage. Step-free, with a hearing loop."),
}

# =====================================================================
# Helpers
# =====================================================================
def src(pid, w, ratio):
    return f'https://images.unsplash.com/{pid}?auto=format&amp;fit=crop&amp;w={w}&amp;h={round(w * ratio)}&amp;q=72'

def img(key, ratio, sizes, widths=(480, 800, 1200, 1600), eager=False):
    pid, who, href, alt = PHOTOS[key]
    srcset = ', '.join(f'{src(pid, w, ratio)} {w}w' for w in widths)
    w0 = widths[2] if len(widths) > 2 else widths[-1]
    load = 'fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="{src(pid, w0, ratio)}" srcset="{srcset}" sizes="{sizes}" width="{w0}" '
            f'height="{round(w0 * ratio)}" alt="{e(alt)}" {load} decoding="async">')

def credit(key):
    pid, who, href, alt = PHOTOS[key]
    return f'Photo: <a href="{href}" target="_blank" rel="noopener">{e(who)}</a> / Unsplash'

def frame(key, ratio_cls, ratio, sizes, label, eager=False, tag='figure'):
    return f'<{tag} class="ph {ratio_cls}" data-alt="{e(label)}">{img(key, ratio, sizes, eager=eager)}</{tag}>'

NAV = [('whats-on.html', 'What’s On', 'whats-on'), ('exhibitions.html', 'Exhibitions &amp; Grounds', 'exhibitions'),
       ('visit.html', 'Plan Your Visit', 'visit'), ('learning.html', 'Learning &amp; Community', 'learning'),
       ('support.html', 'Support Us', 'support')]
FOOT = [('accessibility.html', 'Accessibility Statement'), ('governance.html', 'Code of Governance'), ('venue-hire.html', 'Venue Hire'),
        ('environment.html', 'Environmental Policy'), ('privacy.html', 'Privacy Policy')]

def header(root, current):
    items = ''.join(f'<li><a href="{root}{h}"{" aria-current=\"page\"" if k == current else ""}>{t}</a></li>' for h, t, k in NAV)
    return f'''  <div class="utility">
    <div class="wrap">
      <p class="status"><span class="pulse" aria-hidden="true"></span><span><b>Open today:</b> 10:00 – 17:00 <span style="opacity:.75">(Meadow trail closes at dusk)</span></span></p>
      <nav aria-label="Quick links">
        <ul>
          <li><a href="{root}visit.html#getting-here">Getting to Bruton</a></li>
          <li class="sep" aria-hidden="true">|</li>
          <li><a href="{root}accessibility.html">Access Information</a></li>
        </ul>
      </nav>
    </div>
  </div>

  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="{root}index.html" aria-label="The Brue Yard, Bruton, Somerset: home">
        <b>THE BRUE YARD</b>
        <span>· BRUTON, SOMERSET</span>
      </a>
      <nav class="primary-nav" aria-label="Primary">
        <ul>{items}</ul>
      </nav>
      <button class="btn" type="button" data-book="echoes"><span class="book-long">Book Tickets / Timed Entry</span><span class="book-short">Book</span></button>
      <button class="burger" type="button" id="menu-trigger" aria-expanded="false" aria-controls="mobile-menu"><span aria-hidden="true"></span><span class="sr-only">Open menu</span></button>
    </div>
  </header>
'''

def menu(root, current):
    items = '\n'.join(f'      <li><a href="{root}{h}"{" aria-current=\"page\"" if k == current else ""}>{t}</a></li>' for h, t, k in NAV)
    return f'''<div class="menu" id="mobile-menu" role="dialog" aria-modal="true" aria-label="Site menu" hidden>
  <div class="wrap menu__top">
    <span class="brand"><b>THE BRUE YARD</b><span>· BRUTON, SOMERSET</span></span>
    <button class="icon-btn" type="button" id="menu-close" aria-label="Close menu">×</button>
  </div>
  <nav class="wrap" aria-label="Primary (mobile)">
    <ul class="menu__list">
      <li><a href="{root}index.html"{" aria-current=\"page\"" if current == 'home' else ""}>Home</a></li>
{items}
    </ul>
    <button class="btn" type="button" data-book="echoes" style="width:100%">Book Tickets / Timed Entry</button>
  </nav>
</div>
'''

def footer(root):
    f = P('footer')
    legal = ''.join(f'\n            <li><a href="{root}{h}">{t}</a></li>' for h, t in FOOT)
    f = re.sub(r'<nav aria-label="Footer">\s*<ul>.*?</ul>', f'<nav aria-label="Footer">\n          <ul>{legal}\n          </ul>', f, flags=re.S)
    f = f.replace('<p class="brand"><b>THE BRUE YARD</b>', f'<p class="brand"><b>THE BRUE YARD</b>')
    sitemap = ''.join(f'<li><a href="{root}{h}">{t}</a></li>' for h, t, k in NAV)
    f = f.replace('<p class="note">Registered charity no. 1189034</p>',
                  f'<p class="note">Registered charity no. 1189034</p>\n          <ul class="foot-nav" aria-label="Site">{sitemap}</ul>')
    return f

def crumbs(root, trail):
    items = ''.join(f'<li><a href="{root}{h}">{t}</a></li>' for h, t in trail[:-1])
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol><li><a href="{root}index.html">Home</a></li>{items}<li aria-current="page">{trail[-1][1]}</li></ol></nav>'

def page_head(root, trail, eyebrow, title, standfirst, extra=''):
    return f'''    <section class="page-head" aria-labelledby="page-title">
      <div class="wrap">
        {crumbs(root, trail)}
        <div class="page-head__grid">
          <div>
            <p class="eyebrow eyebrow--accent">{eyebrow}</p>
            <h1 class="page-title" id="page-title">{title}</h1>
          </div>
          <p class="standfirst">{standfirst}</p>
        </div>{extra}
      </div>
    </section>
'''

FAV = P('favicon').strip()

def layout(path, *, title, desc, body, current=None):
    depth = path.count('/')
    root = '../' * depth
    full_title = 'The Brue Yard' if current == 'home' else f'{title} · The Brue Yard'
    doc = f'''<!doctype html>
<html lang="en-GB" data-root="{root}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{full_title}</title>
<meta name="description" content="{e(desc)}">
{FAV}
<meta name="theme-color" content="#18191A">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&amp;family=IBM+Plex+Mono:wght@400;500&amp;family=Newsreader:ital,opsz,wght@0,6..72,400..600;1,6..72,400..500&amp;display=swap">
<link rel="stylesheet" href="{root}assets/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>

<div id="page">
{header(root, current)}
  <main id="main" tabindex="-1">
{body}
  </main>

{footer(root)}
</div>

{menu(root, current)}
{P('drawer')}
<script src="{root}assets/data.js"></script>
<script src="{root}assets/site.js"></script>
</body>
</html>
'''
    out = HERE / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    return out

def section_head(eyebrow, title, standfirst='', h='h2', id_=''):
    sf = f'<p>{standfirst}</p>' if standfirst else ''
    return f'''        <div class="section-head">
          <div>
            <p class="eyebrow eyebrow--accent">{eyebrow}</p>
            <{h} class="section-title"{f' id="{id_}"' if id_ else ''}>{title}</{h}>
          </div>
          {sf}
        </div>'''

def link_fix(s, root):
    """Point in-page anchors from the old one-page site at the real pages."""
    for a, b in [('href="#whats-on"', f'href="{root}whats-on.html"'), ('href="#grounds"', f'href="{root}exhibitions.html#grounds"'),
                 ('href="#visit"', f'href="{root}visit.html"'), ('href="#learning"', f'href="{root}learning.html"'),
                 ('href="#support"', f'href="{root}support.html"'), ('href="#access"', f'href="{root}visit.html#access"'),
                 ('href="#essay"', f'href="{root}exhibitions/echoes-across-the-valley.html#essay"')]:
        s = s.replace(a, b)
    return s

# =====================================================================
# Pieces cut from the original one-page design
# =====================================================================
G = P('grounds')
SITES = G[G.index('<ul class="sites">'):G.index('</ul>', G.index('<ul class="sites">')) + 5]
RIVER = G[G.index('<figure class="plate-wide">'):G.index('</figure>', G.index('<figure class="plate-wide">')) + 9]
ESSAY = G[G.index('<article class="essay"'):G.index('</article>') + 10]
VISIT = P('visit')
VISIT_INNER = VISIT[VISIT.index('<div class="visit">'):VISIT.rindex('</div>\n    </section>')]
WHATSON = P('whatson')
WHATSON_INNER = WHATSON[WHATSON.index('<div class="filters"'):WHATSON.rindex('</div>\n    </section>')]

def static_cards(ids, root):
    """Plain links shown until the script draws the full cards (and to search engines)."""
    return ''.join(f'<li class="event-static"><a href="{root}events/{ev["slug"]}.html">{e(ev["title"])}</a></li>'
                   for ev in EVENTS if ev['id'] in ids)

# =====================================================================
# Pages
# =====================================================================
def home():
    root = ''
    body = f'''    {link_fix(P('hero'), root)}

    {P('ticker')}

    <section class="section" id="whats-on" aria-labelledby="hl-title">
      <div class="wrap">
{section_head('Autumn / Winter 2026–27', 'What’s On', 'Exhibitions in the barns, evening walks on the meadow, Sunday music and Saturday clay. Turn any card over for times, what to bring and access details.', id_='hl-title')}
        <ul class="events" data-cards="echoes,twilight,clay">{static_cards(['echoes', 'twilight', 'clay'], root)}</ul>
        <div class="more-row">
          <p><b>{len(EVENTS)} events</b> this season, with filters for dates, type and access needs.</p>
          <a class="btn btn--ghost" href="whats-on.html">See the full programme</a>
        </div>
      </div>
    </section>

    <section class="section" id="grounds" aria-labelledby="grounds-title">
      <div class="wrap">
{section_head('Twelve acres on the River Brue', 'Exhibitions &amp; Grounds', 'A working farmyard turned gallery: two stone barns, a granary and a meadow trail that follows the river east of the town.', id_='grounds-title')}
        {SITES}
        {RIVER}
        <div class="more-row">
          <p>Read the exhibition essay and find the four riverside commissions on the map.</p>
          <a class="btn btn--ghost" href="exhibitions/echoes-across-the-valley.html">About the exhibition</a>
        </div>
      </div>
    </section>

    <section class="section" aria-labelledby="visit-band-title">
      <div class="wrap">
{section_head('Getting to Bruton', 'Plan Your Visit', 'Bruton has its own railway station, eight minutes’ walk from our gate.', id_='visit-band-title')}
        <ul class="band">
          <li><p class="eyebrow">Open</p><h3>Tuesday – Sunday</h3><p class="mono">10:00 – 17:00</p><p>Meadow trail until dusk. Quiet sensory hour Thursdays 10:00–11:30.</p></li>
          <li><p class="eyebrow">By train</p><h3>8 minutes on foot</h3><p class="mono">Bruton station</p><p>Direct GWR trains from Bath, Westbury and Weymouth. Change at Castle Cary for London.</p></li>
          <li><p class="eyebrow">Access</p><h3>Step-free barns</h3><p class="mono">All-terrain chairs</p><p>Free to borrow for the meadow. Visual stories and tactile maps at the desk.</p></li>
        </ul>
        <div class="more-row">
          <p>Dropping Lane, Bruton, Somerset BA10 0NL</p>
          <a class="btn btn--ghost" href="visit.html">Opening times, travel and access</a>
        </div>
      </div>
    </section>

    {link_fix(P('panels'), root).replace('href="whats-on.html" data-cat-link="workshop"', 'href="whats-on.html?cat=workshop"').replace('See family workshops', 'See family workshops').replace('<a class="btn" href="support.html">Become a Friend</a>', '<a class="btn" href="support.html">Become a Friend</a>')}'''
    body = body.replace('<a class="btn btn--ghost" href="learning.html"', '<a class="btn btn--ghost" href="learning.html"')
    layout('index.html', title='Home', desc='The Brue Yard Contemporary & Sculpture Meadows in Bruton, Somerset: exhibitions, events, visiting information and timed-entry tickets.', body=body, current='home')

def whats_on():
    root = ''
    body = page_head(root, [('whats-on.html', 'What’s On')], 'Autumn / Winter 2026–27', 'What’s On',
                     'Every event this season. Filter by date, type or access provision, turn a card over for the detail, or pick a day from the calendar.')
    body += f'''
    {P('ticker')}

    <section class="section section--tight" id="whats-on" aria-labelledby="page-title">
      <div class="wrap">
        {WHATSON_INNER}
      </div>
    </section>
'''
    body = body.replace('<ul class="events" id="events" role="tabpanel" aria-labelledby="whatson-title"></ul>',
                        f'<ul class="events" id="events" role="tabpanel" aria-labelledby="page-title">{static_cards([x["id"] for x in EVENTS], root)}</ul>')
    layout('whats-on.html', title='What’s On', desc='Exhibitions, performances, workshops, walks and talks at The Brue Yard, Bruton, this autumn and winter.', body=body, current='whats-on')

ICON = {'stepfree': '<svg viewBox="0 0 12 12" aria-hidden="true"><circle cx="6" cy="2" r="1.5"/><path d="M4 4h3v3h2.5L11 10.5 10 11 8.8 8.5H5.5a1.5 1.5 0 0 1-1.5-1.5z"/></svg>',
        'bsl': '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M3 11V5l1-3 1 3V1.5l1 .2V5l1-3.5 1 .3L7.5 6 10 4.5l.7.7L7 9.5V11z"/></svg>',
        'relaxed': '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M6 1a5 5 0 1 0 0 10A5 5 0 0 0 6 1zm-2 3.5a.8.8 0 1 1 0 1.6.8.8 0 0 1 0-1.6zm4 0a.8.8 0 1 1 0 1.6.8.8 0 0 1 0-1.6zM3.6 7.4h4.8A2.6 2.6 0 0 1 6 9a2.6 2.6 0 0 1-2.4-1.6z"/></svg>',
        'audio': '<svg viewBox="0 0 12 12" aria-hidden="true"><path d="M1 4.5h2L6 2v8L3 7.5H1zM8 3.5a3.5 3.5 0 0 1 0 5l-.7-.7a2.5 2.5 0 0 0 0-3.6zm1.5-1.5a5.6 5.6 0 0 1 0 8l-.7-.7a4.6 4.6 0 0 0 0-6.6z"/></svg>'}

def event_page(ev):
    root = '../'
    x = EXTRA[ev['id']]
    label, eyebrow = CATS[ev['cat']]
    p1, p2 = ev['price'].split(' · ')
    chips = ''.join(f'<li class="chip">{ICON[a]}{ACCESS[a]}</li>' for a in ev['access'])
    exhibition_link = ('<p><a class="link-arrow" href="../exhibitions/echoes-across-the-valley.html">Read about the exhibition →</a></p>'
                       if ev['id'] in ('echoes', 'preview', 'twilight') else '')
    body = f'''    <section class="ev-hero" aria-labelledby="page-title">
      <div class="wrap">
        {crumbs(root, [('whats-on.html', 'What’s On'), (f'whats-on.html?cat={ev["cat"]}', label), ('', e(ev['title']))])}
        <div class="ev-hero__grid">
          <div class="ev-hero__text">
            <p class="badge">{eyebrow}</p>
            <h1 class="page-title" id="page-title">{e(ev['title'])}</h1>
            <p class="standfirst">{e(ev['desc'])}</p>
            <dl class="meta">
              <div><dt>When</dt><dd>{e(ev['when'])}</dd></div>
              <div><dt>Where</dt><dd>{e(ev['where'])}</dd></div>
              <div><dt>Tickets</dt><dd>{p1} · {p2}</dd></div>
            </dl>
            <ul class="chips" aria-label="Access">{chips}</ul>
            <div class="hero__actions">
              <button class="btn" type="button" data-book="{ev['id']}">Book tickets</button>
              <a class="link-arrow" href="#dates">See all dates →</a>
            </div>
          </div>
          <figure class="ev-hero__photo">
            {frame(ev['photo'], 'ph--3x2', 2/3, '(max-width: 960px) 100vw, 50vw', ev['title'], eager=True, tag='div')}
            <figcaption class="credit">{credit(ev['photo'])}</figcaption>
          </figure>
        </div>
      </div>
    </section>

    <section class="section section--tight">
      <div class="wrap ev-body">
        <div class="ev-main prose">
          <h2>About this event</h2>
          <p class="lead">{e(x['more'])}</p>
          <p>{e(ev['body'])}</p>
          {exhibition_link}
          <h2>What to expect</h2>
          <dl class="ev-facts">
            <div><dt>Length</dt><dd>{e(x['duration'])}</dd></div>
            <div><dt>Suits</dt><dd>{e(x['suitable'])}</dd></div>
            <div><dt>Bring</dt><dd>{e(x['bring'])}</dd></div>
            <div><dt>Where</dt><dd>{e(ev['where'])}</dd></div>
          </dl>
          <h2 id="access">Access</h2>
          <p>{e(x['accessnote'])}</p>
          <p>Carers and personal assistants come free. Tell us what you need when you book, or call the box office on <span class="mono">01749 555 018</span>. Read the full <a href="../accessibility.html">access information</a>.</p>
          <h2>Getting here</h2>
          <p>The Yard is on Dropping Lane, an 8-minute signposted walk from Bruton station. There are four accessible EV bays on site and overflow parking on Station Road. <a href="../visit.html#getting-here">Travel and parking →</a></p>
        </div>
        <aside class="ev-aside" id="dates" aria-labelledby="dates-title">
          <h2 id="dates-title">Upcoming dates</h2>
          <p class="note">Choose a date to book. Times: {', '.join(ev['slots'])}.</p>
          <ol class="date-list" data-event-dates="{ev['id']}" data-limit="6"><li class="none">{e(ev['when'])}</li></ol>
          <p class="note" data-more-dates></p>
          <dl class="prices">
            <div><dt>Adult</dt><dd>£12.50</dd></div>
            <div><dt>Concession (65+, students)</dt><dd>£9.00</dd></div>
            <div><dt>Under 25 / Somerset resident</dt><dd>Free</dd></div>
          </dl>
          <button class="btn btn--block" type="button" data-book="{ev['id']}">Book tickets</button>
        </aside>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="related-title">
      <div class="wrap">
{section_head('More at the Yard', 'You might also like', id_='related-title')}
        <ul class="events" data-cards="related:{ev['id']}">{static_cards([o['id'] for o in EVENTS if o['id'] != ev['id']][:3], root)}</ul>
      </div>
    </section>
'''
    layout(f'events/{ev["slug"]}.html', title=ev['title'], desc=ev['desc'], body=body, current='whats-on')

def exhibition():
    root = '../'
    hero = link_fix(P('hero'), root).replace(f'href="{root}exhibitions/echoes-across-the-valley.html#essay"', 'href="#essay"').replace('Read Exhibition Essay &amp; Audio Guide →', 'Read the essay and find the commissions →')
    hero = hero.replace('<div class="wrap hero__grid">', f'<div class="wrap">{crumbs(root, [("exhibitions.html", "Exhibitions &amp; Grounds"), ("", "Echoes Across the Valley")])}</div>\n      <div class="wrap hero__grid">', 1)
    stops = [('1', 'Welcome: reading the valley', '3:10'), ('2', 'The threshing floor', '4:05'), ('3', 'Casting a room', '5:20'),
             ('4', 'A line made by walking', '4:40'), ('5', 'The 1917 flood', '3:55'), ('6', 'N1 · Weir Line', '2:50')]
    stops_html = ''.join(f'<li><span class="k">{n}</span><span class="t">{t}</span><span class="mono">{d}</span></li>' for n, t, d in stops)
    body = f'''    {hero}

    <section class="section section--tight" aria-label="Exhibition essay">
      <div class="wrap">
        {RIVER}

        {ESSAY}
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="artists-title">
      <div class="wrap">
{section_head('In the exhibition', 'Artists', 'Two artists who have spent careers measuring land with their hands, and four new works made for this river.', id_='artists-title')}
        <ul class="artists">
          <li><p class="eyebrow">The Threshing Barn</p><h3>Rachel Whiteread</h3><p>Casts the spaces inside and beneath things: rooms, stairs, the gap under a chair. Works in plaster, resin and bronze stand on the barn’s original threshing floor.</p></li>
          <li><p class="eyebrow">The North Meadow</p><h3>Richard Long</h3><p>Makes work by walking, from lines worn into grass to stones gathered and set out in lines and circles. His work here runs from the barn door down to the water.</p></li>
          <li><p class="eyebrow">The river banks</p><h3>Four new commissions</h3><p>Chosen through an open call to artists in the South West, and placed along the river path where the 1917 flood line reached.</p></li>
        </ul>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="audio-title">
      <div class="wrap split-2">
        <div>
{section_head('Audio guide', 'Listen as you walk', '', id_='audio-title')}
          <p class="lead">Fourteen stops, 52 minutes, narrated by the curators and the artists. Use your own phone and headphones on the Yard’s free wifi, or borrow a player from the Welcome Desk.</p>
          <p>Every stop has a transcript and a BSL video. Large-print and Easy Read guides are free at the desk.</p>
        </div>
        <ol class="stops" aria-label="First six stops">{stops_html}<li class="more">+ 8 more stops along the river</li></ol>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="exh-events-title">
      <div class="wrap">
{section_head('Around the exhibition', 'Events', 'Walks, previews and talks that take you further into the work.', id_='exh-events-title')}
        <ul class="events" data-cards="echoes,preview,twilight">{static_cards(['echoes', 'preview', 'twilight'], root)}</ul>
      </div>
    </section>
'''
    layout('exhibitions/echoes-across-the-valley.html', title='Echoes Across the Valley', desc='Echoes Across the Valley: Bronze, Stone, and Topography. Rachel Whiteread, Richard Long and new commissions on the River Brue. 24 October 2026 – 28 February 2027.', body=body, current='exhibitions')

def exhibitions():
    root = ''
    past = [('Spring 2026', 'Common Ground', 'Furniture and tools from farms on the Somerset Levels'),
            ('Autumn 2025', 'Weather Station', 'Instruments, diaries and paintings of West Country weather'),
            ('Spring 2025', 'Lime &amp; Lias', 'The stone, mortar and makers who built Bruton'),
            ('Autumn 2024', 'Open Barn', 'The Yard’s first exhibition, after the restoration of the Threshing Barn')]
    past_html = ''.join(f'<li><span class="mono">{d}</span><b>{t}</b><span>{s}</span></li>' for d, t, s in past)
    body = page_head(root, [('exhibitions.html', 'Exhibitions &amp; Grounds')], 'Twelve acres on the River Brue', 'Exhibitions &amp; Grounds',
                     'Two stone barns, a granary and a meadow trail along the river. One major exhibition each season, with the meadow open every day until dusk.')
    body += f'''
    <section class="section section--tight" aria-labelledby="now-title">
      <div class="wrap">
        <article class="feature">
          <a class="feature__media" href="exhibitions/echoes-across-the-valley.html" tabindex="-1" aria-hidden="true">{frame('hero', 'ph--4x5', 1.25, '(max-width: 860px) 100vw, 45vw', 'Echoes Across the Valley', tag='div')}</a>
          <div class="feature__text">
            <p class="badge">Now showing · from 24 October</p>
            <h2 id="now-title" class="feature__title"><a href="exhibitions/echoes-across-the-valley.html">Echoes Across the Valley</a></h2>
            <p class="feature__sub">Bronze, Stone, and Topography</p>
            <p>Rachel Whiteread, Richard Long and four new commissions on the River Brue, across the Threshing Barn and the North Meadow.</p>
            <dl class="meta">
              <div><dt>Dates</dt><dd class="mono">24 Oct 2026 – 28 Feb 2027</dd></div>
              <div><dt>Admission</dt><dd>£12.50 · Under 25s free</dd></div>
            </dl>
            <div class="hero__actions">
              <button class="btn" type="button" data-book="echoes">Book Timed Entry</button>
              <a class="link-arrow" href="exhibitions/echoes-across-the-valley.html">About the exhibition →</a>
            </div>
            <p class="credit">{credit('hero')}</p>
          </div>
        </article>
      </div>
    </section>

    <section class="section section--rule" id="grounds" aria-labelledby="grounds-title">
      <div class="wrap">
{section_head('The site', 'The grounds', 'Everything is within a few minutes’ walk of the Welcome Desk, and all three buildings are step-free.', id_='grounds-title')}
        {SITES}
        {RIVER}
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="next-title">
      <div class="wrap split-2">
        <div>
{section_head('Coming next', 'Spring 2027', '', id_='next-title')}
          <p class="lead">Our spring exhibition will be announced in January. Journal subscribers hear first, a week before tickets go on sale.</p>
          <p><a class="link-arrow" href="#journal-title">Sign up to the Journal →</a></p>
        </div>
        <div>
          <h3 class="list-title">Past exhibitions</h3>
          <ol class="past">{past_html}</ol>
        </div>
      </div>
    </section>
'''
    layout('exhibitions.html', title='Exhibitions & Grounds', desc='Current and past exhibitions at The Brue Yard, and a guide to the barns, granary and North Meadow trail in Bruton.', body=body, current='exhibitions')

def visit():
    root = ''
    faqs = [('Do I need to book?', 'Booking a timed entry slot is the best way to be sure of getting in, especially at weekends. Walk-up tickets are sold at the Welcome Desk when there is space.'),
            ('Are under 25s really free?', 'Yes. Under 25s and Somerset residents go free, but please reserve a ticket so we can manage numbers in the barns. Bring proof of age or a Somerset postcode.'),
            ('Can I bring my dog?', 'Dogs on leads are welcome on the meadow trail and in the courtyard. Only assistance dogs can come into the barns.'),
            ('Is there somewhere to eat?', 'The Granary Café serves breakfast, lunch and cake from 10:00 to 16:30, using produce from farms around Bruton. Picnics are welcome on the meadow.'),
            ('What if it rains?', 'The barns are fully covered. The meadow paths are mown grass and can get muddy, so we lend wellies in most sizes at the desk.'),
            ('Can I take photographs?', 'Yes, for personal use and without flash. A few loaned works are marked with a no-photography symbol.')]
    faq_html = ''.join(f'<details class="faq"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    facilities = [('The Granary Café', 'Breakfast, lunch and cake, 10:00–16:30.'), ('Shop', 'Books, prints and ceramics made in Somerset.'),
                  ('Toilets', 'Accessible toilet and Changing Places room by the Welcome Desk.'), ('Baby change', 'In the accessible toilet and the café.'),
                  ('Cloakroom', 'Free lockers for bags and coats.'), ('Wifi', 'Free across the courtyard and barns.')]
    fac_html = ''.join(f'<li><b>{t}</b><span>{d}</span></li>' for t, d in facilities)
    inner = VISIT_INNER.replace('<div class="transit" aria-label="How to get here">', '<div class="transit" id="getting-here" aria-label="How to get here">')
    body = page_head(root, [('visit.html', 'Plan Your Visit')], 'Getting to Bruton', 'Plan Your Visit',
                     'Bruton has its own railway station, eight minutes’ walk from our gate. Most visitors arrive by train or on foot from the High Street.')
    body += f'''
    <section class="section section--tight" id="visit" aria-label="Opening hours and travel">
      <div class="wrap">
        {inner}
        </div>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="fac-title">
      <div class="wrap">
{section_head('On site', 'Facilities', '', id_='fac-title')}
        <ul class="facilities">{fac_html}</ul>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="faq-title">
      <div class="wrap split-2">
        <div>
{section_head('Before you come', 'Questions', '', id_='faq-title')}
          <p class="lead">Can’t find what you need? Call the box office on <span class="mono">01749 555 018</span>, Tuesday to Sunday, 10:00–17:00.</p>
        </div>
        <div class="faqs">{faq_html}</div>
      </div>
    </section>
'''
    layout('visit.html', title='Plan Your Visit', desc='Opening hours, directions from Bruton station, parking, access and facilities at The Brue Yard.', body=body, current='visit')

def learning():
    root = ''
    stages = [('EYFS &amp; KS1', 'Mud, Stone and Me', 'Sorting, stacking and printing with river stones.'),
              ('KS2', 'Mapping the Valley', 'Contour drawing on the meadow and a clay relief of the river.'),
              ('KS3', 'Casting Space', 'Plaster casting inspired by the Threshing Barn sculptures.'),
              ('KS4–5', 'Land and Making', 'Portfolio day for art and geography students, with a curator.')]
    stage_html = ''.join(f'<tr><th scope="row">{a}</th><td><b>{b}</b><br>{c}</td></tr>' for a, b, c in stages)
    body = page_head(root, [('learning.html', 'Learning &amp; Community')], 'For schools, families and the town', 'Learning &amp; Community',
                     'Free visits for every Somerset state school, Saturday clay for families, and a monthly town forum in the Granary.')
    body += f'''
    <section class="section section--tight" aria-labelledby="schools-title">
      <div class="wrap split-2 split-2--media">
        <figure class="split-media">{frame('vessels', 'ph--4x5', 1.25, '(max-width: 860px) 100vw, 45vw', 'Clay vessels from a school workshop', tag='div')}<figcaption class="credit">{credit('vessels')}</figcaption></figure>
        <div>
{section_head('Schools', 'Free school visits', '', id_='schools-title')}
          <p class="lead">Every state school in Somerset can bring a class for free, including a two-hour workshop with an artist educator.</p>
          <p>Our rural school bus fund pays for the coach from schools more than five miles away. Last year it brought 1,140 pupils from Wincanton, Castle Cary and Frome.</p>
          <div class="table-wrap">
            <table class="stages"><caption>Workshops by key stage</caption><tbody>{stage_html}</tbody></table>
          </div>
          <p>To book, email <span class="mono">schools@brueyard.org.uk</span> with your school, year group and preferred dates.</p>
        </div>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="families-title">
      <div class="wrap">
{section_head('Families', 'Saturday clay and more', 'Drop-in trails every day, and a hands-on workshop every Saturday with a BSL interpreter.', id_='families-title')}
        <ul class="events" data-cards="clay,twilight,matinee">{static_cards(['clay', 'twilight', 'matinee'], root)}</ul>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="community-title">
      <div class="wrap">
{section_head('Community', 'For Bruton', '', id_='community-title')}
        <ul class="band">
          <li><p class="eyebrow">First Tuesday, 18:30</p><h3>Town forum</h3><p>An open meeting in the Granary on what the Yard should do next. Tea provided, everyone welcome.</p></li>
          <li><p class="eyebrow">At cost</p><h3>Community Barn</h3><p>Bruton groups can hire the Community Barn for rehearsals, meetings and celebrations at cost. <a href="venue-hire.html">Venue hire</a></p></li>
          <li><p class="eyebrow">Thursdays</p><h3>Quiet sensory hour</h3><p>10:00–11:30, with lower light, no audio and a quiet room in the Granary.</p></li>
        </ul>
      </div>
    </section>
'''
    layout('learning.html', title='Learning & Community', desc='Free school visits, family workshops and community programmes at The Brue Yard, Bruton.', body=body, current='learning')

def support():
    root = ''
    tiers = [('Friend', '£45', 'a year', ['Free entry for you, all season', 'Book events a week early', 'The Journal in print', '10% off in the café and shop']),
             ('Joint Friends', '£70', 'a year', ['Everything in Friend, for two adults at one address', 'Bring two under-25s to any event free', 'Invitation to exhibition previews']),
             ('Patron', '£300', 'a year', ['Everything in Joint Friends', 'Private curator tour each season', 'Your name on the supporters’ wall', 'Pays for a school class’s coach'])]
    tier_html = ''
    for i, (n, p, per, ben) in enumerate(tiers):
        lis = ''.join(f'<li>{b}</li>' for b in ben)
        tier_html += f'<li class="tier-card{" tier-card--accent" if i == 1 else ""}"><p class="eyebrow">{n}</p><p class="tier-card__price"><b>{p}</b> {per}</p><ul>{lis}</ul><a class="btn{" " if i == 1 else " btn--ghost"}" href="#join" data-join="{n}">Join as {n}</a></li>'
    body = page_head(root, [('support.html', 'Support Us')], 'A charity in Bruton', 'Support Us',
                     'Tickets cover less than half of what it costs to run the Yard. Friends, donors and funders pay for the rest, including free entry for everyone under 25.')
    body += f'''
    <section class="section section--tight" id="join" aria-labelledby="friends-title">
      <div class="wrap">
{section_head('Membership', 'Become a Friend', 'Free entry all season, early booking, and the knowledge that you are keeping the barns open.', id_='friends-title')}
        <ul class="tiers">{tier_html}</ul>
        <p class="note" id="join-note" role="status"></p>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="bus-title">
      <div class="wrap split-2 split-2--media">
        <figure class="split-media">{frame('somerset', 'ph--4x5', 1.25, '(max-width: 860px) 100vw, 45vw', 'Somerset countryside on the school bus route', tag='div')}<figcaption class="credit">{credit('somerset')}</figcaption></figure>
        <div>
{section_head('Donate', 'Keep the rural school bus running', '', id_='bus-title')}
          <p class="lead">The nearest bus to the Yard from many villages runs twice a week. Our coach fund brings whole classes to Bruton for free.</p>
          <form class="donate-form" data-donate novalidate aria-labelledby="bus-title">
            <fieldset>
              <legend>Choose an amount</legend>
              <div class="amounts">
                <label class="amount"><input type="radio" name="amount" value="10"><span>£10</span></label>
                <label class="amount"><input type="radio" name="amount" value="25" checked><span>£25</span></label>
                <label class="amount"><input type="radio" name="amount" value="50"><span>£50</span></label>
                <label class="amount"><input type="radio" name="amount" value="120"><span>£120</span></label>
              </div>
            </fieldset>
            <p class="impact" data-impact aria-live="polite"></p>
            <label class="check"><input type="checkbox" id="giftaid"> I’m a UK taxpayer. Add Gift Aid (+25% at no cost to me).</label>
            <button class="btn" type="submit" data-donate-btn>Donate £25</button>
            <p class="note" data-donate-note role="status"></p>
          </form>
        </div>
      </div>
    </section>

    <section class="section section--rule" aria-labelledby="other-title">
      <div class="wrap">
{section_head('Other ways to give', 'Trusts, businesses and legacies', '', id_='other-title')}
        <ul class="band">
          <li><p class="eyebrow">Trusts and foundations</p><h3>Fund a season</h3><p>Our learning and access work is supported by trusts across the South West. Our director will gladly talk through what your grant could do.</p></li>
          <li><p class="eyebrow">Businesses</p><h3>Corporate partners</h3><p>Sponsor an exhibition, a family workshop series or the school bus fund, with staff visits and use of the Granary.</p></li>
          <li><p class="eyebrow">Legacies</p><h3>Leave a gift in your will</h3><p>A gift of any size helps keep entry free for young people. Email <span class="mono">giving@brueyard.org.uk</span> for a confidential conversation.</p></li>
        </ul>
      </div>
    </section>
'''
    layout('support.html', title='Support Us', desc='Become a Friend of The Brue Yard, donate to the rural school bus fund, or support us as a trust, business or legacy.', body=body, current='support')

def text_page(path, title, eyebrow, standfirst, sections, desc, extra=''):
    root = ''
    toc = ''.join(f'<li><a href="#{sid}">{h}</a></li>' for sid, h, _ in sections)
    secs = ''.join(f'<section id="{sid}" aria-labelledby="{sid}-h"><h2 id="{sid}-h">{h}</h2>{c}</section>' for sid, h, c in sections)
    body = page_head(root, [(path, title)], eyebrow, title, standfirst)
    body += f'''
    <section class="section section--tight">
      <div class="wrap textpage">
        <nav class="toc" aria-label="On this page"><p class="eyebrow">On this page</p><ol>{toc}</ol></nav>
        <div class="prose">{secs}{extra}<p class="updated">Last reviewed October 2026.</p></div>
      </div>
    </section>
'''
    layout(path, title=title, desc=desc, body=body)

def footer_pages():
    text_page('accessibility.html', 'Accessibility Statement', 'Access for everyone',
      'We want everyone to be able to visit the Yard and use this website. This page covers both.',
      [('site', 'Visiting the Yard', '<p>All three buildings are step-free, with level thresholds and accessible toilets including a Changing Places room. The meadow trail is mown grass with two gentle slopes. All-terrain manual wheelchairs are free to borrow.</p><ul><li>Carers and personal assistants come free.</li><li>Quiet sensory hour every Thursday, 10:00–11:30.</li><li>Visual stories, tactile large-print maps and ear defenders at the Welcome Desk.</li><li>Hearing loops in the Community Barn, Granary Room and at the desk.</li><li>BSL-interpreted family workshops every Saturday, and audio-described tours monthly.</li></ul>'),
       ('website', 'This website', '<p>This website aims to meet the Web Content Accessibility Guidelines (WCAG) 2.1 at level AA. You can:</p><ul><li>use it with a keyboard alone, with a visible focus ring on every control</li><li>use it with screen readers, which announce filter results and ticket totals as they change</li><li>zoom to 400% without losing content</li><li>turn off animation by choosing reduced motion in your device settings</li><li>use it in light or dark mode</li></ul>'),
       ('known', 'Known issues', '<p>Some photographs are stand-in images with shorter descriptions than we would like. We will replace them, with full descriptions, after our photography commission.</p>'),
       ('contact', 'Tell us what doesn’t work', '<p>If something on the site or at the Yard gets in your way, email <span class="mono">access@brueyard.org.uk</span> or call <span class="mono">01749 555 018</span>. We aim to reply within five working days.</p>')],
      'How The Brue Yard and its website work for disabled visitors, and how to tell us when something doesn’t.')
    text_page('governance.html', 'Code of Governance', 'How we are run',
      'The Brue Yard is a registered charity governed by a board of volunteer trustees.',
      [('charity', 'The charity', '<p>The Brue Yard Contemporary &amp; Sculpture Meadows is a charitable incorporated organisation, registered with the Charity Commission for England and Wales, number 1189034.</p>'),
       ('board', 'Board of trustees', '<p>Nine trustees, at least three of whom live in Bruton or the surrounding parishes, serve terms of three years, renewable once. The board meets six times a year and publishes its minutes here.</p>'),
       ('code', 'Charity Governance Code', '<p>We follow the Charity Governance Code for smaller charities and review our practice against it every year, publishing what we have changed in our annual report.</p>'),
       ('reports', 'Annual reports', '<p>Our annual report and accounts are published each January and filed with the Charity Commission.</p>')],
      'How The Brue Yard is governed: trustees, the Charity Governance Code and annual reports.')
    form = '''<form class="enquiry" data-enquiry novalidate aria-labelledby="enquire-h">
          <h2 id="enquire-h">Make an enquiry</h2>
          <div class="grid2">
            <div class="field"><label for="q-name">Your name</label><input id="q-name" name="name" required autocomplete="name"><p class="error" aria-live="polite"></p></div>
            <div class="field"><label for="q-email">Email address</label><input id="q-email" name="email" type="email" required autocomplete="email"><p class="error" aria-live="polite"></p></div>
            <div class="field"><label for="q-space">Space</label><select id="q-space" name="space" class="select"><option>The Threshing Barn</option><option>The Community Barn</option><option>The Granary Room</option><option>Not sure yet</option></select></div>
            <div class="field"><label for="q-date">Preferred date</label><input id="q-date" name="date" type="date"></div>
          </div>
          <div class="field"><label for="q-msg">Tell us about your event</label><textarea id="q-msg" name="message" rows="4" required></textarea><p class="error" aria-live="polite"></p></div>
          <button class="btn" type="submit">Send enquiry</button>
          <p class="success" role="status" hidden></p>
        </form>'''
    text_page('venue-hire.html', 'Venue Hire', 'Spaces to hire',
      'Three historic spaces for weddings, meetings, rehearsals and celebrations, with income going straight back into the charity.',
      [('spaces', 'The spaces', '<div class="table-wrap"><table class="spaces"><thead><tr><th scope="col">Space</th><th scope="col">Seated</th><th scope="col">Standing</th><th scope="col">Good for</th></tr></thead><tbody><tr><th scope="row">The Threshing Barn</th><td class="mono">140</td><td class="mono">200</td><td>Evening receptions, after hours</td></tr><tr><th scope="row">The Community Barn</th><td class="mono">120</td><td class="mono">150</td><td>Concerts, ceilidhs, talks</td></tr><tr><th scope="row">The Granary Room</th><td class="mono">40</td><td class="mono">60</td><td>Meetings, workshops, dinners</td></tr></tbody></table></div>'),
       ('community', 'Community rates', '<p>Bruton charities and community groups hire the Community Barn at cost. Ask us for the current rate.</p>'),
       ('catering', 'Catering and bar', '<p>The Granary Café caters for daytime events. For evenings we work with three Somerset caterers and run our own bar.</p>')],
      'Hire the Threshing Barn, Community Barn or Granary Room at The Brue Yard in Bruton for events and meetings.', extra=form)
    text_page('environment.html', 'Environmental Policy', 'Twelve acres to look after',
      'We run a gallery in a floodplain meadow, so our footprint and the river’s health are the same question.',
      [('energy', 'Energy', '<p>The barns are heated by ground-source heat pumps under the North Meadow, and the roof of the South Courtyard carries 60 kW of solar panels. We buy the rest from a renewable supplier.</p>'),
       ('meadow', 'The meadow and river', '<p>The North Meadow is cut once a year, in late summer, to keep its wildflowers. The wet meadow dug in 2024 slows floodwater above Bruton and has brought back water voles.</p>'),
       ('travel', 'Travel', '<p>Most of our visitors’ carbon comes from getting here. We put train times first in every listing, give 10% off café orders for anyone with a same-day rail ticket, and provide secure bike racks.</p>'),
       ('exhibitions', 'Exhibitions', '<p>We reuse plinths and walls between shows, ship loans together where we can, and follow the Gallery Climate Coalition’s guidance.</p>')],
      'How The Brue Yard reduces its environmental impact: energy, meadow management, visitor travel and exhibitions.')
    text_page('privacy.html', 'Privacy Policy', 'Your data',
      'What we collect when you book, subscribe or donate, why we collect it, and how to ask us to delete it.',
      [('what', 'What we collect', '<p>When you book we collect your name, email address and the tickets you choose. If you subscribe to the Journal we keep your email address. If you donate with Gift Aid we keep the details HMRC requires.</p>'),
       ('why', 'Why', '<p>To send your tickets, tell you about changes to your booking, send the Journal if you asked for it, and claim Gift Aid. We never sell your data.</p>'),
       ('cookies', 'Cookies', '<p>This site stores one preference in your browser: whether you last viewed the programme as a grid or a list. We use no tracking or advertising cookies.</p>'),
       ('rights', 'Your rights', '<p>You can ask to see, correct or delete what we hold about you at any time. Email <span class="mono">privacy@brueyard.org.uk</span>.</p>')],
      'How The Brue Yard collects and uses personal data from bookings, the Journal and donations.')

def not_found():
    root = ''
    body = page_head(root, [('404.html', 'Page not found')], 'Error 404', 'This path doesn’t lead anywhere',
                     'The page may have moved when the season changed. Try the programme, or head back to the start.',
                     extra='\n        <div class="hero__actions" style="margin-top:24px"><a class="btn" href="whats-on.html">See What’s On</a><a class="link-arrow" href="index.html">Back to the home page →</a></div>')
    layout('404.html', title='Page not found', desc='Page not found.', body=body)

# =====================================================================
def write_data():
    data = dict(events=EVENTS, extra=EXTRA, closed=CLOSED, seasonEnd=SEASON_END,
                photos={k: dict(id=v[0], who=v[1], href=v[2], alt=v[3]) for k, v in PHOTOS.items()})
    (HERE / 'assets' / 'data.js').write_text('/* Generated by build.py. Edit the data there, then run `python3 build.py`. */\nwindow.BY = '
                                             + json.dumps(data, ensure_ascii=False, indent=1) + ';\n')

if __name__ == '__main__':
    write_data()
    home(); whats_on(); exhibition(); exhibitions(); visit(); learning(); support(); footer_pages(); not_found()
    for ev in EVENTS:
        event_page(ev)
    print('Built', len(list(HERE.glob('*.html'))) + len(list((HERE / 'events').glob('*.html'))) + len(list((HERE / 'exhibitions').glob('*.html'))), 'pages')
