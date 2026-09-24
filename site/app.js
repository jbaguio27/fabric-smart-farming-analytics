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
  initDashboardWalkthrough();
  initBeforeAfterSlider();
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

  let isManualClick = false;
  let clickTimeout = null;

  function setActive(idx) {
    // 1. Highlight target layer block
    layerBlocks.forEach(block => {
      const bIdx = parseInt(block.getAttribute('data-layer-idx'), 10);
      if (bIdx === idx) {
        block.classList.add('active-layer');
      } else {
        block.classList.remove('active-layer');
      }
    });

    // 2. Activate nav node & animate tracker dot
    navNodes.forEach(node => {
      const nIdx = parseInt(node.getAttribute('data-target-layer'), 10);
      if (nIdx === idx) {
        node.classList.add('active');
        if (trackerDot) {
          const nodeTop = node.offsetTop;
          const nodeHeight = node.offsetHeight;
          const dotTop = nodeTop + (nodeHeight / 2) - 5;
          trackerDot.style.transform = `translateY(${dotTop}px)`;
        }
      } else {
        node.classList.remove('active');
      }
    });
  }

  // Click on pipeline choice
  navNodes.forEach(node => {
    node.addEventListener('click', (e) => {
      e.preventDefault();
      const idx = parseInt(node.getAttribute('data-target-layer'), 10);
      const targetBlock = document.querySelector(`.layer-block[data-layer-idx="${idx}"]`);

      if (targetBlock) {
        isManualClick = true;
        clearTimeout(clickTimeout);
        setActive(idx);

        // Scroll target layer into view just below sticky navbar
        const headerOffset = 140;
        const targetTop = targetBlock.getBoundingClientRect().top + window.scrollY - headerOffset;

        window.scrollTo({
          top: targetTop,
          behavior: 'smooth'
        });

        // Release scroll lock after smooth scroll animation completes
        clickTimeout = setTimeout(() => {
          isManualClick = false;
        }, 850);
      }
    });
  });

  // Dynamic onScroll spy using top threshold
  const onScroll = () => {
    if (isManualClick) return;

    // Viewport threshold just below sticky header
    const threshold = 180;
    let activeIdx = 1;

    layerBlocks.forEach(block => {
      const rect = block.getBoundingClientRect();
      const bIdx = parseInt(block.getAttribute('data-layer-idx'), 10);

      // As user scrolls down, each layer whose top has crossed the threshold becomes active
      if (rect.top <= threshold) {
        activeIdx = bIdx;
      }
    });

    setActive(activeIdx);
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  
  // Set initial Layer 1 on page load
  setTimeout(() => {
    setActive(1);
  }, 100);
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

      // Touch toggle for mobile
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

    // Update Buttons
    tabBtns.forEach(b => {
      b.classList.toggle('active', b.getAttribute('data-view') === viewKey);
    });

    // Fade transition on image
    displayImg.style.opacity = '0';
    setTimeout(() => {
      displayImg.src = data.img;
      displayImg.alt = data.title;
      if (urlDisplay) urlDisplay.textContent = data.url;
      if (modeBadge) modeBadge.textContent = data.mode;
      if (captionText) captionText.textContent = data.caption;
      displayImg.style.opacity = '1';
      renderHotspots(data.hotspots);
    }, 200);
  }

  // Bind click listeners on view tabs
  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const viewKey = btn.getAttribute('data-view');
      setView(viewKey);
    });
  });

  // Expand in Fullscreen Lightbox
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
        modalImg.src = data.img;
        modalCaption.textContent = data.caption;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  }

  // Dismiss open tooltips when clicking anywhere in viewport
  document.addEventListener('click', () => {
    document.querySelectorAll('.hotspot-item').forEach(el => el.classList.remove('active'));
  });

  // Initial load
  setView('executive-ops');
}

/**
 * Interactive Before & After Telemetry Transformation Slider
 */
function initBeforeAfterSlider() {
  const container = document.getElementById('before-after-widget');
  const beforeLayer = document.getElementById('slider-before-layer');
  const divider = document.getElementById('slider-divider');

  if (!container || !beforeLayer || !divider) return;

  let isDragging = false;

  function updateSlider(clientX) {
    const rect = container.getBoundingClientRect();
    const offsetX = clientX - rect.left;
    let percentage = (offsetX / rect.width) * 100;

    // Clamp between 5% and 95%
    percentage = Math.max(5, Math.min(95, percentage));

    beforeLayer.style.width = `${percentage}%`;
    divider.style.left = `${percentage}%`;
  }

  // Mouse Events
  divider.addEventListener('mousedown', (e) => {
    isDragging = true;
    e.preventDefault();
  });

  container.addEventListener('mousedown', (e) => {
    isDragging = true;
    updateSlider(e.clientX);
  });

  window.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    updateSlider(e.clientX);
  });

  window.addEventListener('mouseup', () => {
    isDragging = false;
  });

  // Touch Events
  divider.addEventListener('touchstart', (e) => {
    isDragging = true;
  }, { passive: true });

  container.addEventListener('touchstart', (e) => {
    isDragging = true;
    if (e.touches[0]) updateSlider(e.touches[0].clientX);
  }, { passive: true });

  window.addEventListener('touchmove', (e) => {
    if (!isDragging || !e.touches[0]) return;
    updateSlider(e.touches[0].clientX);
  }, { passive: true });

  window.addEventListener('touchend', () => {
    isDragging = false;
  });
}
