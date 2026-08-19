const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

/* Mobile nav toggle (only present on the main page header) */
const navToggle = document.getElementById('navToggle');
const nav = document.getElementById('nav');
if (navToggle && nav) {
  navToggle.addEventListener('click', () => {
    const isOpen = nav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', isOpen);
  });
  document.querySelectorAll('#navLinks a').forEach(a => {
    a.addEventListener('click', () => nav.classList.remove('is-open'));
  });
}

/* Scroll reveal */
const revealEls = document.querySelectorAll(
  '.section-kicker, .section-title, .section-sub, .about-grid, .tl-item, .award-card, .project-card, .skill-card, .contact-panel'
);
revealEls.forEach(el => el.classList.add('reveal'));

const io = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('is-visible');
      io.unobserve(entry.target);
    }
  });
}, { threshold: 0.12, rootMargin: '0px 0px -60px 0px' });

revealEls.forEach(el => io.observe(el));

/* Stagger project cards slightly */
document.querySelectorAll('.project-card').forEach((card, i) => {
  card.style.transitionDelay = `${(i % 3) * 70}ms`;
});

/* Project filter */
const filterBar = document.getElementById('filterBar');
const cards = document.querySelectorAll('.project-card');
if (filterBar) {
  filterBar.addEventListener('click', (e) => {
    const btn = e.target.closest('.filter-chip');
    if (!btn) return;
    filterBar.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('is-active'));
    btn.classList.add('is-active');
    const filter = btn.dataset.filter;
    cards.forEach(card => {
      const tags = card.dataset.tags || '';
      const show = filter === 'all' || tags.includes(filter);
      card.classList.toggle('is-hidden', !show);
    });
  });
}

/* Active nav link highlighting */
const sections = document.querySelectorAll('main section[id]');
const navLinks = document.querySelectorAll('#navLinks a');
const navObserver = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    const id = entry.target.getAttribute('id');
    const link = document.querySelector(`#navLinks a[href="#${id}"]`);
    if (!link) return;
    if (entry.isIntersecting) {
      navLinks.forEach(l => l.classList.remove('is-current'));
      link.classList.add('is-current');
    }
  });
}, { threshold: 0.4, rootMargin: '-68px 0px -50% 0px' });
sections.forEach(s => navObserver.observe(s));
