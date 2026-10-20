import React from 'react';

export default function NotesSection() {
  return (
    <section id="notes" className="section section-quiet">
      <div className="container">
        <h2 className="section-title">Engineering Decisions &amp; Defensibility</h2>
        <p className="section-lead">
          Detailed technical rationale behind architectural choices, interview-defensible tradeoffs, honest platform boundaries, and production deployment contrasts.
        </p>

        {/* Defensible Architecture Q&A Accordions */}
        <div className="notes-container">
          <details className="note-item" open>
            <summary className="note-summary">Why Eventhouse and KQL for the real-time path instead of relational SQL?</summary>
            <div className="note-content">
              <p>
                <strong>The Architectural Driver:</strong> In continuous IoT environments (8 facilities, 80 zones emitting multi-stream sensor events), relational database engines encounter severe transaction log contention and lock escalations during high-frequency micro-batch appends.
              </p>
              <p>
                <strong>Why KQL/Eventhouse was Chosen:</strong> KQL (Kusto Query Language) is built on an append-only, distributed column-store architecture with automatic indexing on all columns. Eventhouse supports native continuous update policies, time-window bucket aggregations (<code>bin()</code>), and in-memory NVMe hot caching (7 days). This allows sub-second analytical queries across millions of raw telemetry rows without degrading streaming write throughput.
              </p>
              <p>
                <strong>Engineering Tradeoff:</strong> Eventhouse does not support cross-table relational transactional integrity (ACID multi-statement transactions) or row-level mutations (UPDATE/DELETE). It is purely an append-and-aggregate engine, which is why historical dimensional transformations are routed separately to Delta Lakehouse.
              </p>
            </div>
          </details>

          <details className="note-item">
            <summary className="note-summary">Why build a Kimball Star Schema in Gold rather than querying raw Silver tables?</summary>
            <div className="note-content">
              <p>
                <strong>The Architectural Driver:</strong> Exposing normalized or semi-cleansed Silver Delta tables directly to business analysts forces complex multi-table joins, exposes technical identifiers, and duplicates business logic across separate Power BI reports.
              </p>
              <p>
                <strong>Why Kimball Star Schema was Chosen:</strong> The Gold layer is organized into 6 conformed dimensions (facilities, zones, crops, equipment, technicians, dates) and 8 business fact tables. This provides a single, reusable source of truth for all downstream reporting. Conformed dimensions allow drill-across capabilities between operational telemetry facts (environmental, equipment runtime) and biological harvest yields.
              </p>
              <p>
                <strong>Engineering Tradeoff:</strong> Maintaining dimensional tables requires surrogate key lookups and orchestration pipelines during batch sync. However, it drastically simplifies Power BI DAX calculations, eliminates circular join paths, and structures Delta Parquet files for maximum VertiPaq column compression.
              </p>
            </div>
          </details>

          <details className="note-item">
            <summary className="note-summary">Why Medallion Architecture (Bronze &rarr; Silver &rarr; Gold)?</summary>
            <div className="note-content">
              <p>
                <strong>The Architectural Driver:</strong> A data platform must separate raw data fidelity from analytical curation so that upstream ingestion errors never corrupt analytical reporting and historical raw data can always be reprocessed.
              </p>
              <p>
                <strong>How it Works in this Platform:</strong>
              </p>
              <ul style={{ margin: "0.5rem 0 0.75rem 1.5rem", color: "var(--text-secondary)", fontSize: "0.95rem", lineHeight: "1.6" }}>
                <li><strong>Bronze:</strong> Immutable raw landing via Zero-Copy Fabric shortcuts. Retains raw JSON schema for auditability.</li>
                <li><strong>Silver:</strong> Cleansed Delta tables where timestamps are parsed, duplicates removed, and technician PII masked via SHA-256 hashing.</li>
                <li><strong>Gold:</strong> Business-ready Kimball dimensional star schema optimized with Delta V-Order for Direct Lake reporting.</li>
              </ul>
              <p>
                <strong>Engineering Tradeoff:</strong> Storage footprint increases due to multi-layer persistence. This is mitigated by implementing automated OneLake cold tiering (30-day lifecycle retention).
              </p>
            </div>
          </details>

          <details className="note-item">
            <summary className="note-summary">Why Power BI Direct Lake mode instead of Import or DirectQuery?</summary>
            <div className="note-content">
              <p>
                <strong>The Architectural Driver:</strong> Traditional Power BI Import mode requires scheduled model refreshes (causing data latency and hitting memory size limits), while DirectQuery translates DAX queries into T-SQL on the fly (introducing severe query latency and database compute overhead).
              </p>
              <p>
                <strong>Why Direct Lake was Chosen:</strong> Direct Lake mode allows Power BI's Analysis Services VertiPaq memory engine to read Delta Parquet files directly from OneLake storage without data duplication or scheduled imports. When Spark or Fabric pipelines update Gold Delta tables, Power BI instantly reflects the latest records with in-memory VertiPaq query speeds (&lt; 250ms).
              </p>
              <p>
                <strong>Engineering Tradeoff:</strong> Direct Lake requires Gold Delta tables to adhere to strict schema constraints (standard Delta Parquet with V-Order compression). Queries that exceed capacity memory limits fallback to DirectQuery mode.
              </p>
            </div>
          </details>

          <details className="note-item">
            <summary className="note-summary">What happens to malformed telemetry? (5-Worker DLQ Remediation)</summary>
            <div className="note-content">
              <p>
                <strong>The Architectural Driver:</strong> In physical IoT systems, hardware glitches produce malformed JSON, dropped timestamps, or out-of-range sensor readings. Simply dropping bad records hides upstream hardware degradation, while letting them enter Silver tables corrupts analytical aggregates.
              </p>
              <p>
                <strong>How the DLQ Flow Operates:</strong> Fabric Eventstream applies schema validation filters and routes failed packets to a dedicated <code>Dest_DeadLetterTelemetry</code> quarantine table. The automated <code>Notebook_DeadLetter_Remediation</code> executes a 5-worker self-healing pipeline:
              </p>
              <ul style={{ margin: "0.5rem 0 0.75rem 1.5rem", color: "var(--text-secondary)", fontSize: "0.95rem", lineHeight: "1.6" }}>
                <li><strong>Worker 01:</strong> Validates payload schemas and isolates unparseable records.</li>
                <li><strong>Worker 02:</strong> Repairs null primary keys using deterministic facility-zone lookup tables.</li>
                <li><strong>Worker 03:</strong> Filters electrical noise and clips sensor anomalies into valid bounds.</li>
                <li><strong>Worker 04:</strong> Standardizes physical units (e.g., Fahrenheit to Celsius).</li>
                <li><strong>Worker 05:</strong> Enriches valid records and appends diagnostic traces to <code>fact_dead_letter_governance</code>.</li>
              </ul>
              <p>
                <strong>Engineering Outcome:</strong> Achieved a <strong>66.1% automated remediation rate</strong> on simulated anomalies while preserving 100% data auditability.
              </p>
            </div>
          </details>

          <details className="note-item">
            <summary className="note-summary">How is Security and Governance handled (RLS &amp; DDM)?</summary>
            <div className="note-content">
              <p>
                <strong>The Architectural Driver:</strong> Multi-region agricultural operations require regional facility managers to only access telemetry and work orders within their geographic jurisdiction, while protecting technician personal contact information.
              </p>
              <p>
                <strong>How Security is Enforced:</strong> Row-Level Security (RLS) is enforced at the warehouse database engine via an inline table-valued security predicate function (<code>Security.fn_SecurityPredicate_FacilityRegion</code>) bound to fact tables through a Security Policy. Sensitive technician telephone and email details are dynamically masked using SQL Dynamic Data Masking (DDM).
              </p>
              <p>
                <strong>Distinction from Production IAM:</strong> In this portfolio implementation, security behavior is validated using simulated execution contexts. In an enterprise production deployment, these predicates would be bound directly to Microsoft Entra ID role claims and security groups.
              </p>
            </div>
          </details>
        </div>

        {/* Portfolio Implementation vs. Production Deployment Note */}
        <div className="portfolio-vs-prod-note">
          <h3 className="portfolio-vs-prod-title">Implementation vs. Production Architecture</h3>
          <p className="portfolio-vs-prod-body">
            This project is an independent technical proof of concept inspired by real operational observations at a local farm. It was not deployed at the farm, nor was it formally commissioned or approved by them. It demonstrates how I would approach solving fragmented operational data problems as a data engineer—contrasting the implemented architecture with what would still be required for an enterprise-grade rollout with real paying users, enterprise identity federation, production capacity sizing, and multi-team operational ownership.
          </p>
        </div>

        {/* What I Would Change for a Real Production Deployment (Side-by-Side Cards) */}
        <div className="production-changes-box">
          <div className="production-changes-title">What I Would Change for a Real Enterprise Production Deployment</div>
          <p className="production-changes-sub">
            To demonstrate clear engineering judgment, the cards below contrast how capabilities are implemented in this public portfolio demonstration versus how they would be architected in an enterprise organization:
          </p>

          <div className="prod-changes-dual-grid">

            {/* Card 1: Secrets Management */}
            <div className="prod-dual-card">
              <div className="prod-dual-header">
                <span className="prod-dual-num">01</span>
                <h4 className="prod-dual-title">Secrets &amp; Credential Management</h4>
              </div>
              <div className="dual-env-rows">
                <div className="dual-env-block env-portfolio">
                  <span className="dual-env-tag">Portfolio Implementation</span>
                  <p>Environment-based configuration (<code>.env</code> files) is sufficient for local simulator execution, unit tests, and the public architectural demonstration.</p>
                </div>
                <div className="dual-env-block env-prod">
                  <span className="dual-env-tag">Enterprise Production</span>
                  <p>Secrets, connection strings, and tokens must be stored in <strong>Azure Key Vault</strong> with automated rotation and accessed strictly via <strong>Microsoft Fabric Managed Identities</strong> without persisted credentials.</p>
                </div>
              </div>
            </div>

            {/* Card 2: Identity & Access Management */}
            <div className="prod-dual-card">
              <div className="prod-dual-header">
                <span className="prod-dual-num">02</span>
                <h4 className="prod-dual-title">Enterprise Identity (IAM) &amp; Governance</h4>
              </div>
              <div className="dual-env-rows">
                <div className="dual-env-block env-portfolio">
                  <span className="dual-env-tag">Portfolio Implementation</span>
                  <p>Security behavior is validated through the implemented SQL Row-Level Security predicate functions and simulated role/context test suites (e.g., <code>Operator_Benguet</code>).</p>
                </div>
                <div className="dual-env-block env-prod">
                  <span className="dual-env-tag">Enterprise Production</span>
                  <p>Authorization flows would integrate natively with <strong>Microsoft Entra ID security groups</strong>, automated SCIM provisioning, and Microsoft Purview data catalog classification tags.</p>
                </div>
              </div>
            </div>

            {/* Card 3: CI/CD & ALM Lifecycle */}
            <div className="prod-dual-card">
              <div className="prod-dual-header">
                <span className="prod-dual-num">03</span>
                <h4 className="prod-dual-title">CI/CD &amp; Release Automation</h4>
              </div>
              <div className="dual-env-rows">
                <div className="dual-env-block env-portfolio">
                  <span className="dual-env-tag">Portfolio Implementation</span>
                  <p>Platform artifacts (TMDL semantic models, KQL scripts, DDL) were authored, tested, and validated within the available Fabric workspace environment with GitHub Actions unit testing.</p>
                </div>
                <div className="dual-env-block env-prod">
                  <span className="dual-env-tag">Enterprise Production</span>
                  <p>Requires multi-stage <strong>Fabric Git Integration</strong> with strict branch promotion (Dev &rarr; Test &rarr; Prod), automated validation pipelines, PR approvals, and deployment rollback telemetry.</p>
                </div>
              </div>
            </div>

            {/* Card 4: Capacity & Workload Governance */}
            <div className="prod-dual-card">
              <div className="prod-dual-header">
                <span className="prod-dual-num">04</span>
                <h4 className="prod-dual-title">Capacity Sizing &amp; Workload Isolation</h4>
              </div>
              <div className="dual-env-rows">
                <div className="dual-env-block env-portfolio">
                  <span className="dual-env-tag">Portfolio Implementation</span>
                  <p>The solution was developed and benchmarked on an evaluation <strong>Microsoft Fabric Trial (FT64)</strong> capacity with single-tenant streaming workloads.</p>
                </div>
                <div className="dual-env-block env-prod">
                  <span className="dual-env-tag">Enterprise Production</span>
                  <p>Capacity sizing (e.g., Reserved F64/F128), multi-workload isolation (separating Spark ETL from Direct Lake memory), burst smoothing, and cost controls would be tuned to actual user traffic.</p>
                </div>
              </div>
            </div>

          </div>
        </div>

        {/* Project Limitations & Boundary of Measurements */}
        <div className="limitations-container">
          <div className="limitations-header">
            <h3 className="limitations-title">Project Limitations &amp; Measurement Boundaries</h3>
            <p className="limitations-lead">
              A critical mark of engineering maturity is knowing the exact boundary of what was measured versus what requires enterprise production infrastructure:
            </p>
          </div>

          <div className="limitations-grid">
            <div className="limitation-item">
              <div className="limitation-icon">&bull;</div>
              <div className="limitation-content">
                <strong>Synthetic Telemetry Nuances:</strong> The Python simulator models realistic diurnal cycles, pump degradation curves, and anomalies, but synthetic telemetry cannot reproduce every edge-case electrical failure or physical hardware degradation mode of physical sensors.
              </div>
            </div>

            <div className="limitation-item">
              <div className="limitation-icon">&bull;</div>
              <div className="limitation-content">
                <strong>Workload &amp; Concurrency Bounds:</strong> Portfolio ingestion benchmarks demonstrate platform throughput under controlled simulated batch runs, but do not represent 24/7 continuous enterprise multi-tenant query concurrency.
              </div>
            </div>

            <div className="limitation-item">
              <div className="limitation-icon">&bull;</div>
              <div className="limitation-content">
                <strong>Trial Compute vs. Dedicated Enterprise Capacity:</strong> Fabric Trial capacity (FT64) provides shared compute evaluation, which differs from dedicated enterprise capacity with hard governance, background job throttling, and cross-workspace billing.
              </div>
            </div>

            <div className="limitation-item">
              <div className="limitation-icon">&bull;</div>
              <div className="limitation-content">
                <strong>Simulated Identity vs. Enterprise IAM:</strong> Simulated session context proves that Row-Level Security predicates work mathematically, but does not substitute for corporate Entra ID directory synchronizations and OAuth token exchanges.
              </div>
            </div>

            <div className="limitation-item">
              <div className="limitation-icon">&bull;</div>
              <div className="limitation-content">
                <strong>Modeled Storage vs. Actual Invoice Savings:</strong> The modeled 62% storage reduction represents file size tiering calculations between NVMe hot cache and Delta Parquet, rather than a realized corporate billing invoice.
              </div>
            </div>

            <div className="limitation-item">
              <div className="limitation-icon">&bull;</div>
              <div className="limitation-content">
                <strong>Ingestion Latency vs. End-to-End Alert Delivery:</strong> The measured p50 latency (1.70s) and max latency (5.38s) represent Eventstream-to-KQL ingestion speed, which is distinct from multi-channel alert delivery latency (Teams/Email webhooks) under public internet congestion.
              </div>
            </div>
          </div>
        </div>

      </div>
    </section>
  );
}
