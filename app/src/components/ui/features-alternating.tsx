import React from 'react';
import { Check } from 'lucide-react';

export interface AlternatingFeatureItem {
  stage: string;
  eyebrow: string;
  description: string;
  bullets: string[];
  statValue: string;
  statLabel: string;
  statSubtext: string;
  techChips: string[];
  imageSrc: string;
  imageAlt: string;
  badgeLabel: string;
  caption: string;
}

const FEATURES_DATA: AlternatingFeatureItem[] = [
  {
    stage: '01',
    eyebrow: 'STAGE 01 — INGESTION & WIRE-SPEED QUARANTINE',
    description:
      'Real farm IoT sensors transmit across unstable edge gateways, dropping primary keys, drifting timestamps, and sending unparsed unit strings. Rather than allowing dirty packets to pollute downstream analytical tables, Microsoft Fabric Eventstream evaluates schemas at the wire boundary, instantly routing invalid events to a dedicated Dead-Letter Queue while forwarding clean telemetry to the Bronze lakehouse.',
    bullets: [
      'Eventstream schema filter enforces structural integrity in under 2.8 seconds.',
      'Isolates missing keys (zone_id: null) and type mismatches before Silver Delta tables.',
      'Guarantees zero analytical pipeline crashes from malformed sensor payloads.',
    ],
    statValue: '1.70s',
    statLabel: 'Median Ingestion Latency (p50)',
    statSubtext: 'Observed max 5.38s vs 15.0s SLA target',
    techChips: ['Fabric Eventstream', 'Eventhouse KQL DB', 'Kafka Ingress'],
    imageSrc: '/assets/diagrams/streaming-architecture.png',
    imageAlt: 'Microsoft Fabric Eventstream and KQL streaming architecture diagram showing wire-speed filtering and DLQ quarantine',
    badgeLabel: 'STREAMING ARCHITECTURE TOPOLOGY',
    caption: 'Wire-speed Eventstream pipeline: Edge IoT telemetry validated and routed to Bronze storage or Dead-Letter isolation.',
  },
  {
    stage: '02',
    eyebrow: 'STAGE 02 — DATAOPS & AUTONOMOUS REMEDIATION',
    description:
      'When edge sensors experience battery degradation or firmware resets, manual engineering intervention is too slow to maintain streaming SLAs. Fabric deploys an automated 5-worker PySpark notebook that inspects quarantined Dead-Letter records, resolves missing growing zone identifiers against the hardware MAC address cache, strips malformed units, and appends clean records to Silver Delta Parquet.',
    bullets: [
      'PySpark worker executes lookup_zone_udf(sensor_mac) against device registry.',
      'Automatically strips unparsed unit strings ("2.65mS" to 2.65 numeric float).',
      'Writes clean, deduplicated records to Silver Delta tables with V-Order compression.',
    ],
    statValue: '66.1%',
    statLabel: 'Autonomous Self-Healing Rate',
    statSubtext: '2,723 of 4,120 malformed events repaired with zero manual triage',
    techChips: ['Fabric Spark 3.4', 'Delta Lake Silver', 'Device Registry UDF'],
    imageSrc: '/assets/dashboards/kql_dashboard_pipeline_observability.png',
    imageAlt: 'KQL Dashboard for Pipeline Observability showing automated DLQ triage, worker execution, and self-healing telemetry',
    badgeLabel: 'KQL PIPELINE OBSERVABILITY DASHBOARD',
    caption: 'Autonomous DataOps triage: Real-time monitoring of self-healing Spark workers reconciling quarantined Dead-Letter events.',
  },
  {
    stage: '03',
    eyebrow: 'STAGE 03 — DIRECT LAKE ANALYTICS & REFLEX',
    description:
      'Clean Silver records graduate into a Kimball Gold Star Schema where fact_telemetry_reading connects to conformed facility, zone, and crop dimensions. Power BI Direct Lake mode reads these Delta Parquet files directly from OneLake into VertiPaq memory without data duplication or scheduled refresh latency, while Fabric Activator evaluates microclimate stability to trigger automated greenhouse blowers.',
    bullets: [
      'Zero-copy Direct Lake queries render complex multi-million row visuals in under 1 second.',
      'Kimball star-schema ensures instant dimensional slicing across facilities and crops.',
      'Activator Reflex rules evaluate conditions every 5 seconds for automated intervention.',
    ],
    statValue: '< 1.0s',
    statLabel: 'Direct Lake Visual Query Speed',
    statSubtext: 'Zero dataset refresh latency with direct OneLake VertiPaq caching',
    techChips: ['Power BI Direct Lake', 'Kimball Gold Schema', 'Fabric Activator'],
    imageSrc: '/assets/diagrams/gold_star_schema_erd.png',
    imageAlt: 'Gold Star Schema Entity Relationship Diagram showing fact_telemetry_reading and dimensional tables',
    badgeLabel: 'DIRECT LAKE STAR SCHEMA ERD',
    caption: 'Kimball Gold Star Schema: Zero-copy Direct Lake VertiPaq model serving sub-second queries directly from Delta Parquet.',
  },
];

export default function FeaturesAlternating() {
  return (
    <div className="features-alternating-container">
      {FEATURES_DATA.map((item, index) => {
        const isReversed = index % 2 === 1;

        return (
          <div key={item.stage} className="feature-alternating-block">
            <div className={`feature-row-grid ${isReversed ? 'is-reversed' : ''}`}>
              {/* Visual Card Column: Project Artifact Image */}
              <div className="feature-visual-col">
                <div className="feature-image-card">
                  <div className="feature-image-topbar">
                    <span className="feature-image-badge">{item.badgeLabel}</span>
                    <span className="feature-stage-chip">{item.stage}</span>
                  </div>
                  <div className="feature-image-wrapper">
                    <img
                      src={item.imageSrc}
                      alt={item.imageAlt}
                      className="feature-preview-img"
                      loading="lazy"
                    />
                  </div>
                  <div className="feature-image-bottombar">
                    <span className="feature-image-caption">{item.caption}</span>
                  </div>
                </div>
              </div>

              {/* Editorial Content Column (NO HEADINGS, ONLY EYEBROWS, BODY, BULLETS, STATS) */}
              <div className="feature-content-col">
                <div className="feature-eyebrow-wrap">
                  <span className="feature-eyebrow-text">{item.eyebrow}</span>
                </div>

                <p className="feature-body-text">{item.description}</p>

                <ul className="feature-bullet-list">
                  {item.bullets.map((bullet, bIdx) => (
                    <li key={bIdx} className="feature-bullet-item">
                      <span className="bullet-check-icon">
                        <Check size={15} strokeWidth={2.5} />
                      </span>
                      <span className="bullet-text">{bullet}</span>
                    </li>
                  ))}
                </ul>

                {/* Stat Box */}
                <div className="feature-stat-box">
                  <div className="stat-metric-row">
                    <span className="stat-big-value">{item.statValue}</span>
                    <div className="stat-meta-col">
                      <span className="stat-meta-label">{item.statLabel}</span>
                      <span className="stat-meta-sub">{item.statSubtext}</span>
                    </div>
                  </div>
                </div>

                {/* Technology Chips */}
                <div className="feature-tech-chips">
                  {item.techChips.map((chip, cIdx) => (
                    <span key={cIdx} className="tech-chip-item">
                      {chip}
                    </span>
                  ))}
                </div>
              </div>
            </div>

            {/* Separator Divider */}
            {index < FEATURES_DATA.length - 1 && <div className="feature-row-divider" />}
          </div>
        );
      })}
    </div>
  );
}
