# whatsthepoint.to — Personal Blog & Brand Site

A static HTML/CSS/JS blog and personal brand site for an AI consulting manager.
Designed for GitHub Pages with a custom domain (`whatsthepoint.to`).

---

## Site Structure

```
/
├── index.html          ← Homepage with latest posts
├── blog.html           ← Full post archive with tag filters
├── about.html          ← About the Author
├── speaking.html       ← Speaking, workshops & consulting services
├── contact.html        ← Contact form + info
├── post.html           ← Sample/template for blog posts
├── css/
│   └── style.css       ← All styles (design system)
├── js/
│   ├── shared.js       ← Header + footer injection
│   └── main.js         ← Interactivity (scroll, filters, forms)
├── CNAME               ← Custom domain config for GitHub Pages
├── _config.yml         ← GitHub Pages Jekyll config
└── README.md           ← This file
```

---

## Deployment to GitHub Pages

### 1. Create the repository

```bash
git init
git add .
git commit -m "Initial commit — whatsthepoint.to"
```

Create a new repo on GitHub (e.g. `yourusername/whatsthepoint`), then:

```bash
git remote add origin https://github.com/yourusername/whatsthepoint.git
git branch -M main
git push -u origin main
```

### 2. Enable GitHub Pages

1. Go to your repo → **Settings** → **Pages**
2. Source: **Deploy from a branch**
3. Branch: `main` / `/(root)`
4. Save

### 3. Configure your custom domain

In your GitHub Pages settings, add `whatsthepoint.to` as your custom domain.

Then go to your DNS provider (wherever `whatsthepoint.to` is registered) and add:

```
# For apex domain (whatsthepoint.to):
A     @     185.199.108.153
A     @     185.199.109.153
A     @     185.199.110.153
A     @     185.199.111.153

# For www redirect (optional):
CNAME www   yourusername.github.io
```

Wait for DNS propagation (up to 24h), then enable **Enforce HTTPS** in Pages settings.

The `CNAME` file in the repo root tells GitHub Pages which domain to serve from.

---

## Customisation Checklist

### Personal Details
- [ ] Replace "Your Name Here" in `about.html`
- [ ] Update the portrait placeholder in `about.html` with a real photo
- [ ] Fill in LinkedIn, GitHub, Twitter handles across all pages
- [ ] Update the email address from `hello@whatsthepoint.to`
- [ ] Update the career timeline in `about.html`
- [ ] Replace client logo placeholders in `speaking.html`

### Content
- [ ] Write and add your first real blog post (copy `post.html` as a template)
- [ ] Update featured post on `index.html` to point to a real post
- [ ] Fill in speaking history in `speaking.html`
- [ ] Update testimonials with real quotes (with permission)

### Forms
The contact form and newsletter form are currently demo-only.  
Wire them to a real backend:

- **Contact form**: [Formspree](https://formspree.io) (free tier works) — add `action="https://formspree.io/f/YOUR_ID"` to the `<form>` tag and remove the `novalidate` + JS override
- **Newsletter**: [Buttondown](https://buttondown.email) or [Substack](https://substack.com) — replace the newsletter form with their embed code

### Analytics
Add before `</body>` on each page:
```html
<!-- Plausible (privacy-friendly, recommended) -->
<script defer data-domain="whatsthepoint.to" src="https://plausible.io/js/script.js"></script>

<!-- Or Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
```

### SEO
- Add Open Graph meta tags to each page for social sharing previews
- Create a `sitemap.xml` once you have real post URLs
- Add a `robots.txt` if needed

---

## Writing New Posts

1. Copy `post.html` to a new file (e.g. `posts/my-post-title.html`)
2. Update the title, meta description, hero, and body content
3. Add the post to `blog.html` (archive) and `index.html` (latest posts)
4. Commit and push — GitHub Pages deploys automatically

**Future improvement**: Consider migrating to [Jekyll](https://jekyllrb.com/) or [Eleventy](https://www.11ty.dev/) for templating and automatic post management as the blog grows.

---

## Design System Notes

- **Fonts**: Playfair Display (display), IBM Plex Sans (body), IBM Plex Mono (UI/labels)
- **Colors**: `--ink` (near-black), `--paper` (warm off-white), `--accent` (editorial red `#d4380d`), `--accent-2` (deep navy)
- **Aesthetic**: Editorial brutalist — newspaper-meets-tech-blog
- All colours and spacing are CSS custom properties in `css/style.css`
