/**
 * HydroGrow: Microsoft Fabric Smart Farming Platform
 * Client-side Controller & Interactive Handlers
 * 
 * Upgraded with Apple Design Fluid Interface Principles:
 * - Direct Manipulation (Pointer Events + setPointerCapture)
 * - Progressive Boundary Rubber-Banding
 * - Momentum Projection & Inertial Velocity Handoff
 * - Spatially Anchored Origins for Modals & Tooltips
 * - Latency Elimination & Full Interruptibility
 * - Accessibility (prefers-reduced-motion / reduced-transparency)
 */

document.addEventListener('DOMContentLoaded', () => {
  initAppleTouchFeedback();
  initLightbox();
  initTabs();
  initCodeCopy();
  initScrollSpy();
  initMobileNav();
  initCounters();
  // Swiper replaced with accessible failure matrix
  initScrolltellingPipeline();
  initDashboardWalkthrough();
  initBeforeAfterSlider();
  initLiveTelemetryTicker();
  initKqlDrawers();
  initSliderPresets();
  initLatencyInstrumentHover();
  initHeroFilterPills();
});

/**
 * Apple Design Principle 1: Response - Kill Latency
 * Instant tactile feedback on pointerdown
 */
function initAppleTouchFeedback() {
  const interactiveSelector = 'button, .btn, .tab-btn, .walkthrough-tab-btn, .filter-pill, .photo-card, [data-lightbox-src]';
  document.addEventListener('pointerdown', (e) => {
    const target = e.target.closest(interactiveSelector);
    if (!target) return;
    target.classList.add('apple-pressed');

    const clearPress = () => {
      target.classList.remove('apple-pressed');
      window.removeEventListener('pointerup', clearPress);
      window.removeEventListener('pointercancel', clearPress);
    };

    window.addEventListener('pointerup', clearPress, { once: true });
    window.addEventListener('pointercancel', clearPress, { once: true });
  }, { passive: true });
}

/**
 * Apple Design Principle 9: Progressive Rubber-Banding
 * Soft boundaries that resist progressively instead of stopping hard
 */
function rubberband(overshoot, dimension, constant = 0.55) {
  return (overshoot * dimension * constant) / (dimension + constant * Math.abs(overshoot));
}

/**
 * Apple Design Principle 6: Momentum Projection
 * Projects resting position based on release velocity
 */
function projectMomentum(initialVelocity, decelerationRate = 0.998) {
  return (initialVelocity / 1000) * decelerationRate / (1 - decelerationRate);
}

/**
 * Fullscreen Lightbox Modal Controller with Anchored Spatial Origins & Pan
 * Apple Principle 7: Spatial Consistency - Expand from triggered card & collapse back
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
  let lastMoveTime = 0;
  let lastX = 0;
  let lastY = 0;
  let velocityX = 0;
  let velocityY = 0;
  let panAnimFrame = null;

  function updateTransform() {
    modalImg.style.transform = `translate(${posX}px, ${posY}px) scale(${scale})`;
    if (zoomLevelTag) {
      zoomLevelTag.textContent = `${Math.round(scale * 100)}%`;
    }
    modalImg.style.cursor = scale > 1 ? (isDragging ? 'grabbing' : 'grab') : 'default';
  }

  function resetZoom() {
    cancelAnimationFrame(panAnimFrame);
    scale = 1;
    posX = 0;
    posY = 0;
    velocityX = 0;
    velocityY = 0;
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

  if (zoomInBtn) zoomInBtn.addEventListener('click', (e) => { e.stopPropagation(); zoomIn(); });
  if (zoomOutBtn) zoomOutBtn.addEventListener('click', (e) => { e.stopPropagation(); zoomOut(); });
  if (zoomResetBtn) zoomResetBtn.addEventListener('click', (e) => { e.stopPropagation(); resetZoom(); });

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

  // Direct Manipulation Pan with Pointer Events & Momentum Projection
  modalImg.addEventListener('pointerdown', (e) => {
    if (scale <= 1) return;
    isDragging = true;
    cancelAnimationFrame(panAnimFrame);
    modalImg.setPointerCapture(e.pointerId);

    startX = e.clientX - posX;
    startY = e.clientY - posY;
    lastX = e.clientX;
    lastY = e.clientY;
    lastMoveTime = performance.now();
    velocityX = 0;
    velocityY = 0;
    updateTransform();
    e.preventDefault();
  });

  modalImg.addEventListener('pointermove', (e) => {
    if (!isDragging) return;
    const now = performance.now();
    const dt = Math.max(1, now - lastMoveTime);

    velocityX = (e.clientX - lastX) / dt;
    velocityY = (e.clientY - lastY) / dt;

    lastX = e.clientX;
    lastY = e.clientY;
    lastMoveTime = now;

    posX = e.clientX - startX;
    posY = e.clientY - startY;
    updateTransform();
  });

  const handlePointerEnd = () => {
    if (!isDragging) return;
    isDragging = false;
    updateTransform();

    const speed = Math.hypot(velocityX, velocityY);
    if (speed > 0.25) {
      const glideStartTime = performance.now();
      const startPosX = posX;
      const startPosY = posY;
      const projX = projectMomentum(velocityX * 1000, 0.995);
      const projY = projectMomentum(velocityY * 1000, 0.995);

      function glideStep(now) {
        const elapsed = now - glideStartTime;
        const duration = 500;
        const progress = Math.min(1, elapsed / duration);
        const easeOut = 1 - Math.pow(1 - progress, 3);

        posX = startPosX + projX * easeOut;
        posY = startPosY + projY * easeOut;
        updateTransform();

        if (progress < 1) {
          panAnimFrame = requestAnimationFrame(glideStep);
        }
      }

      panAnimFrame = requestAnimationFrame(glideStep);
    }
  };

  modalImg.addEventListener('pointerup', handlePointerEnd);
  modalImg.addEventListener('pointercancel', handlePointerEnd);

  // Spatially Anchored Trigger: Expand from trigger's viewport coordinates
  const triggerElements = document.querySelectorAll('[data-lightbox-src]');
  triggerElements.forEach(el => {
    el.addEventListener('click', () => {
      const src = el.getAttribute('data-lightbox-src');
      const caption = el.getAttribute('data-lightbox-caption') || el.querySelector('.gallery-item-title')?.textContent || '';
      
      const rect = el.getBoundingClientRect();
      const originX = rect.left + rect.width / 2;
      const originY = rect.top + rect.height / 2;
      modal.style.setProperty('--origin-x', `${originX}px`);
      modal.style.setProperty('--origin-y', `${originY}px`);

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

  const closeModal = () => {
    modal.classList.remove('active');
    setTimeout(() => {
      modalImg.src = '';
      modalCaption.textContent = '';
      resetZoom();
    }, 280);
    document.body.style.overflow = '';
  };

  closeBtn.addEventListener('click', closeModal);

  modal.addEventListener('click', (e) => {
    if (e.target === modal || e.target === viewport) {
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

      tabBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

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
        btn.textContent = '✓ Copied';
        btn.classList.add('copied');

        setTimeout(() => {
          btn.textContent = originalText;
          btn.classList.remove('copied');
        }, 2000);
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
    const scrollPos = window.scrollY + 140;

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
  onScroll();
}

/**
 * Mobile Navigation Toggle with Sheet Backdrop & Spring Entrance
 */
function initMobileNav() {
  const toggleBtn = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  if (!toggleBtn || !navLinks) return;

  function toggleMenu() {
    const isOpen = navLinks.classList.contains('mobile-open');
    navLinks.classList.toggle('mobile-open');
    toggleBtn.setAttribute('aria-expanded', !isOpen);
    toggleBtn.classList.toggle('active', !isOpen);
    document.body.classList.toggle('nav-sheet-open', !isOpen);
  }

  toggleBtn.addEventListener('click', toggleMenu);

  navLinks.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
      navLinks.classList.remove('mobile-open');
      toggleBtn.setAttribute('aria-expanded', 'false');
      toggleBtn.classList.remove('active');
      document.body.classList.remove('nav-sheet-open');
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && navLinks.classList.contains('mobile-open')) {
      toggleMenu();
    }
  });
}

/**
 * Animated Metric Number Counter Ticker (Respects Reduced Motion)
 */
function initCounters() {
  const counterElements = document.querySelectorAll('[data-counter]');
  if (!counterElements.length || !('IntersectionObserver' in window)) return;

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        if (prefersReducedMotion) {
          const el = entry.target;
          const target = parseFloat(el.getAttribute('data-counter'));
          const prefix = el.getAttribute('data-prefix') || '';
          const suffix = el.getAttribute('data-suffix') || '';
          const decimals = parseInt(el.getAttribute('data-decimals') || '0', 10);
          el.textContent = `${prefix}${target.toFixed(decimals)}${suffix}`;
        } else {
          animateCounter(entry.target);
        }
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
  const duration = 1100;
  const startTime = performance.now();

  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
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

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  new Swiper('.problem-swiper', {
    effect: prefersReducedMotion ? 'slide' : 'coverflow',
    grabCursor: true,
    centeredSlides: true,
    slidesPerView: 'auto',
    initialSlide: 0,
    speed: prefersReducedMotion ? 200 : 400,
    coverflowEffect: {
      rotate: prefersReducedMotion ? 0 : 20,
      stretch: 0,
      depth: prefersReducedMotion ? 0 : 120,
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
 * Scrolltelling Data Pipeline Visualization Controller
 * Apple Principle 3: Fully Interruptible, Zero Delay Lockouts
 */
function initScrolltellingPipeline() {
  const layerBlocks = document.querySelectorAll('.layer-block[data-layer-idx]');
  const navNodes = document.querySelectorAll('.pipeline-nav-node[data-target-layer]');
  const trackerDot = document.getElementById('pipeline-packet-dot');

  if (!layerBlocks.length || !navNodes.length) return;

  let isManualScroll = false;

  function setActive(idx) {
    layerBlocks.forEach(block => {
      const bIdx = parseInt(block.getAttribute('data-layer-idx'), 10);
      block.classList.toggle('active-layer', bIdx === idx);
    });

    navNodes.forEach(node => {
      const nIdx = parseInt(node.getAttribute('data-target-layer'), 10);
      const isMatch = nIdx === idx;
      node.classList.toggle('active', isMatch);
      if (isMatch && trackerDot) {
        const nodeTop = node.offsetTop;
        const nodeHeight = node.offsetHeight;
        const dotTop = nodeTop + (nodeHeight / 2) - 5;
        trackerDot.style.transform = `translateY(${dotTop}px)`;
      }
    });
  }

  navNodes.forEach(node => {
    node.addEventListener('click', (e) => {
      e.preventDefault();
      const idx = parseInt(node.getAttribute('data-target-layer'), 10);
      const targetBlock = document.querySelector(`.layer-block[data-layer-idx="${idx}"]`);

      if (targetBlock) {
        setActive(idx);
        const headerOffset = 130;
        const targetTop = targetBlock.getBoundingClientRect().top + window.scrollY - headerOffset;

        isManualScroll = true;
        window.scrollTo({
          top: targetTop,
          behavior: 'smooth'
        });

        const onSettled = () => {
          isManualScroll = false;
          window.removeEventListener('wheel', onSettled);
          window.removeEventListener('touchmove', onSettled);
        };
        window.addEventListener('wheel', onSettled, { once: true, passive: true });
        window.addEventListener('touchmove', onSettled, { once: true, passive: true });
        setTimeout(() => { isManualScroll = false; }, 600);
      }
    });
  });

  const onScroll = () => {
    if (isManualScroll) return;
    const threshold = 180;
    let activeIdx = 1;

    layerBlocks.forEach(block => {
      const rect = block.getBoundingClientRect();
      const bIdx = parseInt(block.getAttribute('data-layer-idx'), 10);
      if (rect.top <= threshold) {
        activeIdx = bIdx;
      }
    });

    setActive(activeIdx);
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  setTimeout(() => setActive(1), 50);
}

/**
 * Interactive Dashboard Walkthrough Theater & Hotspot Tooltips
 */
const WALKTHROUGH_DATA = {
  'executive-ops': {
    title: 'Executive Operations Overview',
    url: 'https://app.fabric.microsoft.com/groups/smart-farming/reports/executive-operations',
    mode: '● DIRECT LAKE (VERTIPAQ)',
    img: 'assets/reports/page_1_executive_operations.png',
    caption: 'Executive Operations Control Tower: Real-time nationwide facility health indices, Grade-A harvest yield realization, wholesale revenue (₱137.83M), and regional production.',
    hotspots: [
      {
        top: '14%', left: '38%',
        tag: 'BI ARCHITECTURE',
        title: 'Single-Row KPI Tracking',
        desc: 'High-level facility health (92.94% - 93.13%) and power draw pre-aggregated via Gold Kimball facts and KQL materialized views to establish instant situational awareness.',
        align: 'tooltip-bottom'
      },
      {
        top: '36%', left: '9%',
        tag: 'DATA DISCOVERY',
        title: 'Native Multi-Select Filter Sidebar',
        desc: 'Dedicated vertical pane allows operators to slice by facility region, growing room, timeframe, or anomaly type without Cartesian product query lag.',
        align: 'tooltip-right'
      },
      {
        top: '58%', left: '64%',
        tag: 'DIRECT LAKE MODE',
        title: 'Direct Lake Storage Engine',
        desc: 'Power BI queries OneLake Delta Parquet directly using VertiPaq memory compression—delivering sub-second rendering without scheduled import refreshes.',
        align: 'tooltip-left'
      }
    ]
  },
  'streaming-sla': {
    title: 'Streaming Ingress SLA & Governance',
    url: 'https://app.fabric.microsoft.com/groups/smart-farming/kql-dashboards/streaming-sla-governance',
    mode: '● STREAMING (3.0s KQL REFRESH)',
    img: 'assets/dashboards/kql_dashboard_streaming_sla_governance.png',
    caption: 'Streaming Ingestion SLA & Real-Time Telemetry Observability: Per-stream ingestion lag tracking (SLA < 3.0s), data quality scorecard, DLQ quarantine logs, and ingress velocity.',
    hotspots: [
      {
        top: '18%', left: '32%',
        tag: 'REAL-TIME SLA',
        title: 'Sub-3.0s Ingestion SLA Tracking',
        desc: 'Tracks real-time telemetry lag percentiles (p50: 1.70s, max: 5.38s), proving high-throughput streaming arrival far exceeds the 15-second SLA target.',
        align: 'tooltip-bottom'
      },
      {
        top: '48%', left: '78%',
        tag: 'DATA QUALITY',
        title: 'Dead-Letter Queue Quarantine',
        desc: 'Eventstream routes schema violations, missing keys, and electrical jitter to a dedicated DLQ sink before reaching downstream Silver tables.',
        align: 'tooltip-left'
      },
      {
        top: '74%', left: '42%',
        tag: 'STREAM PROCESSING',
        title: 'Continuous Multi-Stream Velocity',
        desc: 'Monitors 6 continuous telemetry streams across 8 vertical farming facilities with sub-second KQL window aggregations.',
        align: 'tooltip-top'
      }
    ]
  },
  'microclimates': {
    title: 'Environmental Microclimates',
    url: 'https://app.fabric.microsoft.com/groups/smart-farming/reports/environmental-microclimates',
    mode: '● DIRECT LAKE (VERTIPAQ)',
    img: 'assets/reports/page_2_environmental_microclimates.png',
    caption: 'Environmental Telemetry & Crop Biological Health: Microclimate stability across 80 growing zones, canopy VPD (1.64 kPa), DLI photoperiods (16.88 mol/m²/d), and biomass growth.',
    hotspots: [
      {
        top: '22%', left: '45%',
        tag: 'CROP BIOLOGY',
        title: 'Canopy Vapor Pressure Deficit (VPD)',
        desc: 'Calculates live transpiration pressure differential (1.64 kPa) to prevent stomatal closure and vegetative tip burn on high-value greens.',
        align: 'tooltip-bottom'
      },
      {
        top: '52%', left: '76%',
        tag: 'LIGHTING TELEMETRY',
        title: 'Daily Light Integral (DLI) Tracking',
        desc: 'Correlates lighting fixture power draw with PAR sensor telemetry to ensure crops reach optimal photosynthetic photon flux daily.',
        align: 'tooltip-left'
      },
      {
        top: '78%', left: '30%',
        tag: 'ANOMALY DETECTION',
        title: 'Zone Microclimate Variance',
        desc: 'Cross-zone statistical variance triggers automated HVAC blower adjustments before biological crop damage occurs.',
        align: 'tooltip-top'
      }
    ]
  },
  'pipeline-observability': {
    title: 'DataOps Observability & Pipeline Traces',
    url: 'https://app.fabric.microsoft.com/groups/smart-farming/kql-dashboards/dataops-observability',
    mode: '● DATAOPS OBSERVE (OPENTELEMETRY)',
    img: 'assets/dashboards/kql_dashboard_pipeline_observability.png',
    caption: 'DataOps Observability & Pipeline Traces: 100.0% Pipeline Run Success Rate, Medallion Pipeline Trace & Execution History, 2.84 min End-to-End Batch Duration, Data Quality Gate Compliance.',
    hotspots: [
      {
        top: '16%', left: '22%',
        tag: 'RELIABILITY',
        title: '100.0% Pipeline Run Success Rate',
        desc: 'Continuous verification of Medallion orchestration runs, tracking end-to-end execution reliability across Bronze, Silver, and Gold stages.',
        align: 'tooltip-bottom'
      },
      {
        top: '28%', left: '78%',
        tag: 'SLA BENCHMARK',
        title: '2.84 min End-to-End Batch Duration',
        desc: 'Measures full delta sync across Bronze shortcuts, Silver deduplication/PII masking, and Gold Star Schema aggregation.',
        align: 'tooltip-left'
      },
      {
        top: '68%', left: '50%',
        tag: 'OPENTELEMETRY',
        title: 'Span Propagation & Execution Logging',
        desc: 'Every Spark task and master pipeline run instruments OpenTelemetry spans stored in fact_dataops_pipeline_log for full operational auditability.',
        align: 'tooltip-top'
      }
    ]
  }
};

function initDashboardWalkthrough() {
  const tabBtns = document.querySelectorAll('.walkthrough-tab-btn');
  const displayImg = document.getElementById('theater-img');
  const urlDisplay = document.getElementById('theater-url-display');
  const modeBadge = document.getElementById('theater-mode-badge');
  const captionText = document.getElementById('theater-caption-text');
  const hotspotsContainer = document.getElementById('theater-hotspots');
  const expandBtn = document.getElementById('theater-expand-lightbox');

  if (!tabBtns.length || !displayImg || !hotspotsContainer) return;

  function renderHotspots(hotspotList) {
    hotspotsContainer.innerHTML = '';
    hotspotList.forEach(hs => {
      const item = document.createElement('div');
      item.className = 'hotspot-item';
      item.style.top = hs.top;
      item.style.left = hs.left;

      item.innerHTML = `
        <div class="hotspot-dot">
          <span class="hotspot-ring"></span>
          <span class="hotspot-core"></span>
        </div>
        <div class="hotspot-tooltip ${hs.align || 'tooltip-bottom'}">
          <div class="tooltip-header">
            <span class="tooltip-tag">${hs.tag}</span>
            <span class="tooltip-title">${hs.title}</span>
          </div>
          <p class="tooltip-desc">${hs.desc}</p>
        </div>
      `;

      item.addEventListener('click', (e) => {
        e.stopPropagation();
        const wasActive = item.classList.contains('active');
        document.querySelectorAll('.hotspot-item').forEach(el => el.classList.remove('active'));
        if (!wasActive) item.classList.add('active');
      });

      hotspotsContainer.appendChild(item);
    });
  }

  function setView(viewKey) {
    const data = WALKTHROUGH_DATA[viewKey];
    if (!data) return;

    tabBtns.forEach(b => {
      b.classList.toggle('active', b.getAttribute('data-view') === viewKey);
    });

    displayImg.src = data.img;
    displayImg.alt = data.title;
    if (urlDisplay) urlDisplay.textContent = data.url;
    if (modeBadge) modeBadge.textContent = data.mode;
    if (captionText) captionText.textContent = data.caption;
    renderHotspots(data.hotspots);
  }

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const viewKey = btn.getAttribute('data-view');
      setView(viewKey);
    });
  });

  if (expandBtn) {
    expandBtn.addEventListener('click', () => {
      const activeBtn = document.querySelector('.walkthrough-tab-btn.active');
      const viewKey = activeBtn ? activeBtn.getAttribute('data-view') : 'executive-ops';
      const data = WALKTHROUGH_DATA[viewKey];
      if (!data) return;

      const modal = document.getElementById('lightbox-modal');
      const modalImg = document.getElementById('lightbox-img');
      const modalCaption = document.getElementById('lightbox-caption');
      if (modal && modalImg && modalCaption) {
        const rect = expandBtn.getBoundingClientRect();
        modal.style.setProperty('--origin-x', `${rect.left + rect.width / 2}px`);
        modal.style.setProperty('--origin-y', `${rect.top + rect.height / 2}px`);

        modalImg.src = data.img;
        modalCaption.textContent = data.caption;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  }

  document.addEventListener('click', () => {
    document.querySelectorAll('.hotspot-item').forEach(el => el.classList.remove('active'));
  });

  setView('executive-ops');
}

/**
 * Interactive Before & After Telemetry Transformation Slider
 * Apple Fluid Interface Upgrades:
 * - Direct Manipulation (Pointer Events with setPointerCapture)
 * - Progressive Boundary Rubber-Banding
 * - Release Velocity Tracking & Momentum Handoff
 */
function initBeforeAfterSlider() {
  const container = document.getElementById('before-after-widget');
  const beforeLayer = document.getElementById('slider-before-layer');
  const divider = document.getElementById('slider-divider');

  if (!container || !beforeLayer || !divider) return;

  let isDragging = false;
  let currentPercentage = 50;
  let history = [];
  let momentumAnimFrame = null;

  function applyPercentage(pct, withSpring = false) {
    currentPercentage = pct;
    beforeLayer.style.width = `${pct}%`;
    divider.style.left = `${pct}%`;
    if (withSpring) {
      beforeLayer.style.transition = 'width 0.4s cubic-bezier(0.16, 1, 0.3, 1)';
      divider.style.transition = 'left 0.4s cubic-bezier(0.16, 1, 0.3, 1)';
    } else {
      beforeLayer.style.transition = 'none';
      divider.style.transition = 'none';
    }
  }

  function handlePointerMove(clientX) {
    const rect = container.getBoundingClientRect();
    const rawX = clientX - rect.left;
    let rawPct = (rawX / rect.width) * 100;

    let finalPct = rawPct;
    if (rawPct < 5) {
      const overshoot = 5 - rawPct;
      finalPct = 5 - rubberband(overshoot, 100, 0.4);
    } else if (rawPct > 95) {
      const overshoot = rawPct - 95;
      finalPct = 95 + rubberband(overshoot, 100, 0.4);
    }

    applyPercentage(finalPct, false);

    const now = performance.now();
    history.push({ x: finalPct, time: now });
    if (history.length > 5) history.shift();
  }

  function handlePointerDown(e) {
    isDragging = true;
    cancelAnimationFrame(momentumAnimFrame);
    history = [{ x: currentPercentage, time: performance.now() }];
    divider.setPointerCapture(e.pointerId);
    container.classList.add('is-dragging');
    handlePointerMove(e.clientX);
    e.preventDefault();
  }

  function handlePointerUp(e) {
    if (!isDragging) return;
    isDragging = false;
    container.classList.remove('is-dragging');

    const now = performance.now();
    let velocity = 0;
    if (history.length >= 2) {
      const recent = history[history.length - 1];
      const prev = history[0];
      const dt = Math.max(1, recent.time - prev.time);
      velocity = ((recent.x - prev.x) / dt) * 1000;
    }

    if (Math.abs(velocity) > 150) {
      const projectedDelta = projectMomentum(velocity, 0.992) * 0.12;
      let target = currentPercentage + projectedDelta;
      target = Math.max(5, Math.min(95, target));

      const startTime = performance.now();
      const startPct = currentPercentage;
      const totalDelta = target - startPct;

      function momentumStep(t) {
        const progress = Math.min(1, (t - startTime) / 450);
        const ease = 1 - Math.pow(1 - progress, 3);
        const current = startPct + totalDelta * ease;
        applyPercentage(current, false);

        if (progress < 1) {
          momentumAnimFrame = requestAnimationFrame(momentumStep);
        } else {
          applyPercentage(target, true);
        }
      }

      momentumAnimFrame = requestAnimationFrame(momentumStep);
    } else {
      if (currentPercentage < 5) {
        applyPercentage(5, true);
      } else if (currentPercentage > 95) {
        applyPercentage(95, true);
      }
    }
  }

  divider.addEventListener('pointerdown', handlePointerDown);
  container.addEventListener('pointerdown', handlePointerDown);

  window.addEventListener('pointermove', (e) => {
    if (!isDragging) return;
    handlePointerMove(e.clientX);
  });

  window.addEventListener('pointerup', handlePointerUp);
  window.addEventListener('pointercancel', handlePointerUp);

  applyPercentage(50, false);
}

/**
 * Live Simulated Edge Telemetry HUD Controller
 * Demonstrates real-time streaming velocity and IoT microclimate stability
 */
function initLiveTelemetryTicker() {
  const clockEl = document.getElementById('hud-clock');
  const tempEl = document.getElementById('hud-temp');
  const humEl = document.getElementById('hud-humidity');
  const vpdEl = document.getElementById('hud-vpd');
  const phEl = document.getElementById('hud-ph');
  const ecEl = document.getElementById('hud-ec');
  const rateEl = document.getElementById('hud-rate');

  if (!clockEl || !tempEl) return;

  function updateClock() {
    const now = new Date();
    clockEl.textContent = now.toTimeString().split(' ')[0] + ' UTC';
  }
  updateClock();
  setInterval(updateClock, 1000);

  // Periodic realistic sensor jitter
  setInterval(() => {
    // Temp: 19.2 to 19.6
    const temp = (19.4 + (Math.random() * 0.4 - 0.2)).toFixed(1);
    tempEl.innerHTML = `${temp}<span class="hud-metric-unit">°C</span>`;

    // Humidity: 85.8 to 86.6
    const hum = (86.2 + (Math.random() * 0.8 - 0.4)).toFixed(1);
    humEl.innerHTML = `${hum}<span class="hud-metric-unit">%</span>`;

    // VPD: 1.10 to 1.14
    const vpd = (1.12 + (Math.random() * 0.04 - 0.02)).toFixed(2);
    vpdEl.innerHTML = `${vpd}<span class="hud-metric-unit">kPa</span>`;

    // pH: 6.22 to 6.26
    const ph = (6.24 + (Math.random() * 0.04 - 0.02)).toFixed(2);
    phEl.innerHTML = `${ph}<span class="hud-metric-unit">pH</span>`;

    // EC: 1.82 to 1.86
    const ec = (1.84 + (Math.random() * 0.04 - 0.02)).toFixed(2);
    ecEl.innerHTML = `${ec}<span class="hud-metric-unit">mS/cm</span>`;

    // Rate: 1,220 to 1,260
    const rate = Math.floor(1240 + (Math.random() * 40 - 20));
    rateEl.innerHTML = `${rate.toLocaleString()}<span class="hud-metric-unit">ev/s</span>`;
  }, 3500);
}

/**
 * KQL Detection Query Accordions in Failure Matrix
 */
function initKqlDrawers() {
  const btns = document.querySelectorAll('.kql-drawer-btn');
  btns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = btn.getAttribute('data-target-kql');
      const drawer = document.getElementById(targetId);
      if (!drawer) return;

      const isOpen = drawer.classList.contains('is-open');
      if (isOpen) {
        drawer.classList.remove('is-open');
        btn.classList.remove('is-active');
        btn.setAttribute('aria-expanded', 'false');
      } else {
        drawer.classList.add('is-open');
        btn.classList.add('is-active');
        btn.setAttribute('aria-expanded', 'true');
      }
    });
  });
}

/**
 * Interactive Before & After Slider Preset Toolbar
 */
function initSliderPresets() {
  const presetBtns = document.querySelectorAll('.slider-preset-btn');
  const divider = document.querySelector('.slider-divider');
  const container = document.getElementById('before-after-widget');
  const beforeLayer = document.getElementById('slider-before-layer');
  if (!presetBtns.length || !divider || !beforeLayer || !container) return;

  presetBtns.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      presetBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const split = parseFloat(btn.getAttribute('data-split'));
      // Smoothly animate divider to target split using spring
      const startSplit = parseFloat(divider.style.left) || 50;
      const targetSplit = split;
      const startTime = performance.now();
      const duration = 400; // ms

      function step(t) {
        const progress = Math.min(1, (t - startTime) / duration);
        // Custom Apple-style ease-out spring
        const ease = 1 - Math.pow(1 - progress, 3);
        const current = startSplit + (targetSplit - startSplit) * ease;

        divider.style.left = `${current}%`;
        beforeLayer.style.clipPath = `polygon(0 0, ${current}% 0, ${current}% 100%, 0 100%)`;

        if (progress < 1) {
          requestAnimationFrame(step);
        }
      }
      requestAnimationFrame(step);
    });
  });
}

/**
 * Latency Instrument Interactive Tooltip & Point Inspection
 */
function initLatencyInstrumentHover() {
  const cols = document.querySelectorAll('.instrument-data-table .data-col');
  const pts = {
    'p50': document.getElementById('pt-p50'),
    'p95': document.getElementById('pt-p95'),
    'pmax': document.getElementById('pt-pmax')
  };

  cols.forEach(col => {
    const key = col.getAttribute('data-percentile');
    const pt = pts[key];

    col.addEventListener('mouseenter', () => {
      cols.forEach(c => c.classList.remove('is-active'));
      col.classList.add('is-active');
      if (pt) pt.classList.add('highlighted');
    });

    col.addEventListener('mouseleave', () => {
      col.classList.remove('is-active');
      if (pt) pt.classList.remove('highlighted');
    });
  });

  Object.entries(pts).forEach(([key, pt]) => {
    if (!pt) return;
    pt.addEventListener('mouseenter', () => {
      const col = document.querySelector(`.instrument-data-table .data-col[data-percentile="${key}"]`);
      if (col) col.classList.add('is-active');
      pt.classList.add('highlighted');
    });
    pt.addEventListener('mouseleave', () => {
      const col = document.querySelector(`.instrument-data-table .data-col[data-percentile="${key}"]`);
      if (col) col.classList.remove('is-active');
      pt.classList.remove('highlighted');
    });
  });
}

/**
 * Hero Architecture Filter Pills Interactive Quick-Jump
 */
function initHeroFilterPills() {
  const pills = document.querySelectorAll('.hero-filter-pills .filter-pill');
  const railNodes = document.querySelectorAll('.pipeline-nav-node');

  pills.forEach(pill => {
    pill.addEventListener('click', (e) => {
      e.preventDefault();
      pills.forEach(p => p.classList.remove('active'));
      pill.classList.add('active');

      const targetLayer = pill.getAttribute('data-target-layer');
      const targetBlock = document.querySelector(`.layer-block[data-layer-idx="${targetLayer}"]`);
      const targetNode = document.querySelector(`.pipeline-nav-node[data-target-layer="${targetLayer}"]`);

      if (targetBlock) {
        targetBlock.scrollIntoView({ behavior: 'smooth', block: 'center' });
        // Pulse layer border to confirm destination
        targetBlock.classList.add('active-layer');
      }

      if (targetNode && railNodes.length) {
        railNodes.forEach(n => n.classList.remove('active'));
        targetNode.classList.add('active');
      }
    });
  });
}
