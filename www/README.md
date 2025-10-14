# Barsoom MUD Website

This directory contains the promotional website for Barsoom MUD, a Mars-themed Multi-User Dungeon based on Edgar Rice Burroughs' classic novels.

## Files

- `index.html` - Landing page with call-to-action
- `classes.html` - Character classes overview
- `races.html` - Playable races information
- `world.html` - World setting and lore
- `technology.html` - Technology system details
- `style.css` - Mars-themed styling

## Deployment

Simply copy all files in this directory to your web hosting service. The site is:

- **Static HTML/CSS only** - No JavaScript, no build process required
- **No dependencies** - Just HTML and CSS files
- **Mobile responsive** - Works on all screen sizes
- **Self-contained** - All styling is in style.css

## Testing Locally

You can test the website locally with any HTTP server:

```bash
cd www
python3 -m http.server 8080
```

Then visit http://localhost:8080 in your browser.

## Game Client Link

All "Play Now" buttons link to:
https://dikuclient.morpheum.dev/?server=barsoom.morpheum.dev&port=4000

## Design Notes

The site uses a Mars color palette:

- Mars red (#cd5c5c, #8b3a3a)
- Mars orange (#ff8c42)
- Mars sand/gold (#daa520)
- Night sky gradients (#1a0f08, #2c1810)
- Light text (#f4e4d7) with gold accents (#ffcc66)

Typography uses Georgia serif font for a classic, literary feel appropriate to the Edgar Rice Burroughs source material.
