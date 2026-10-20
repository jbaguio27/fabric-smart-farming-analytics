import React from 'react';

export default function AuthorSection() {
  return (
    <section id="author" className="author-section">
      <div className="container">
        <div className="author-card">
          <div className="author-main-grid">
            <div className="author-portrait-wrap">
              <img src="/assets/images/author-portrait.jpg" alt="Joseph Baguio - Data Engineer" className="author-portrait-img" />
              <div className="author-status-badge">
                <span>Open for Engineering Roles</span>
              </div>
            </div>

            <div className="author-details">
              <h2 className="author-name">Joseph Baguio</h2>
              <div className="author-title-sub">Data Engineer • Microsoft Fabric, Streaming &amp; Lakehouse Systems</div>

              {/* Data Engineer Creed / Quote */}
              <div className="author-quote-box">
                <div className="author-quote-icon">“</div>
                <div className="author-quote-text">
                  I saw a real operational data problem in a farming environment where valuable data was trapped across silos, spreadsheets, and manual logs. The organization was not ready to modernize it, so I built this independent proof of concept to explore how I would solve that problem as a data engineer using Microsoft Fabric.
                </div>
                <div className="author-quote-meta">— Joseph Baguio, Data Engineer</div>
              </div>

              <p className="author-bio">
                Focused on building robust data platforms across Microsoft Fabric (Eventstream, KQL Eventhouse, Delta Lake, OneLake, Power BI Direct Lake), Databricks, Snowflake, and dbt. Committed to clean dimensional modeling, automated test coverage, and transparent engineering defensibility.
              </p>

              <div className="author-links">
                <a href="https://github.com/jbaguio27" target="_blank" rel="noopener" className="author-link-btn primary-btn">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                  </svg>
                  <span>GitHub Profile</span>
                </a>
                <a href="https://github.com/jbaguio27/fabric-smart-farming-analytics" target="_blank" rel="noopener" className="author-link-btn">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polyline points="16 18 22 12 16 6"></polyline>
                    <polyline points="8 6 2 12 8 18"></polyline>
                  </svg>
                  <span>Project Repository</span>
                </a>
                <a href="mailto:joseph.baguio@example.com" className="author-link-btn">
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                    <polyline points="22,6 12,13 2,6"></polyline>
                  </svg>
                  <span>Get In Touch</span>
                </a>
              </div>
            </div>
          </div>

          {/* Verified Credentials & Badges Showcase */}
          <div className="author-badges-showcase">
            <div className="badges-header">
              <div className="badges-heading">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm-2 16l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z"/>
                </svg>
                <span>Verified Technical Certifications & Credentials</span>
              </div>
              <div className="badges-hint"><svg className="inline-svg-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg> Click banner to inspect in fullscreen pan &amp; zoom</div>
            </div>

            <div className="badges-banner-container" data-lightbox-src="/assets/images/author-certifications-badges.png" data-lightbox-caption="Joseph Baguio - Verified Technical Certifications & Credentials across Microsoft Fabric/Azure, Databricks Data Engineer Associate, Snowflake Essentials, dbt Learn, Google Analytics, and DataCamp.">
              <img src="/assets/images/author-certifications-badges.png" alt="Joseph Baguio Technical Certifications and Badges" className="badges-banner-img" />
              <div className="badges-banner-overlay">
                <span className="badges-zoom-pill">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                    <line x1="11" y1="8" x2="11" y2="14"></line>
                    <line x1="8" y1="11" x2="14" y2="11"></line>
                  </svg>
                  Inspect Full Credentials
                </span>
              </div>
            </div>

            <div className="credentials-specs-grid">
              <div className="credential-item">
                <span className="credential-issuer">Microsoft</span>
                <span className="credential-name">Fabric &amp; AI Skills Fest 2026</span>
              </div>
              <div className="credential-item">
                <span className="credential-issuer">Microsoft</span>
                <span className="credential-name">Certified Associate &amp; Fundamentals</span>
              </div>
              <div className="credential-item">
                <span className="credential-issuer">Databricks</span>
                <span className="credential-name">Certified Data Engineer Associate</span>
              </div>
              <div className="credential-item">
                <span className="credential-issuer">Snowflake</span>
                <span className="credential-name">Hands On Essentials (Warehouse, Lake, Apps)</span>
              </div>
              <div className="credential-item">
                <span className="credential-issuer">dbt Labs</span>
                <span className="credential-name">dbt Learn Fundamentals</span>
              </div>
              <div className="credential-item">
                <span className="credential-issuer">Google</span>
                <span className="credential-name">Data Analytics Professional Certificate</span>
              </div>
              <div className="credential-item">
                <span className="credential-issuer">DataCamp</span>
                <span className="credential-name">Certified Data Engineer &amp; Python Associate</span>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  );
}
