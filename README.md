# Chesham Taxis — website

Static marketing site for Chesham Taxis (Chesham, Buckinghamshire).
Homepage rebranded from a Framer template; sub-pages built on a shared design system (`assets/site.css`).

- Pages: index, about-us, taxi, services, pricing, reviews, drivers, cars-for-rental, contact-us
- Fully self-contained (all fonts/images/JS local under `assets/`)
- Rebuild sub-pages: `python3 build.py` (wraps `content/*.html` in the shared shell)
