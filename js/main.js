/* whatsthepoint.to — main.js */

// ── Nav toggle (mobile) ───────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.querySelector('.nav-toggle');
  const nav    = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', () => {
      nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', nav.classList.contains('open'));
    });
  }

  // Active nav link
  const links = document.querySelectorAll('.main-nav a');
  const current = window.location.pathname.split('/').pop() || 'index.html';
  links.forEach(link => {
    if (link.getAttribute('href') === current) link.classList.add('active');
  });

  // Live date in masthead
  const dateBanner = document.querySelector('.date-banner__date');
  if (dateBanner) {
    const opts = { weekday:'long', year:'numeric', month:'long', day:'numeric' };
    dateBanner.textContent = new Date().toLocaleDateString('en-GB', opts);
  }

  // Scroll reveal
  const revealEls = document.querySelectorAll('.reveal');
  const io = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  revealEls.forEach(el => io.observe(el));

  // Newsletter form
  const newsletterForm = document.querySelector('.newsletter-form');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', e => {
      e.preventDefault();
      const btn = newsletterForm.querySelector('button');
      const input = newsletterForm.querySelector('input');
      if (input.value) {
        btn.textContent = 'Subscribed ✓';
        btn.style.background = '#2d6a4f';
        input.value = '';
        input.disabled = true;
        btn.disabled = true;
      }
    });
  }

  // Contact form
  const contactForm = document.querySelector('.contact-form');
  if (contactForm) {
    contactForm.addEventListener('submit', e => {
      e.preventDefault();
      const btn = contactForm.querySelector('.submit-btn');
      btn.textContent = 'Message Sent ✓';
      btn.style.background = '#2d6a4f';
      btn.disabled = true;
    });
  }

  // Archive filter buttons
  const filterBtns = document.querySelectorAll('.filter-btn');
  if (filterBtns.length) {
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const tag = btn.dataset.tag;
        const posts = document.querySelectorAll('.archive-post-item');
        posts.forEach(post => {
          if (tag === 'all' || post.dataset.tags?.includes(tag)) {
            post.style.display = 'grid';
          } else {
            post.style.display = 'none';
          }
        });
      });
    });
  }
});
