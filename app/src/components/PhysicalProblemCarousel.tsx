import React, { useState } from 'react';
import { Code2, Activity, AlertTriangle, ShieldCheck } from 'lucide-react';
import PolaroidLineCarousel, { Slide } from './ui/polaroid-line-carousel';

interface TelemetryRow {
  sensor: string;
  data: string;
  flag?: string;
  type?: 'alert' | 'critical' | 'warn' | 'normal';
}

interface FailureMode {
  id: string;
  idx: string;
  category: string;
  title: string;
  italicTitle: string;
  image: string;
  desc: string;
  caption: string;
  telemetry: TelemetryRow[];
  consequenceLabel: string;
  consequenceText: string;
  defenseText: string;
  drawerTarget: string;
  codeTitle: string;
  codeSnippet: string;
}

const FAILURE_MODES: FailureMode[] = [
  {
    id: 'mode-01',
    idx: '01',
    category: 'Microclimate Drift',
    title: 'Atmospheric & Thermal Runaway',
    italicTitle: 'Atmospheric & Thermal Runaway',
    image: '/assets/images/farm-crop-canopy.jpg',
    desc: 'Canopy temperature, relative humidity, CO2 levels, and Photosynthetically Active Radiation (PAR) fluctuate rapidly across 80 growing zones.',
    caption: 'Canopy microclimate drift across 80 growing zones triggers stomatal closure, desiccation, and irreversible tip burn within 90 minutes.',
    telemetry: [
      { sensor: 'Zone-003 Ambient', data: '34.8°C', flag: 'Spike', type: 'alert' },
      { sensor: 'Relative Humidity', data: '78.4%', type: 'normal' },
      { sensor: 'VPD Canopy Index', data: '1.84 kPa', type: 'normal' },
    ],
    consequenceLabel: 'Biological Consequence',
    consequenceText: 'Rapid stomatal closure, impaired transpiration, and irreversible tip burn on high-value greens within 90 minutes.',
    defenseText: 'Eventstream → Eventhouse KQL DB → Activator Rule 01 automated greenhouse ventilation trigger (< 5s SLA).',
    drawerTarget: 'kql-rule-01',
    codeTitle: 'Activator Rule 01: Thermal Runaway & VPD Desiccation',
    codeSnippet: `// Activator Rule 01: Thermal Runaway & VPD Desiccation
EnvironmentalTelemetry
| where Timestamp > ago(5m)
| where Temperature_C > 30.0 and RelativeHumidity_Pct < 60.0
| extend VPD_kPa = round(calculate_vpd(Temperature_C, RelativeHumidity_Pct), 2)
| where VPD_kPa > 1.60
| project Timestamp, FacilityId, ZoneId, Temperature_C, RelativeHumidity_Pct, VPD_kPa
| extend AlertSeverity = "CRITICAL_ACTION_REQUIRED"`,
  },
  {
    id: 'mode-02',
    idx: '02',
    category: 'Nutrient Imbalance',
    title: 'Osmotic & pH Lockout',
    italicTitle: 'Osmotic & pH Lockout',
    image: '/assets/images/farm-nft-channels.jpg',
    desc: 'Hydroponic reservoir electrical conductivity (EC) and pH levels drift as crops consume ionic nutrients, risking chemical lockout.',
    caption: 'Hydroponic reservoir pH drops below 5.5, locking root micronutrient uptake and threatening severe crop stunt with 40%+ harvest loss.',
    telemetry: [
      { sensor: 'Reservoir pH', data: '5.48', flag: 'Lockout', type: 'critical' },
      { sensor: 'Electrical Conductivity', data: '2.65 mS/cm', type: 'normal' },
      { sensor: 'Dosing Status', data: 'Active Auto', type: 'normal' },
    ],
    consequenceLabel: 'Biological Consequence',
    consequenceText: 'Roots cannot absorb micronutrients (iron/calcium) when pH drops below 5.5, risking severe crop stunt and 40%+ harvest loss.',
    defenseText: 'Continuous KQL update policy computes moving pH averages; Activator Rule 02 alerts facility dosing controller.',
    drawerTarget: 'kql-rule-02',
    codeTitle: 'Activator Rule 02: Dosing Controller Lockout Alert',
    codeSnippet: `// Activator Rule 02: Dosing Controller Lockout Alert
ReservoirTelemetry
| where Timestamp > ago(10m)
| summarize MovingAvg_pH = round(avg(Reservoir_pH), 2), MovingAvg_EC = round(avg(ElectricalConductivity_mS), 2) by StationId
| where MovingAvg_pH < 5.50 or MovingAvg_EC > 2.80
| extend Remediation = iff(MovingAvg_pH < 5.50, "TRIGGER_ALKALINE_BUFFER", "TRIGGER_RO_DILUTION")`,
  },
  {
    id: 'mode-03',
    idx: '03',
    category: 'Mechanical Degradation',
    title: 'Pump Cavitation & Bearing Wear',
    italicTitle: 'Pump Cavitation & Bearing Wear',
    image: '/assets/images/farm-greenhouse-controls.jpg',
    desc: 'Submersible dosing pumps and HVAC circulation blowers experience thermal stress and vibration spikes before physical seizure.',
    caption: 'Submersible dosing pump bearing vibration spikes past 7.0 mm/s, risking motor seizure and flow stoppage to vertical growing tiers within 4 hours.',
    telemetry: [
      { sensor: 'Pump Vibration', data: '7.82 mm/s', flag: 'Cavitation', type: 'warn' },
      { sensor: 'Motor Runtime', data: '4,120 hrs', type: 'normal' },
      { sensor: 'MTBF Wear Index', data: '84.2%', type: 'normal' },
    ],
    consequenceLabel: 'Operational Consequence',
    consequenceText: 'Pump seizure cuts nutrient flow to vertical tiers, causing dry roots within 4 hours and costly emergency technician dispatch.',
    defenseText: 'Telemetry partitioned to fact_equipment_health_daily; Activator Rule 03 escalates maintenance work orders.',
    drawerTarget: 'kql-rule-03',
    codeTitle: 'Activator Rule 03: Mechanical Equipment Degradation',
    codeSnippet: `// Activator Rule 03: Mechanical Equipment Degradation
EquipmentHealth
| where Timestamp > ago(15m)
| where Vibration_mm_s > 7.0 or BearingTemp_C > 75.0
| project Timestamp, FacilityId, PumpId, Vibration_mm_s, BearingTemp_C, MTBF_Hours
| extend AnomalyType = "BEARING_CAVITATION"
| extend Escalation = "DISPATCH_FIELD_TECHNICIAN"`,
  },
  {
    id: 'mode-04',
    idx: '04',
    category: 'Data Quality Anomaly',
    title: 'Telemetry Corruption & Clock Skew',
    italicTitle: 'Telemetry Corruption & Skew',
    image: '/assets/images/images (3).jpg',
    desc: 'Edge IoT hardware drops packets, emits null identifiers, or generates electrical noise spikes that threaten downstream analytics.',
    caption: 'Edge IoT hardware drops packets, emits null sensor MACs, and skews timestamps by +420s; routed to Dead-Letter Queue with 66.1% auto-healing.',
    telemetry: [
      { sensor: 'Ingress Status', data: 'Malformed', flag: 'DLQ Sink', type: 'critical' },
      { sensor: 'Clock Skew', data: '+420.0s', type: 'normal' },
      { sensor: 'Repair Worker', data: 'Worker 02 OK', type: 'normal' },
    ],
    consequenceLabel: 'Downstream Consequence',
    consequenceText: 'Corrupts Gold Kimball fact joins and distorts Direct Lake reports if bad records are allowed into Silver Delta tables.',
    defenseText: 'Schema filter routes malformed events to Dest_DeadLetterTelemetry; 5-worker notebook achieves 66.1% self-healing.',
    drawerTarget: 'kql-rule-04',
    codeTitle: '5-Worker Automated DLQ Remediation Engine',
    codeSnippet: `# 5-Worker Automated Dead-Letter Queue Remediation Engine
spark.read.format("delta").table("bronze_dead_letter") \\
    .filter("status = 'UNRESOLVED'") \\
    .withColumn("remediated_zone_id", when(col("zone_id").isNull(), lookup_zone_udf(col("payload.sensor_mac"))).otherwise(col("zone_id"))) \\
    .withColumn("remediation_flag", lit("AUTO_REPAIRED_WORKER_02")) \\
    .write.format("delta").mode("append").saveAsTable("silver_telemetry_clean")`,
  },
  {
    id: 'mode-05',
    idx: '05',
    category: 'Hydrostatic Drift',
    title: 'Vertical Column Pressure Drift',
    italicTitle: 'Vertical Pressure Drift',
    image: '/assets/images/farm-vertical-towers.jpg',
    desc: 'Hydrostatic pressure imbalances across vertical aeroponic columns starve upper misting nozzles while over-saturating lower collection reservoirs.',
    caption: 'Pressure drops starve top-tier aeroponic misting nozzles while drowning lower root zones, creating stark gradient yield variations.',
    telemetry: [
      { sensor: 'Top Manifold', data: '1.12 bar', flag: 'Under-press', type: 'alert' },
      { sensor: 'Bottom Return', data: '4.85 L/min', type: 'normal' },
      { sensor: 'Emitter Coeff', data: '81.4%', type: 'normal' },
    ],
    consequenceLabel: 'Biological Consequence',
    consequenceText: 'Top-tier crops suffer dehydration within 2 hours while bottom tiers risk pythium root rot from standing water stagnation.',
    defenseText: 'KQL anomaly rule flags pressure gradient anomalies across manifold tiers and commands proportional valve balancing.',
    drawerTarget: 'kql-rule-05',
    codeTitle: 'Activator Rule 05: Vertical Manifold Pressure Differential',
    codeSnippet: `// Activator Rule 05: Vertical Manifold Pressure Differential
HydrostaticTelemetry
| where Timestamp > ago(5m)
| summarize Top_Bar = avg(TopPressure_Bar), Bottom_Bar = avg(BottomPressure_Bar) by TowerClusterId
| extend Delta_Bar = round(Bottom_Bar - Top_Bar, 2)
| where Delta_Bar > 1.25
| extend Command = "REBALANCE_BOOSTER_SOLENOID"`,
  },
  {
    id: 'mode-06',
    idx: '06',
    category: 'Calibration Drift',
    title: 'Manual Logs & Probe Oxidation',
    italicTitle: 'Probe Drift & Manual Records',
    image: '/assets/images/farm-origin-inspection.jpg',
    desc: 'Galvanic probe oxidation and whiteboard logging lag introduce stealthy calibration offsets that skew automated dosing controllers.',
    caption: 'Manual whiteboard logging intervals and galvanic probe oxidation produce stealthy sensor drift that bypasses static threshold alerts.',
    telemetry: [
      { sensor: 'Probe Drift Delta', data: '+0.42 pH', flag: 'Offset', type: 'warn' },
      { sensor: 'Oxidation Index', data: '68.2%', type: 'normal' },
      { sensor: 'Calibration Age', data: '24 Days', type: 'normal' },
    ],
    consequenceLabel: 'Systemic Consequence',
    consequenceText: 'Silent pH offset causes chronic under-dosing of calcium nitrate, reducing overall harvest biomass by 28% without triggering static alarms.',
    defenseText: 'Cross-sensor spatial correlation matrix flags divergent probes against neighbor cluster medians before harvest impact.',
    drawerTarget: 'kql-rule-06',
    codeTitle: 'Activator Rule 06: Spatial Cross-Probe Correlation Drift',
    codeSnippet: `// Activator Rule 06: Spatial Cross-Probe Correlation Drift
ReservoirTelemetry
| where Timestamp > ago(30m)
| summarize Probe_pH = avg(Reservoir_pH) by BayId, SensorId
| join kind=inner (
    ReservoirTelemetry
    | where Timestamp > ago(30m)
    | summarize Median_pH = percentile(Reservoir_pH, 50) by BayId
  ) on BayId
| extend pH_Offset = abs(Probe_pH - Median_pH)
| where pH_Offset > 0.35
| extend Action = "FLAG_PROBE_RECALIBRATION"`,
  },
];

export default function PhysicalProblemCarousel() {
  const [activeIndex, setActiveIndex] = useState(0);
  const [openDrawers, setOpenDrawers] = useState<Record<string, boolean>>({});

  const toggleDrawer = (targetId: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setOpenDrawers((prev) => ({
      ...prev,
      [targetId]: !prev[targetId],
    }));
  };

  // Build slides for PolaroidLineCarousel
  const slides: Slide[] = FAILURE_MODES.map((mode) => ({
    image: mode.image,
    title: mode.italicTitle,
    caption: mode.caption,
    alt: mode.title,
    category: mode.category,
    idx: mode.idx,
  }));

  const activeMode = FAILURE_MODES[activeIndex] || FAILURE_MODES[0];
  const isKqlOpen = !!openDrawers[activeMode.drawerTarget];

  return (
    <div className="problem-polaroid-experience">
      {/* 21st.dev Hanging Polaroid Image Carousel Component */}
      <div className="polaroid-carousel-mount">
        <PolaroidLineCarousel
          slides={slides}
          height="620px"
          cardWidth={380}
          sag={44}
          swing={1.2}
          autoplay={0}
          string="#8C673D"
          background="transparent"
          ink="#283618"
          onChange={(newIndex) => setActiveIndex(newIndex)}
          ariaLabel="Physical Farm Operational Failure Modes Carousel"
        />
      </div>

      {/* Reactive Diagnostic Telemetry & Fabric Real-Time Defense Card */}
      <div className="polaroid-active-scenario-card" key={activeMode.id}>
        <div className="scenario-card-header">
          <div className="scenario-header-left">
            <span className="scenario-pill-idx">{activeMode.idx}</span>
            <span className="scenario-pill-cat">{activeMode.category}</span>
            <h3 className="scenario-card-title">{activeMode.title}</h3>
          </div>
          <div className="scenario-header-badge">
            <Activity size={14} className="pulse-icon" />
            <span>Scenario Active</span>
          </div>
        </div>

        <p className="scenario-card-desc">{activeMode.desc}</p>

        {/* Telemetry Pills */}
        <div className="scenario-telemetry-row">
          <div className="telemetry-row-title">
            <span>Observed Telemetry Signatures:</span>
          </div>
          <div className="scenario-telemetry-grid">
            {activeMode.telemetry.map((t, idx) => (
              <div key={idx} className="telemetry-pill-box">
                <span className="telemetry-box-sensor">{t.sensor}</span>
                <div className="telemetry-box-val-wrap">
                  <span className={`telemetry-box-val ${t.type && t.type !== 'normal' ? t.type : ''}`}>
                    {t.data}
                  </span>
                  {t.flag && <span className="telemetry-box-flag">{t.flag}</span>}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Consequence Callout */}
        <div className="scenario-consequence-card">
          <div className="consequence-icon-col">
            <AlertTriangle size={18} className="consequence-icon" />
          </div>
          <div className="consequence-text-col">
            <span className="consequence-label">{activeMode.consequenceLabel}</span>
            <p className="consequence-body">{activeMode.consequenceText}</p>
          </div>
        </div>

        {/* Defense & KQL Trigger */}
        <div className="scenario-defense-card">
          <div className="defense-info-row">
            <div className="defense-left">
              <ShieldCheck size={18} className="defense-shield-icon" />
              <div>
                <span className="defense-tag">Fabric Real-Time Defense</span>
                <p className="defense-statement-text">{activeMode.defenseText}</p>
              </div>
            </div>
            <button
              type="button"
              className={`defense-kql-toggle-btn ${isKqlOpen ? 'is-open' : ''}`}
              onClick={(e) => toggleDrawer(activeMode.drawerTarget, e)}
              aria-expanded={isKqlOpen}
            >
              <Code2 size={15} />
              <span>{isKqlOpen ? 'Hide KQL Rule' : 'Inspect KQL Rule'}</span>
            </button>
          </div>

          {/* Collapsible KQL Drawer */}
          {isKqlOpen && (
            <div className="kql-code-drawer animate-drawer-down" onClick={(e) => e.stopPropagation()}>
              <div className="drawer-bar">
                <span className="drawer-title">{activeMode.codeTitle}</span>
                <span className="drawer-badge">Eventhouse Kusto KQL</span>
              </div>
              <pre className="drawer-code-block">
                <code>{activeMode.codeSnippet}</code>
              </pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
