import React from 'react';

export default function PlatformSection() {
  return (
    <section id="platform" className="section section-quiet">
      <div className="container">
          <h2 className="section-title">The Microsoft Fabric Platform</h2>
          <p className="section-lead">
            The platform combines real-time stream processing and historical batch warehousing into a unified OneLake architecture. Below is the full end-to-end solution blueprint.
          </p>
        </div>

        {/* Central Solution Blueprint Visual & 3D Spatial Walkthrough Film */}
        <div className="container-wide">
          <div className="spatial-film-showcase" id="spatial-film">
            <div className="spatial-film-header">
              <div className="spatial-film-title-group">
                <span className="spatial-film-title">Microsoft Fabric 3D Architecture Walkthrough</span>
              </div>
              <span className="spatial-film-spec-badge">1080p60 · Continuous 3D Spatial Flythrough · 19 Fabric Artifacts</span>
            </div>
            <div className="spatial-film-player-wrapper">
              <video 
                className="spatial-film-video"
                src="/assets/videos/fabric-smart-farming-film-web.mp4" 
                poster="/assets/videos/fabric-smart-farming-film-poster.jpg" 
                controls 
                autoPlay 
                muted 
                loop 
                playsInline
              ></video>
            </div>
            <div className="spatial-film-footer">
              <span className="spatial-film-path-label">
                Flight path: Fabric Workspace Portal ➔ Eventstream Studio ➔ KQL Queryset ➔ Delta Lakehouse ➔ Self-Healing DLQ ➔ Direct Lake ➔ Activator Reflex ➔ Architecture Loop
              </span>
              <div className="spatial-film-btn-group">
                <a href="/assets/videos/fabric-smart-farming-film-web.mp4" download className="spatial-film-download-btn">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                  <span>Web MP4 (15MB)</span>
                </a>
                <a href="/assets/videos/fabric-smart-farming-film.mp4" download className="spatial-film-download-btn spatial-film-btn-secondary">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
                  <span>Master 1080p60 (57MB)</span>
                </a>
              </div>
            </div>
          </div>
        </div>
        <div className="container-wide">
          <div className="platform-blueprint" data-lightbox-src="/assets/diagrams/microsoft-fabric-solution-architecture.png" data-lightbox-caption="Microsoft Fabric End-to-End Solution Architecture: Dual-path real-time intelligence and OneLake medallion lakehouse.">
            <img src="/assets/diagrams/microsoft-fabric-solution-architecture.png" alt="Microsoft Fabric Solution Architecture Diagram" className="blueprint-img" />
            <div className="blueprint-caption">
              <span>Figure 1: Full-width Microsoft Fabric solution architecture across all 7 layers.</span>
              <span className="blueprint-zoom-hint">Click diagram to expand <svg className="inline-svg-icon" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg></span>
            </div>
          </div>
        </div>

        <div className="container">
          {/* Scrolltelling Architecture Layout with Sticky Dataflow Pipeline Track */}
          <div className="scrolltelling-container">
            
            <aside className="pipeline-scrolltelling-rail">
              <div className="pipeline-rail-title">Dataflow Pipeline</div>
              <div className="pipeline-nodes-list">
                <div className="pipeline-svg-line"></div>
                <div className="pipeline-packet-tracker" id="pipeline-packet-dot"></div>

                <div className="pipeline-nav-node active" data-target-layer="1">
                  <span className="node-idx">01</span>
                  <span>Stream &amp; KQL</span>
                </div>
                <div className="pipeline-nav-node" data-target-layer="2">
                  <span className="node-idx">02</span>
                  <span>Medallion Lakehouse</span>
                </div>
                <div className="pipeline-nav-node" data-target-layer="3">
                  <span className="node-idx">03</span>
                  <span>Kimball Star Schema</span>
                </div>
                <div className="pipeline-nav-node" data-target-layer="4">
                  <span className="node-idx">04</span>
                  <span>Direct Lake Semantic</span>
                </div>
                <div className="pipeline-nav-node" data-target-layer="5">
                  <span className="node-idx">05</span>
                  <span>Activator &amp; DLQ</span>
                </div>
                <div className="pipeline-nav-node" data-target-layer="6">
                  <span className="node-idx">06</span>
                  <span>Security &amp; RLS</span>
                </div>
              </div>
            </aside>

            <div className="layer-walkthrough">

              {/* Layer 1: Streaming Ingestion */}
              <div className="layer-block active-layer" data-layer-idx="1">
                <div className="layer-tag">Layer 01 — Streaming &amp; Operational Path</div>
                <h3 className="layer-title">Real-Time Ingestion &amp; Eventhouse KQL Database</h3>
                <p className="layer-desc">
                  Events from the Python simulator are received by <strong>Microsoft Fabric Eventstream</strong> via a dedicated Custom App endpoint. The stream partitions and routes events to 9 specific targets. Real-time telemetry is ingested directly into <strong>SmartFarmingKQLDB</strong> inside an Eventhouse, where continuous update policies and materialized views pre-aggregate microclimate metrics.
                </p>
                <div className="layer-details-grid">
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Routing Channels</div>
                    <div className="layer-detail-val">9 Eventstream destinations including Dead-Letter sink</div>
                  </div>
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Hot Cache Policy</div>
                    <div className="layer-detail-val">7-day NVMe in-memory cache for sub-second KQL querying</div>
                  </div>
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Operational Dashboard</div>
                    <div className="layer-detail-val">17-tile multi-page real-time KQL dashboard</div>
                  </div>
                </div>
              </div>

              {/* Layer 2: Medallion Lakehouse */}
              <div className="layer-block" data-layer-idx="2">
                <div className="layer-tag">Layer 02 — Historical Analytics Path</div>
                <h3 className="layer-title">OneLake Medallion Architecture: Bronze, Silver &amp; Gold</h3>
                <p className="layer-desc">
                  Historical telemetry is curated within <strong>SmartFarming_Lakehouse</strong> using Microsoft Fabric custom schemas. Data quality progressively increases as records move from raw append files to cleansed tables and finally into a business-ready Gold Kimball Star Schema.
                </p>
                <div className="layer-details-grid">
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Bronze Schema</div>
                    <div className="layer-detail-val">Immutable append-only Delta tables via 9 Zero-Copy shortcuts</div>
                  </div>
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Silver Schema</div>
                    <div className="layer-detail-val">Cleansed, deduplicated, and SHA-256 PII-masked tables</div>
                  </div>
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Gold Schema</div>
                    <div className="layer-detail-val">Kimball Star Schema optimized with Delta V-Order</div>
                  </div>
                </div>
              </div>

              {/* Layer 3: Dimensional Model */}
              <div className="layer-block" data-layer-idx="3">
                <div className="layer-tag">Layer 03 — Data Warehousing</div>
                <h3 className="layer-title">Kimball Dimensional Model (6 Dimensions, 8 Fact Tables)</h3>
                <p className="layer-desc">
                  Rather than building isolated KPI aggregates, the Gold layer models the farming domain into conformed dimensions (facilities, zones, crops, equipment, technicians, dates) and granular business facts (environmental daily, equipment telemetry, crop yield, maintenance SLA, and dead-letter governance).
                </p>
                <div className="layer-details-grid">
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Conformed Dimensions</div>
                    <div className="layer-detail-val">dim_facility, dim_zone, dim_crop, dim_equipment, dim_technician, dim_date</div>
                  </div>
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Business Fact Tables</div>
                    <div className="layer-detail-val">8 fact tables covering operations, biological yield, SLA, and governance</div>
                  </div>
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Storage Optimization</div>
                    <div className="layer-detail-val">Z-Order clustering on (facility_id, timestamp) for partition pruning</div>
                  </div>
                </div>
              </div>

              {/* Layer 4: Power BI Direct Lake */}
              <div className="layer-block" data-layer-idx="4">
                <div className="layer-tag">Layer 04 — Business Intelligence</div>
                <h3 className="layer-title">Power BI Direct Lake Semantic Modeling</h3>
                <p className="layer-desc">
                  The enterprise semantic model (defined in TMDL format) connects directly to Gold OneLake Delta Parquet files using <strong>Direct Lake mode</strong>. This queries cold storage data directly with in-memory performance, completely bypassing scheduled import refreshes and dataset size limits.
                </p>
                <div className="layer-details-grid">
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Storage Architecture</div>
                    <div className="layer-detail-val">Direct Lake (TMDL model) reading OneLake Delta Parquet</div>
                  </div>
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Query Performance</div>
                    <div className="layer-detail-val">&lt; 250ms cold memory queries via VertiPaq compression</div>
                  </div>
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Capacity Fallback</div>
                    <div className="layer-detail-val">Seamless DirectQuery fallback if memory limits are exceeded</div>
                  </div>
                </div>
              </div>

              {/* Layer 5: Alerting & DataOps */}
              <div className="layer-block" data-layer-idx="5">
                <div className="layer-tag">Layer 05 — Incident Response &amp; DataOps</div>
                <h3 className="layer-title">Real-Time Alerting &amp; Dead-Letter Remediation</h3>
                <p className="layer-desc">
                  <strong>Fabric Activator (Reflex)</strong> monitors live streaming events and triggers automated actions for operational farm anomalies (pH drift, thermal spikes) and DataOps engineering issues (ingestion latency, DLQ spikes). Corrupted payloads are quarantined into a dedicated Dead-Letter table and remediated via an automated 5-worker notebook process.
                </p>
                <div className="layer-details-grid">
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Reflex Alert Rules</div>
                    <div className="layer-detail-val">10 Automated rules alerting Teams, Email &amp; Webhooks (&lt; 15s SLA)</div>
                  </div>
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">DLQ Self-Healing</div>
                    <div className="layer-detail-val">5-Worker automated notebook recovering 66.1% of quarantined payloads</div>
                  </div>
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">DataOps Tracing</div>
                    <div className="layer-detail-val">OpenTelemetry distributed spans logged to fact_dataops_pipeline_log</div>
                  </div>
                </div>
              </div>

              {/* Layer 6: Security */}
              <div className="layer-block" data-layer-idx="6">
                <div className="layer-tag">Layer 06 — Security &amp; Governance</div>
                <h3 className="layer-title">Row-Level Security &amp; Dynamic Data Masking</h3>
                <p className="layer-desc">
                  Security is enforced at the warehouse engine level using an inline table-valued predicate function (<code>fn_SecurityPredicate_FacilityRegion</code>) and Security Policies, ensuring regional facility operators can only view data from their assigned geographic jurisdiction. Sensitive operator contact info is dynamically masked using SQL DDM.
                </p>
                <div className="layer-details-grid">
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Row-Level Security</div>
                    <div className="layer-detail-val">Inline TVF Security.fn_SecurityPredicate_FacilityRegion</div>
                  </div>
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Data Masking</div>
                    <div className="layer-detail-val">SHA-256 and SQL DDM masking technician personal contact info</div>
                  </div>
                  <div className="layer-detail-item">
                    <div className="layer-detail-label">Purview Governance</div>
                    <div className="layer-detail-val">Lineage cataloging, sensitivity labels, and simulated Entra ID roles</div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
    </section>
  );
}
