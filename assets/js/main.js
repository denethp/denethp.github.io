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
const projectGrid = document.getElementById('projectGrid');
const cards = document.querySelectorAll('.project-card');
// Remember each card's original link wrapper in its natural (unfiltered) order,
// so switching back to "All" restores the original layout rather than leaving
// things in whatever order the last filter left them in.
const cardLinksInOriginalOrder = projectGrid
  ? Array.from(projectGrid.querySelectorAll('.project-card-link'))
  : [];
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
    // Beyond just hiding non-matches, actually re-pack the grid: matching
    // cards move to the front (in their original relative order) so a
    // filtered view reads as its own tight group instead of leaving the
    // selection scattered across where the cards happened to start.
    if (projectGrid && cardLinksInOriginalOrder.length) {
      const matching = [];
      const rest = [];
      cardLinksInOriginalOrder.forEach(link => {
        const card = link.querySelector('.project-card');
        const tags = card?.dataset.tags || '';
        const show = filter === 'all' || tags.includes(filter);
        (show ? matching : rest).push(link);
      });
      matching.concat(rest).forEach(link => projectGrid.appendChild(link));
    }
  });
}

/* Project detail gallery */
const galleryMain = document.getElementById('galleryMain');
const presentationMedia = document.getElementById('presentationMedia');
const galleryThumbs = document.querySelectorAll('.gallery-thumb');
if (galleryMain && galleryThumbs.length) {
  galleryThumbs.forEach(thumb => {
    thumb.addEventListener('click', () => {
      if (thumb.dataset.type === 'presentation') {
        // Switch the main viewer back to the presentation CTA (a real link,
        // so clicking the big card itself still navigates out normally).
        if (presentationMedia) presentationMedia.classList.add('is-active');
        galleryMain.style.display = 'none';
      } else {
        if (presentationMedia) presentationMedia.classList.remove('is-active');
        galleryMain.style.display = '';
        galleryMain.src = thumb.dataset.src;
        galleryMain.alt = thumb.dataset.alt || '';
      }
      galleryThumbs.forEach(t => t.classList.remove('is-active'));
      thumb.classList.add('is-active');
    });
  });
}

/* Lightbox — click the big project image to view it uncropped, full-size */
const projMediaImgs = document.querySelectorAll('.proj-media > img');
if (projMediaImgs.length) {
  const overlay = document.createElement('div');
  overlay.className = 'lightbox-overlay';
  overlay.innerHTML = '<button class="lightbox-close" aria-label="Close">&times;</button><img class="lightbox-img" alt="">';
  document.body.appendChild(overlay);
  const lightboxImg = overlay.querySelector('.lightbox-img');
  const lightboxClose = overlay.querySelector('.lightbox-close');

  const openLightbox = (src, alt) => {
    lightboxImg.src = src;
    lightboxImg.alt = alt || '';
    overlay.classList.add('is-open');
    document.body.classList.add('lightbox-open');
  };
  const closeLightbox = () => {
    overlay.classList.remove('is-open');
    document.body.classList.remove('lightbox-open');
  };

  projMediaImgs.forEach(img => {
    img.addEventListener('click', () => openLightbox(img.src, img.alt));
  });
  lightboxClose.addEventListener('click', closeLightbox);
  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeLightbox();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeLightbox();
  });
}

/* Video run demos: whether a video is available is now decided at build time
   (gen_projects.py checks the file exists and bakes an "is-missing" class into the HTML),
   so no client-side check is needed here — this keeps it working identically whether the
   page is opened via file://, a local server, or the live GitHub Pages site. */

/* Video lightbox — click the expand button on a run card to zoom it on a blurred backdrop,
   matching the image lightbox above. */
const videoCards = document.querySelectorAll('.video-card:not(.is-missing)');
if (videoCards.length) {
  const vOverlay = document.createElement('div');
  vOverlay.className = 'lightbox-overlay lightbox-video-overlay';
  vOverlay.innerHTML = '<button class="lightbox-close" aria-label="Close">&times;</button><video class="lightbox-video" controls playsinline></video><iframe class="lightbox-yt" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>';
  document.body.appendChild(vOverlay);
  const lightboxVideo = vOverlay.querySelector('.lightbox-video');
  const lightboxYt = vOverlay.querySelector('.lightbox-yt');
  const vClose = vOverlay.querySelector('.lightbox-close');

  const openVideoLightbox = (card) => {
    const ytId = card.dataset.ytId;
    const label = card.dataset.videoLabel || '';
    if (ytId) {
      lightboxVideo.style.display = 'none';
      lightboxVideo.pause();
      lightboxVideo.removeAttribute('src');
      lightboxYt.style.display = 'block';
      lightboxYt.setAttribute('title', label);
      lightboxYt.src = `https://www.youtube.com/embed/${ytId}?autoplay=1&rel=0`;
    } else {
      lightboxYt.style.display = 'none';
      lightboxYt.src = '';
      lightboxVideo.style.display = 'block';
      lightboxVideo.src = card.dataset.videoSrc;
      lightboxVideo.setAttribute('aria-label', label);
      lightboxVideo.play().catch(() => {});
    }
    vOverlay.classList.add('is-open');
    document.body.classList.add('lightbox-open');
  };
  const closeVideoLightbox = () => {
    vOverlay.classList.remove('is-open');
    document.body.classList.remove('lightbox-open');
    lightboxVideo.pause();
    lightboxVideo.removeAttribute('src');
    lightboxVideo.load();
    lightboxYt.src = '';
  };

  videoCards.forEach(card => {
    const isYt = card.classList.contains('yt-card');
    const trigger = (e) => {
      e.preventDefault();
      e.stopPropagation();
      const inlineVideo = card.querySelector('video');
      if (inlineVideo) inlineVideo.pause();
      openVideoLightbox(card);
    };
    const btn = card.querySelector('.video-expand-btn');
    if (btn) btn.addEventListener('click', trigger);
    if (isYt) card.addEventListener('click', trigger);
  });
  vClose.addEventListener('click', closeVideoLightbox);
  vOverlay.addEventListener('click', (e) => {
    if (e.target === vOverlay) closeVideoLightbox();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && vOverlay.classList.contains('is-open')) closeVideoLightbox();
  });
}

/* "Request CV" buttons: open a WhatsApp chat (pre-filled message) in a new
   tab AND scroll the current page down to the Contact section, so the visit
   naturally lands where the phone/email/LinkedIn details also live. */
document.querySelectorAll('.cv-request-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    const contact = document.getElementById('contact');
    if (contact) {
      // Already on the main page — just scroll down to it.
      contact.scrollIntoView({ behavior: 'smooth' });
    } else if (btn.dataset.contactUrl) {
      // On a project detail page — no #contact section here, so navigate
      // the current tab to the main page's contact section instead (the
      // WhatsApp link itself still opens separately in a new tab).
      window.location.href = btn.dataset.contactUrl;
    }
  });
});

/* Active nav link highlighting.
   An IntersectionObserver keyed on "40% of the section visible" used to drive
   this, but that ratio is measured against each section's FULL height — a
   short section (About, Skills, Contact) clears 40% easily, but a long one
   (Education, Projects) is taller than the viewport itself, so 40% of its
   total area is never on screen at once and it silently never lit up while
   scrolled through the middle of it. Tracking "which section's top edge is
   the last one to have scrolled past the nav" instead works for any section
   height, since it only looks at the boundary, never the whole area. */
const sections = Array.from(document.querySelectorAll('main section[id]'));
const navLinks = document.querySelectorAll('#navLinks a');
function updateActiveNavLink() {
  const navHeight = document.getElementById('nav')?.offsetHeight || 0;
  const line = navHeight + 40; // a little past the sticky nav, into the page
  let current = sections[0];
  for (const sec of sections) {
    if (sec.getBoundingClientRect().top <= line) {
      current = sec;
    }
  }
  const id = current?.getAttribute('id');
  navLinks.forEach(l => l.classList.toggle('is-current', l.getAttribute('href') === `#${id}`));
}
let navTicking = false;
window.addEventListener('scroll', () => {
  if (navTicking) return;
  navTicking = true;
  requestAnimationFrame(() => { updateActiveNavLink(); navTicking = false; });
}, { passive: true });
window.addEventListener('resize', updateActiveNavLink);
updateActiveNavLink();
