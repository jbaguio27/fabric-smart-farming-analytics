import React from 'react';

export default function ResultsSection() {
  return (
    <section id="results" className="metrics-section section py-20 sm:py-24 lg:py-28">
      <div className="results-expanded-container w-full max-w-7xl xl:max-w-[1440px] 2xl:max-w-[1520px] mx-auto px-6 sm:px-8 lg:px-12">
        <div className="metrics-header mb-12 sm:mb-16">
          <h2 className="section-title text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight">Project at a Glance</h2>
          <p className="section-lead max-w-3xl mt-3 text-base sm:text-lg leading-relaxed">
            Every metric below represents verified measurements from automated test suites, simulated facility configurations, and documented capacity models in the repository.
          </p>
        </div>

        {/* Platform Benchmarks & Architectural Specifications (Anti-Slop Technical Layout) */}
        <div className="benchmarks-overview">

          {/* 4 Core Technical Indicators */}
          <div className="benchmarks-metrics-strip">
            
            <div className="benchmark-metric-card">
              <div className="metric-eyebrow">Ingestion Latency (p50)</div>
              <div className="metric-value-wrap">
                <span className="metric-num" data-counter="1.70" data-suffix="s" data-decimals="2">1.70s</span>
                <span className="metric-badge-sub">Target &lt; 15.0s</span>
              </div>
              <div className="metric-label">Observed max 5.38s into Fabric Eventstream &amp; KQL DB</div>
            </div>

            <div className="benchmark-metric-card">
              <div className="metric-eyebrow">Automated Test Suite</div>
              <div className="metric-value-wrap">
                <span className="metric-num" data-counter="53" data-suffix=" / 53">53 / 53</span>
                <span className="metric-badge-sub status-green">100% Pass</span>
              </div>
              <div className="metric-label">Continuous testing across 12 Fabric milestones in 0.34s</div>
            </div>

            <div className="benchmark-metric-card">
              <div className="metric-eyebrow">Modeled Storage Reduction</div>
              <div className="metric-value-wrap">
                <span className="metric-num" data-counter="62" data-suffix="%">62%</span>
                <span className="metric-badge-sub">FinOps Tiering</span>
              </div>
              <div className="metric-label">7-day Hot NVMe KQL Cache vs 30-day Delta Parquet Cold Tier</div>
            </div>

            <div className="benchmark-metric-card">
              <div className="metric-eyebrow">Self-Healing DLQ Rate</div>
              <div className="metric-value-wrap">
                <span className="metric-num" data-counter="66.1" data-suffix="%" data-decimals="1">66.1%</span>
                <span className="metric-badge-sub">Auto-Remediated</span>
              </div>
              <div className="metric-label">5-Worker automated notebook repairing schema drift &amp; null keys</div>
            </div>

          </div>

          {/* Technical Breakdown: Latency Instrument + Architectural Specification Table */}
          <div className="benchmarks-detail-grid">

            {/* Panel A: Ingestion Latency Distribution */}
            <div className="benchmarks-instrument-panel">
              <div className="panel-header">
                <div>
                  <h3 className="panel-title">Latency Distribution vs SLA Threshold</h3>
                </div>
                <span className="instrument-live-tag">
                  <span>Verified Benchmark</span>
                </span>
              </div>

              <p className="panel-desc">
                High-frequency synthetic IoT telemetry ingested via Custom App endpoint into Microsoft Fabric Eventstream, continuously streaming to Eventhouse KQL Database.
              </p>

              {/* Precision Instrument Graph */}
              <div className="instrument-chart-wrapper">
                <svg className="instrument-svg" viewBox="0 0 460 110" aria-label="Ingestion latency percentiles curve">
                  <defs>
                    <linearGradient id="instGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#BC6C25" stopOpacity="0.28"/>
                      <stop offset="100%" stopColor="#BC6C25" stopOpacity="0.0"/>
                    </linearGradient>
                  </defs>
                  {/* Baseline Reference Lines */}
                  <line x1="0" y1="20" x2="460" y2="20" stroke="rgba(255, 255, 255, 0.08)" strokeDasharray="3,3" />
                  <text x="455" y="15" fill="rgba(254, 250, 224, 0.45)" fontSize="10" fontFamily="var(--font-mono)" textAnchor="end">15s SLA Threshold</text>

                  <line x1="0" y1="75" x2="460" y2="75" stroke="rgba(255, 255, 255, 0.05)" />
                  <line x1="0" y1="45" x2="460" y2="45" stroke="rgba(255, 255, 255, 0.05)" />

                  {/* Shaded Area Under Curve */}
                  <path d="M 0,92 L 45,86 L 90,89 L 140,78 L 190,82 L 240,68 L 290,74 L 340,62 L 390,70 L 430,58 L 460,65 L 460,110 L 0,110 Z" fill="url(#instGrad)"/>
                  
                  {/* Clean Precision Line */}
                  <path d="M 0,92 L 45,86 L 90,89 L 140,78 L 190,82 L 240,68 L 290,74 L 340,62 L 390,70 L 430,58 L 460,65" fill="none" stroke="#BC6C25" strokeWidth="2" strokeLinecap="round"/>
                  
                  {/* Calibration Points with Data Anchors */}
                  <circle id="pt-p50" cx="240" cy="68" r="4" fill="#FEFAE0" stroke="#BC6C25" strokeWidth="2" className="inst-point" data-label="p50 Median: 1.70s"/>
                  <circle id="pt-p95" cx="340" cy="62" r="4" fill="#FEFAE0" stroke="#BC6C25" strokeWidth="2" className="inst-point" data-label="p95 Percentile: 4.13s"/>
                  <circle id="pt-pmax" cx="430" cy="58" r="5" fill="#606C38" stroke="#FEFAE0" strokeWidth="2" className="inst-point" data-label="Max Observed: 5.38s"/>
                </svg>

                <div className="instrument-data-table">
                  <div className="data-col" data-percentile="p50">
                    <span className="data-key">p50 Median</span>
                    <span className="data-val">1.70s</span>
                    <span className="data-delta">(-13.30s SLA)</span>
                  </div>
                  <div className="data-col" data-percentile="p95">
                    <span className="data-key">p95 Percentile</span>
                    <span className="data-val">4.13s</span>
                    <span className="data-delta">(-10.87s SLA)</span>
                  </div>
                  <div className="data-col" data-percentile="p99">
                    <span className="data-key">p99 Percentile</span>
                    <span className="data-val">4.80s</span>
                    <span className="data-delta">(-10.20s SLA)</span>
                  </div>
                  <div className="data-col" data-percentile="pmax">
                    <span className="data-key">Max Measured</span>
                    <span className="data-val status-green">5.38s (Pass)</span>
                    <span className="data-delta">(-9.62s SLA)</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Panel B: Editorial Tech Specs Table (Replacing cards-inside-cards) */}
            <div className="benchmarks-specs-panel">
              <div className="panel-header">
                <div>
                  <h3 className="panel-title">End-to-End Platform Stack</h3>
                </div>
              </div>

              <div className="specs-table">
                <div className="spec-row">
                  <span className="spec-label">Simulation Topology</span>
                  <span className="spec-value">8 Facilities • 80 Growing Zones • 6 Streams (Benguet, Tagaytay, Clark, Davao, Iloilo, Laguna, Metro Manila)</span>
                </div>
                <div className="spec-row">
                  <span className="spec-label">Streaming Ingestion</span>
                  <span className="spec-value"><strong>Microsoft Fabric Eventstream</strong> with 9 partitioned routing targets and dead-letter quarantine</span>
                </div>
                <div className="spec-row">
                  <span className="spec-label">Operational KQL Store</span>
                  <span className="spec-value"><strong>Eventhouse KQL DB</strong> with 7-day NVMe hot cache, materialized views &amp; 17-tile dashboard</span>
                </div>
                <div className="spec-row">
                  <span className="spec-label">Medallion Lakehouse</span>
                  <span className="spec-value"><strong>OneLake Delta Lake</strong> (Bronze append shortcuts, Silver cleansing/PII masking, Gold Delta V-Order)</span>
                </div>
                <div className="spec-row">
                  <span className="spec-label">Dimensional Warehouse</span>
                  <span className="spec-value"><strong>Kimball Star Schema</strong> (6 conformed dimensions, 8 fact tables, Regional Row-Level Security)</span>
                </div>
                <div className="spec-row">
                  <span className="spec-label">Business Intelligence</span>
                  <span className="spec-value"><strong>Power BI Direct Lake Mode</strong> (TMDL semantic model, sub-250ms cold memory queries)</span>
                </div>
                <div className="spec-row">
                  <span className="spec-label">Automated Remediation</span>
                  <span className="spec-value"><strong>5-Worker DLQ Notebook</strong> (66.1% self-healing of schema drift &amp; missing keys)</span>
                </div>
                <div className="spec-row">
                  <span className="spec-label">Alerting &amp; DataOps</span>
                  <span className="spec-value"><strong>Fabric Activator (10 Reflex Rules)</strong> &amp; OpenTelemetry distributed span logging</span>
                </div>
              </div>
            </div>

          </div>

        </div>
      </div>
    </section>
  );
}
