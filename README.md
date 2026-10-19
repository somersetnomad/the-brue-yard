# The Brue Yard

Read the [case study](CASE-STUDY.md) for the brief and design decisions.

Website prototype for **The Brue Yard Contemporary & Sculpture Meadows**, Bruton, Somerset.

Open `index.html` in a browser, or serve the folder. The pages are plain HTML with no dependencies
(fonts load from Google Fonts), so the site runs without a build step.

## Pages

| Page | File |
|---|---|
| Home | `index.html` |
| What's On (filterable programme) | `whats-on.html` |
| Event pages (7) | `events/*.html` |
| Exhibition: Echoes Across the Valley | `exhibitions/echoes-across-the-valley.html` |
| Exhibitions & Grounds | `exhibitions.html` |
| Plan Your Visit | `visit.html` |
| Learning & Community | `learning.html` |
| Support Us | `support.html` |
| Accessibility, Governance, Venue Hire, Environment, Privacy | footer pages |
| Not found | `404.html` |

## How it's built

- `assets/site.css`: all styles
- `assets/site.js`: shared behaviour; each feature starts only when its markup is on the page
- `assets/data.js`: events, photos and season dates (generated)
- `src/partials/`: shared sections (hero, ticker, programme filters, booking drawer, footer)
- `build.py`: the layout, page content and event data

To change content, edit `build.py` or a partial, then run `python3 build.py`. It rewrites every page
and `assets/data.js`. Commit the output; the live site never runs the build.

## What's in it

- Utility strip with live opening status, sticky header, keyboard-trapped mobile menu
- Exhibition masthead for *Echoes Across the Valley* (24 Oct 2026 – 28 Feb 2027)
- What's On: filter by date, type and access provision, grid/list toggle, live result count
- Plan Your Visit: train, walking and parking directions, opening hours, access amenities
- Slide-out ticket drawer: date and time slots, ticket tiers, £3 school bus donation, live total
- Journal sign-up with inline validation; supporter ribbon and footer links

## Motion and interaction

- Event cards flip to show length, suitability, what to bring, access detail and the next four dates.
  Each date opens the booking drawer with that day already chosen.
- A "Coming up" ticker under the hero lists the next dates. It pauses on hover, on focus or with its pause button.
- When the last row of cards is short, a "Pick a date and go" tile fills the gap.
- The hero animates in on load, the river on the contour map flows while it's on screen, and sections
  rise into place as you scroll (in browsers with scroll-driven animations; content is fully visible otherwise).
- The ticket total counts up as you add tickets.
- All motion stops for visitors who choose reduced motion in their system settings.

## Accessibility

Built to WCAG 2.1 AA: visible focus rings, `aria-live` updates for results and order totals,
modal dialogs with focus trapping and Escape to close, and light and dark colour schemes.

## Prototype limits

Event data, slot availability and checkout are mocked in `index.html`. The checkout button
ends at a "basket held" screen where a real ticketing integration would take over.

## Photography

The page uses stand-in photography from [Unsplash](https://unsplash.com), under the free
Unsplash Licence (no Unsplash+ images). Every image carries a photographer credit. Images are
hotlinked from `images.unsplash.com` with responsive `srcset` sizes, as Unsplash asks.

To swap in the commissioned shoot, replace the photo IDs in the `PHOTOS` object in the script
(event cards) and the `<img>` tags in the hero, grounds and learning sections. Frames are fixed
ratio (4:5 hero, 3:2 cards, 21:9 river plate), so any photo cropped to those ratios drops in.

If an image fails to load, its frame falls back to a captioned placeholder rather than a broken icon.

## Viewing it live

Turn on GitHub Pages under **Settings → Pages → Deploy from a branch → `main` / root**.
The site then appears at `https://somersetnomad.github.io/the-brue-yard/`.
