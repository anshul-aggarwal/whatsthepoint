/* shared.js — injects header and footer into every page */

const GTAG = `<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-B9XYVRJE07"><\/script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-B9XYVRJE07');
<\/script>`;

function renderHeader() {
  const current = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = [
    { href: 'index.html',  label: 'Home'    },
    { href: 'blog.html',   label: 'Blog'    },
    { href: 'about.html',  label: 'About'   },
    { href: 'contact.html',label: 'Contact' },
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
        <a href="contact.html" class="masthead__cta">Work with Me →</a>
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
        <div style="margin-top:1.25rem;display:flex;gap:0.75rem;">
          <a href="https://linkedin.com/in/anshul-aggarwal" target="_blank" rel="noopener" aria-label="LinkedIn"
             style="display:inline-flex;align-items:center;justify-content:center;width:36px;height:36px;background:#0077b5;color:#fff;font-size:0.75rem;font-family:var(--font-mono);font-weight:600;text-decoration:none;transition:opacity 0.15s;"
             onmouseover="this.style.opacity='0.8'" onmouseout="this.style.opacity='1'">in</a>
        </div>
      </div>
      <div class="footer-col">
        <h4>Navigate</h4>
        <ul>
          <li><a href="index.html">Home</a></li>
          <li><a href="blog.html">Blog</a></li>
          <li><a href="about.html">About</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Topics</h4>
        <ul>
          <li><a href="blog.html">AI Strategy</a></li>
          <li><a href="blog.html">Enterprise ML</a></li>
          <li><a href="blog.html">Leadership</a></li>
          <li><a href="blog.html">Ethics &amp; Risk</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Connect</h4>
        <ul>
          <li><a href="https://linkedin.com/in/anshul-aggarwal" target="_blank" rel="noopener">LinkedIn</a></li>
          <li><a href="contact.html">Get in Touch</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© ${new Date().getFullYear()} Anshul Aggarwal · whatsthepoint.to</span>
      <span>Hosted on GitHub Pages</span>
    </div>
  </footer>`;
}

document.addEventListener('DOMContentLoaded', () => {
  const headerSlot = document.getElementById('site-header');
  const footerSlot = document.getElementById('site-footer');
  if (headerSlot) headerSlot.outerHTML = renderHeader();
  if (footerSlot)  footerSlot.outerHTML = renderFooter();

  // Inject gtag into <head> dynamically
  const gtagDiv = document.createElement('div');
  gtagDiv.innerHTML = GTAG;
  // gtag scripts are already on the page via inline in each HTML file
});
