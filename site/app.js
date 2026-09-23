/**
 * HydroGrow: Microsoft Fabric Smart Farming Platform
 * Client-side Controller & Interactive Handlers
 */

document.addEventListener('DOMContentLoaded', () => {
  initLightbox();
  initTabs();
  initCodeCopy();
  initScrollSpy();
  initMobileNav();
  initCounters();
  initProblemSwiper();
  initScrolltellingPipeline();
});

/**
 * Fullscreen Lightbox Modal Controller with Pan & Zoom
 */
function initLightbox() {
  const modal = document.getElementById('lightbox-modal');
  const modalImg = document.getElementById('lightbox-img');
  const modalCaption = document.getElementById('lightbox-caption');
  const closeBtn = document.getElementById('lightbox-close');
  const zoomInBtn = document.getElementById('lightbox-zoom-in');
  const zoomOutBtn = document.getElementById('lightbox-zoom-out');
  const zoomResetBtn = document.getElementById('lightbox-zoom-reset');
  const zoomLevelTag = document.getElementById('lightbox-zoom-level');
  const loader = document.getElementById('lightbox-loader');
  const viewport = document.getElementById('lightbox-viewport');

  if (!modal || !modalImg || !closeBtn) return;

  let scale = 1;
  let posX = 0;
  let posY = 0;
  let isDragging = false;
  let startX = 0;
  let startY = 0;

  function updateTransform() {
    modalImg.style.transform = `translate(${posX}px, ${posY}px) scale(${scale})`;
    if (zoomLevelTag) {
      zoomLevelTag.textContent = `${Math.round(scale * 100)}%`;
    }
    if (scale > 1) {
      modalImg.style.cursor = isDragging ? 'grabbing' : 'grab';
    } else {
      modalImg.style.cursor = 'default';
    }
  }

  function resetZoom() {
    scale = 1;
    posX = 0;
    posY = 0;
    updateTransform();
  }

  function zoomIn() {
    if (scale < 3.5) {
      scale = Math.min(3.5, scale + 0.35);
      updateTransform();
    }
  }

  function zoomOut() {
    if (scale > 0.6) {
      scale = Math.max(0.6, scale - 0.35);
      if (scale <= 1) {
        posX = 0;
        posY = 0;
      }
      updateTransform();
    }
  }

  // Hook up zoom buttons
  if (zoomInBtn) zoomInBtn.addEventListener('click', (e) => { e.stopPropagation(); zoomIn(); });
  if (zoomOutBtn) zoomOutBtn.addEventListener('click', (e) => { e.stopPropagation(); zoomOut(); });
  if (zoomResetBtn) zoomResetBtn.addEventListener('click', (e) => { e.stopPropagation(); resetZoom(); });

  // Mouse Wheel Zoom
  if (viewport) {
    viewport.addEventListener('wheel', (e) => {
      e.preventDefault();
      if (e.deltaY < 0) {
        zoomIn();
      } else {
        zoomOut();
      }
    }, { passive: false });
  }

  // Click & Drag to Pan (when zoomed in)
  modalImg.addEventListener('mousedown', (e) => {
    if (scale <= 1) return;
    isDragging = true;
    startX = e.clientX - posX;
    startY = e.clientY - posY;
    modalImg.style.cursor = 'grabbing';
    e.preventDefault();
  });

  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    posX = e.clientX - startX;
    posY = e.clientY - startY;
    updateTransform();
  });

  window.addEventListener('mouseup', () => {
    if (isDragging) {
      isDragging = false;
      modalImg.style.cursor = scale > 1 ? 'grab' : 'default';
    }
  });

  // Click triggers for any lightbox target
  const triggerElements = document.querySelectorAll('[data-lightbox-src]');
  triggerElements.forEach(el => {
    el.addEventListener('click', () => {
      const src = el.getAttribute('data-lightbox-src');
      const caption = el.getAttribute('data-lightbox-caption') || el.querySelector('.gallery-item-title')?.textContent || '';
      
      resetZoom();
      if (loader) loader.style.display = 'block';
      modalImg.style.opacity = '0';

      modalImg.onload = () => {
        if (loader) loader.style.display = 'none';
        modalImg.style.opacity = '1';
      };

      modalImg.src = src;
      modalCaption.textContent = caption;
      modal.classList.add('active');
      document.body.style.overflow = 'hidden';
    });
  });

  // Close handlers
  const closeModal = () => {
    modal.classList.remove('active');
    modalImg.src = '';
    modalCaption.textContent = '';
    resetZoom();
    document.body.style.overflow = '';
  };

  closeBtn.addEventListener('click', closeModal);

  modal.addEventListener('click', (e) => {
    // Only close if clicking outside viewport or controls
    if (e.target === modal) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (!modal.classList.contains('active')) return;
    if (e.key === 'Escape') {
      closeModal();
    } else if (e.key === '+' || e.key === '=') {
      zoomIn();
    } else if (e.key === '-' || e.key === '_') {
      zoomOut();
    } else if (e.key === '0') {
      resetZoom();
    }
  });
}

/**
 * Tab Switcher for Chapter 6 Exploration Hubs
 */
function initTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanels = document.querySelectorAll('.tab-panel');

  if (!tabBtns.length) return;

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.getAttribute('data-tab-target');

      // Update active button
      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      // Update active panel
      tabPanels.forEach(p => {
        if (p.id === targetId) {
          p.classList.add('active');
        } else {
          p.classList.remove('active');
        }
      });
    });
  });
}

/**
 * One-Click Code Snippet Copy Controller
 */
function initCodeCopy() {
  const copyBtns = document.querySelectorAll('.code-copy-btn');

  copyBtns.forEach(btn => {
    btn.addEventListener('click', async () => {
      const container = btn.closest('.mock-terminal') || btn.closest('.code-showcase');
      const codeBlock = container?.querySelector('code');
      if (!codeBlock) return;

      const codeText = codeBlock.textContent;

      try {
        await navigator.clipboard.writeText(codeText);
        const originalText = btn.textContent;
        btn.textContent = '✓ Copied!';
        btn.style.borderColor = 'var(--c-orange-accent)';
        btn.style.color = 'var(--c-orange-accent)';
        btn.style.backgroundColor = 'rgba(226, 115, 36, 0.15)';

        setTimeout(() => {
          btn.textContent = originalText;
          btn.style.borderColor = '';
          btn.style.color = '';
          btn.style.backgroundColor = '';
        }, 2200);
      } catch (err) {
        console.error('Clipboard copy failed:', err);
      }
    });
  });
}

/**
 * Navigation Scroll Spy for Active Chapter Highlighting
 */
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  if (!sections.length || !navLinks.length) return;

  const onScroll = () => {
    const scrollPos = window.scrollY + 160;

    sections.forEach(section => {
      const top = section.offsetTop;
      const height = section.offsetHeight;
      const id = section.getAttribute('id');

      if (scrollPos >= top && scrollPos < top + height) {
        navLinks.forEach(link => {
          link.classList.remove('active');
          const href = link.getAttribute('href');
          if (href === `#${id}` || (id === 'problem' && href === '#origin') || (id === 'build' && href === '#platform')) {
            link.classList.add('active');
          }
        });
      }
    });
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll(); // initial check
}

/**
 * Mobile Navigation Toggle
 */
function initMobileNav() {
  const toggleBtn = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (!toggleBtn || !navLinks) return;

  toggleBtn.addEventListener('click', () => {
    navLinks.classList.toggle('mobile-open');
  });

  navLinks.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('mobile-open');
    });
  });
}

/**
 * Animated Metric Number Counter Ticker
 */
function initCounters() {
  const counterElements = document.querySelectorAll('[data-counter]');
  if (!counterElements.length || !('IntersectionObserver' in window)) return;

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        animateCounter(entry.target);
        obs.unobserve(entry.target);
      }
    });
  }, { threshold: 0.25 });

  counterElements.forEach(el => observer.observe(el));
}

function animateCounter(el) {
  const target = parseFloat(el.getAttribute('data-counter'));
  const prefix = el.getAttribute('data-prefix') || '';
  const suffix = el.getAttribute('data-suffix') || '';
  const decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
  const duration = 1200; // ms
  const startTime = performance.now();

  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // Ease-out cubic easing curve
    const easeOut = 1 - Math.pow(1 - progress, 3);
    const currentVal = (target * easeOut).toFixed(decimals);

    el.textContent = `${prefix}${currentVal}${suffix}`;

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      el.textContent = `${prefix}${target.toFixed(decimals)}${suffix}`;
    }
  }

  requestAnimationFrame(update);
}

/**
 * 3D Coverflow Controller for Chapter 2 Physical Challenges
 */
function initProblemSwiper() {
  if (typeof Swiper === 'undefined') return;
  const swiperEl = document.querySelector('.problem-swiper');
  if (!swiperEl) return;

  new Swiper('.problem-swiper', {
    effect: 'coverflow',
    grabCursor: true,
    centeredSlides: true,
    slidesPerView: 'auto',
    initialSlide: 0,
    coverflowEffect: {
      rotate: 20,
      stretch: 0,
      depth: 120,
      modifier: 1.2,
      slideShadows: false,
    },
    pagination: {
      el: '.problem-pagination',
      clickable: true,
    },
    navigation: {
      nextEl: '.problem-nav-next',
      prevEl: '.problem-nav-prev',
    },
    keyboard: {
      enabled: true,
    },
  });
}

/**
 * Scrolltelling Data Pipeline Visualization Controller for Chapter 4
 */
function initScrolltellingPipeline() {
  const layerBlocks = document.querySelectorAll('.layer-block[data-layer-idx]');
  const navNodes = document.querySelectorAll('.pipeline-nav-node[data-target-layer]');
  const trackerDot = document.getElementById('pipeline-packet-dot');

  if (!layerBlocks.length || !navNodes.length) return;

  // Click on nav node to smoothly scroll to corresponding architecture layer
  navNodes.forEach(node => {
    node.addEventListener('click', () => {
      const idx = node.getAttribute('data-target-layer');
      const targetBlock = document.querySelector(`.layer-block[data-layer-idx="${idx}"]`);
      if (targetBlock) {
        targetBlock.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });
  });

  // Track scroll position of layers and illuminate pipeline path
  const onScroll = () => {
    let activeIdx = 1;
    const windowMiddle = window.scrollY + window.innerHeight * 0.45;

    layerBlocks.forEach(block => {
      const top = block.offsetTop;
      const idx = parseInt(block.getAttribute('data-layer-idx'), 10);

      if (windowMiddle >= top - 80) {
        activeIdx = idx;
      }
    });

    // Update active layer block classes
    layerBlocks.forEach(block => {
      const idx = parseInt(block.getAttribute('data-layer-idx'), 10);
      if (idx === activeIdx) {
        block.classList.add('active-layer');
      } else {
        block.classList.remove('active-layer');
      }
    });

    // Update active nav node and translate glowing telemetry packet dot
    navNodes.forEach(node => {
      const idx = parseInt(node.getAttribute('data-target-layer'), 10);
      if (idx === activeIdx) {
        node.classList.add('active');
        if (trackerDot) {
          const nodeTop = node.offsetTop;
          trackerDot.style.transform = `translateY(${nodeTop}px)`;
        }
      } else {
        node.classList.remove('active');
      }
    });
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}
