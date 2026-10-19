# The Brue Yard: case study

**Live site:** https://somersetnomad.github.io/the-brue-yard/
**Code:** https://github.com/somersetnomad/the-brue-yard
**Role:** design and front-end development
**Stack:** semantic HTML, modern CSS (custom properties, grid, scroll-driven animation), vanilla JavaScript, and a small Python build script

---

## The brief

The Brue Yard is a contemporary gallery with sculpture meadows and a community performance barn in Bruton, Somerset. (The venue is fictional; the town, the river and the railway are real.) The site had to:

- launch the autumn/winter exhibition, *Echoes Across the Valley*
- let visitors filter a mixed programme of exhibitions, music, family workshops, walks and talks
- get people to a rural venue, mostly by train and on foot
- sell timed-entry and event tickets without leaving the page
- meet WCAG 2.1 AA, with no frameworks and no build step needed to run it

The visual direction was cultural-sector editorial: archival paper tones, crisp 1px rules, strict type hierarchy and a single Somerset ochre accent.

## The problem

Small cultural venues usually end up with one of two sites: a template that looks like every other gallery, or an agency build with a CMS they can't afford. Both tend to share the same weaknesses:

- **Booking is a cliff edge.** Visitors leave the venue's site for a ticketing platform and lose context.
- **Listings are flat.** A card shows a title and a date. Everything a visitor actually needs to decide (how long it takes, whether it suits a seven-year-old, what to wear, whether it's step-free) is a click and a page load away.
- **Getting there is an afterthought,** even though for a rural venue it is often the biggest barrier.

## Key decisions

### 1. Booking without leaving the page
Every "Book" button on every page opens the same slide-out drawer, already set to that event, and to a date if you picked one from a listing. It works in four steps: date and time, tickets, an optional £3 donation, and a summary. A sticky tray keeps the running total in view and counts up as tickets are added. Sold-out slots are disabled, and ticket counters stop at the seats left. The checkout button explains exactly what's missing instead of failing silently.

### 2. Cards that answer the next question
Each event card turns over to show length, who it suits, what to bring, access detail and the next four dates. Each date opens booking with that day chosen. Visitors can compare events without opening a single page. Each event still has its own page for search engines and sharing.

### 3. No dead space
Reviewing the first build showed gaps: a lone card at the end of the grid, and an essay column that ran out beside a tall map. Each became something useful:
- **Gap tile.** The end of a short grid row fills with a two-week calendar. Choose a day and the tile lists what's on.
- **Commission finder.** The essay column gained a list of the four riverside commissions. Choosing one rings its marker on a generated contour map of the valley.

### 4. A photography system, not just photos
Images sit in fixed-ratio frames (4:5 hero, 3:2 cards, 21:9 river plate) with responsive `srcset`, photographer credits and a captioned fallback if an image fails to load. The site launched with credited, free-licence stand-ins and swapped one that didn't feel like Somerset. The frames mean the commissioned shoot can drop straight in.

### 5. Motion that responds to the visitor
There's one orchestrated moment on load, when the hero headline rises and the photo unveils. After that, motion only follows interaction or scrolling: cards lift and turn, sections rise into place, the river on the map flows while it's on screen. All of it switches off under `prefers-reduced-motion`, and the page is fully readable before any of it runs.

### 6. Accessibility as structure
- Modal dialogs (mobile menu and booking drawer) trap focus, close with Escape and return focus to the button that opened them.
- Filter results, ticket totals and map selections are announced through live regions.
- Category filters behave as a keyboard tab list.
- There is a visible focus ring on every control, AA contrast in light and dark modes, and touch targets of at least 44px.

### 7. One layout, plain HTML out
The site grew from one page to twenty. A small Python script holds the layout and event data and writes every page as static HTML, so there's one source for the header, footer, menu and booking drawer. The output needs no build step and no server to run, and the same event data drives both the static event pages and the interactive programme.

## What's in it

- 20 pages: home, What's On, 7 event pages, the exhibition, Exhibitions & Grounds, Plan Your Visit, Learning & Community, Support Us, 5 footer pages and a 404
- Zero runtime dependencies
- Light and dark themes
- Every page checked at desktop and phone width for script errors, broken links and horizontal overflow

## What I'd do next

- **CMS:** connect the event data to a headless CMS so venue staff can edit listings.
- **Ticketing:** replace the mock checkout with a real integration such as Spektrix or Tessitura.
- **Photography:** commission a shoot of the barns, meadow and works.
- **Testing:** test with screen-reader users and on real devices, then commission a formal accessibility audit.

## Tools

HTML, CSS, JavaScript and Python, with Playwright for automated page checks and AI-assisted coding during implementation. Photography from Unsplash under the Unsplash Licence.
