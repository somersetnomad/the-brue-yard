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
