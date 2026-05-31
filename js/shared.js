/* shared.js — injects header and footer into every page */

const SITE_NAME    = "What's The Point.";
const SITE_TAGLINE = "Clear-eyed thinking on AI, strategy & the enterprise";

function renderHeader() {
  const current = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = [
    { href: 'index.html',    label: 'Home'      },
    { href: 'blog.html',     label: 'Blog'      },
    { href: 'about.html',    label: 'About'     },
    { href: 'speaking.html', label: 'Speaking'  },
    { href: 'contact.html',  label: 'Contact'   },
  ];

  return `
  <header>
    <div class="masthead">
      <div class="masthead__inner">
        <a href="index.html" class="masthead__logo">
          What's The Point<span class="dot">.</span>
        </a>
        <nav class="main-nav" role="navigation" aria-label="Main navigation">
          ${navLinks.map(l => `
            <a href="${l.href}" class="${l.href === current ? 'active' : ''}">${l.label}</a>
          `).join('')}
        </nav>
        <a href="contact.html" class="masthead__cta">Hire for Consulting →</a>
        <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
    <div class="date-banner">
      <div class="date-banner__inner">
        <span class="date-banner__text date-banner__date">Loading…</span>
        <span class="date-banner__topics">
          AI Strategy <span>·</span> Enterprise ML <span>·</span> Consulting <span>·</span> Leadership
        </span>
      </div>
    </div>
  </header>`;
}

function renderFooter() {
  return `
  <footer>
    <div class="footer-grid">
      <div class="footer-brand">
        <h3>What's The Point<span style="color:var(--accent)">.</span></h3>
        <p>Honest, direct writing on AI strategy, enterprise transformation, and what actually matters in the age of machine intelligence.</p>
      </div>
      <div class="footer-col">
        <h4>Navigate</h4>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="speaking.html">Speaking</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Topics</h4>
        <ul>
          <li><a href="blog.html">AI Strategy</a></li>
          <li><a href="blog.html">Enterprise ML</a></li>
          <li><a href="blog.html">Leadership</a></li>
          <li><a href="blog.html">Ethics & Risk</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Connect</h4>
        <ul>
          <li><a href="https://linkedin.com" target="_blank">LinkedIn</a></li>
          <li><a href="https://twitter.com" target="_blank">Twitter / X</a></li>
          <li><a href="https://github.com" target="_blank">GitHub</a></li>
          <li><a href="mailto:hello@whatsthepoint.to">Email</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2025 whatsthepoint.to — All rights reserved</span>
      <span>Hosted on GitHub Pages · Custom domain</span>
    </div>
  </footer>`;
}

document.addEventListener('DOMContentLoaded', () => {
  const headerSlot = document.getElementById('site-header');
  const footerSlot = document.getElementById('site-footer');
  if (headerSlot) headerSlot.outerHTML = renderHeader();
  if (footerSlot)  footerSlot.outerHTML = renderFooter();
});
