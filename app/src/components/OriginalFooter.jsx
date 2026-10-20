import React from 'react';

export default function OriginalFooter() {
  return (
    <>
  {/* Site Footer */}
  <footer className="site-footer">
    <div className="container">
      <p className="footer-statement">
        Inspired by real-world operational farming challenges, modeled with synthetic telemetry, and built as an independent Microsoft Fabric proof of concept.
      </p>

      <div className="tech-stack-inline">
        <span>Python</span> •
        <span>Microsoft Fabric</span> •
        <span>Eventstream</span> •
        <span>Eventhouse (KQL)</span> •
        <span>OneLake</span> •
        <span>Delta Lake</span> •
        <span>Fabric Warehouse</span> •
        <span>Power BI Direct Lake</span> •
        <span>Activator</span> •
        <span>OpenTelemetry</span> •
        <span>GitHub Actions</span>
      </div>

      <p className="footer-copy">
        &copy; 2026 Joseph Baguio. Released under the MIT License.
      </p>
    </div>
  </footer>

  {/* Fullscreen Modal Lightbox with Pan & Zoom */}
  <div id="lightbox-modal" className="lightbox-modal" role="dialog" aria-modal="true">
    <div className="lightbox-top-bar">
      <div className="lightbox-controls">
        <button id="lightbox-zoom-in" className="lightbox-btn" title="Zoom In (+)">+</button>
        <button id="lightbox-zoom-out" className="lightbox-btn" title="Zoom Out (-)">−</button>
        <button id="lightbox-zoom-reset" className="lightbox-btn" title="Reset Zoom">⟲ Reset</button>
        <span id="lightbox-zoom-level" className="lightbox-zoom-tag">100%</span>
        <span className="lightbox-pan-hint"><svg className="inline-svg-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg> Drag to Pan • Scroll to Zoom</span>
      </div>
      <button id="lightbox-close" className="lightbox-close" aria-label="Close image preview">&times;</button>
    </div>
    <div className="lightbox-content-wrapper" id="lightbox-viewport">
      <div id="lightbox-loader" className="lightbox-spinner"></div>
      <img id="lightbox-img" className="lightbox-img" alt="Expanded inspection preview" />
      <div id="lightbox-caption" className="lightbox-caption"></div>
    </div>
  </div>
    </>
  );
}
