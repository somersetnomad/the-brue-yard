# The Brue Yard

Single-page prototype for **The Brue Yard Contemporary & Sculpture Meadows**, Bruton, Somerset.

Open `index.html` in a browser. No build step and no dependencies (fonts load from Google Fonts).

## What's in it

- Utility strip with live opening status, sticky header, keyboard-trapped mobile menu
- Exhibition masthead for *Echoes Across the Valley* (24 Oct 2026 – 28 Feb 2027)
- What's On: filter by date, type and access provision, grid/list toggle, live result count
- Plan Your Visit: train, walking and parking directions, opening hours, access amenities
- Slide-out ticket drawer: date and time slots, ticket tiers, £3 school bus donation, live total
- Journal sign-up with inline validation; supporter ribbon and footer links

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
