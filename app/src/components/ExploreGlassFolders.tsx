"use client";

import React, { useState, useEffect, useCallback, useRef } from "react";
import GlassFolder, { FolderFile } from "@/components/ui/glass-folder-cards";
import {
  Layers,
  BarChart3,
  PieChart,
  BellRing,
  ZoomIn,
  ZoomOut,
  RotateCcw,
  X,
  ChevronLeft,
  ChevronRight,
  ArrowLeft,
  ExternalLink,
  Sparkles,
} from "lucide-react";

export interface ArtifactItem {
  id: string;
  name: string;
  meta: string;
  desc: string;
  image: string;
}

export interface FolderCategory {
  id: string;
  label: string;
  countLabel: string;
  count: number;
  art: "verdant" | "ember" | "aurora" | "dusk";
  seed: number;
  icon: React.ReactNode;
  accent: string;
  accentSoft: string;
  tagline: string;
  items: ArtifactItem[];
}

const CATEGORIES: FolderCategory[] = [
  {
    id: "architecture",
    label: "Architecture Blueprints",
    countLabel: "8 Schematics",
    count: 8,
    art: "verdant",
    seed: 24,
    icon: <Layers size={18} className="text-[#A3B872]" />,
    accent: "#687941",
    accentSoft: "rgba(104, 121, 65, 0.16)",
    tagline: "End-to-end Microsoft Fabric streaming, Medallion lakehouse, and Star Schema engineering topology.",
    items: [
      {
        id: "arch-1",
        name: "Solution Architecture",
        meta: "Microsoft Fabric Blueprint",
        desc: "End-to-end platform blueprint across streaming and OneLake medallion layers.",
        image: "/assets/diagrams/microsoft-fabric-solution-architecture.png",
      },
      {
        id: "arch-2",
        name: "Streaming Ingestion",
        meta: "Eventstream & KQL Policies",
        desc: "Eventstream 9-destination routing and continuous KQL update policies.",
        image: "/assets/diagrams/streaming-architecture.png",
      },
      {
        id: "arch-3",
        name: "Medallion Lakehouse",
        meta: "Bronze/Silver/Gold Delta",
        desc: "Bronze raw landing, Silver PII masking, and Gold Kimball tables.",
        image: "/assets/diagrams/medallion-architecture.png",
      },
      {
        id: "arch-4",
        name: "Gold Star Schema ERD",
        meta: "Kimball Dimensional Model",
        desc: "6 conformed dimensions and 8 business fact tables with surrogate keys.",
        image: "/assets/diagrams/gold_star_schema_erd.png",
      },
      {
        id: "arch-5",
        name: "Security & Governance",
        meta: "Row-Level Security & DDM",
        desc: "Regional Row-Level Security predicate functions and SQL Dynamic Data Masking.",
        image: "/assets/diagrams/security-architecture.png",
      },
      {
        id: "arch-6",
        name: "DataOps Observability",
        meta: "OpenTelemetry Spans & Logs",
        desc: "OpenTelemetry distributed tracing and fact_dataops_pipeline_log shortcuts.",
        image: "/assets/diagrams/monitoring-strategy.png",
      },
      {
        id: "arch-7",
        name: "Storage Tiering Lifecycle",
        meta: "Hot KQL vs Cold OneLake",
        desc: "7-day Hot KQL Cache vs 30-day Cold OneLake storage lifecycle strategy.",
        image: "/assets/diagrams/data-retention-strategy.png",
      },
      {
        id: "arch-8",
        name: "Batch Orchestration",
        meta: "Master CDC Sync Pipelines",
        desc: "Master orchestration pipelines, incremental micro-batch sync, and CDC merges.",
        image: "/assets/diagrams/batch-architecture.png",
      },
    ],
  },
  {
    id: "kql-dashboards",
    label: "Real-Time KQL Dashboards",
    countLabel: "3 Operational HUDs",
    count: 3,
    art: "ember",
    seed: 42,
    icon: <BarChart3 size={18} className="text-[#BC6C25]" />,
    accent: "#BC6C25",
    accentSoft: "rgba(188, 108, 37, 0.16)",
    tagline: "Sub-second operational monitoring, IoT zone stability heatmaps, and streaming ingestion SLAs.",
    items: [
      {
        id: "kql-1",
        name: "Executive Facility Operations",
        meta: "Live Health & Wear Heatmap",
        desc: "Real-time facility health indices (Benguet 92.94, Clark 93.13), equipment wear heatmap, and emergency work order SLAs.",
        image: "/assets/dashboards/kql_dashboard_business_operations.png",
      },
      {
        id: "kql-2",
        name: "DataOps Pipeline Trace & SLA",
        meta: "100.0% Success & Medallion Trace",
        desc: "100.0% Pipeline Run Success Rate, Medallion Pipeline Trace & Execution History, 2.84 min End-to-End Batch SLA Duration.",
        image: "/assets/dashboards/kql_dashboard_pipeline_observability.png",
      },
      {
        id: "kql-3",
        name: "Streaming Ingress & DLQ Governance",
        meta: "Sub-3.0s Latency & Anomaly Rates",
        desc: "Per-stream ingestion lag tracking (SLA < 3.0s), Ingress Data Quality Scorecard, and Dead-Letter Queue anomaly rates.",
        image: "/assets/dashboards/kql_dashboard_streaming_sla_governance.png",
      },
    ],
  },
  {
    id: "direct-lake",
    label: "Direct Lake Reports",
    countLabel: "5 Power BI Reports",
    count: 5,
    art: "aurora",
    seed: 88,
    icon: <PieChart size={18} className="text-[#DDA15E]" />,
    accent: "#DDA15E",
    accentSoft: "rgba(221, 161, 94, 0.14)",
    tagline: "Sub-second Direct Lake Power BI analytics queried directly from Gold Delta Parquet without import refreshes.",
    items: [
      {
        id: "dl-1",
        name: "Executive Operations Overview",
        meta: "Nationwide Control Tower & Yield",
        desc: "Nationwide facility control tower, harvest yield realization (80% Grade A), wholesale revenue (₱137.83M), and production distribution.",
        image: "/assets/reports/page_1_executive_operations.png",
      },
      {
        id: "dl-2",
        name: "Environmental Microclimates",
        meta: "VPD, DLI & Crop Health",
        desc: "Zone-level air temperature, relative humidity, VPD (1.64 kPa), DLI photoperiods (16.88 mol/m²/d), and biomass growth rates.",
        image: "/assets/reports/page_2_environmental_microclimates.png",
      },
      {
        id: "dl-3",
        name: "Equipment Health & Maintenance",
        meta: "Predictive MTTR & Asset Uptime",
        desc: "Dosing pump runtime hours, motor vibration, failure probabilities, MTTR (0.8 hrs), and technician resolution SLAs.",
        image: "/assets/reports/page_3_equipment_health_maintenance.png",
      },
      {
        id: "dl-4",
        name: "Irrigation & Dosing Efficiency",
        meta: "Hydro-Nutrient Resource Efficiency",
        desc: "Water delivery (922.1K L), nutrient solution (55.8K L), energy usage (6.3M kWh), and carbon footprint optimization.",
        image: "/assets/reports/page_4_irrigation_dosing.png",
      },
      {
        id: "dl-5",
        name: "DataOps & Pipeline Ingestion",
        meta: "97.6% Quality Score & Ingress Audit",
        desc: "97.64% Data Quality Score, 66.1% Auto-Remediation Rate, DLQ quarantine reasons, and stream diagnostic matrix.",
        image: "/assets/reports/page_5_dataops_observability.png",
      },
    ],
  },
  {
    id: "activator-rules",
    label: "Activator Alert Rules",
    countLabel: "10 Reflex Hooks",
    count: 10,
    art: "dusk",
    seed: 105,
    icon: <BellRing size={18} className="text-[#EF4444]" />,
    accent: "#EF4444",
    accentSoft: "rgba(239, 68, 68, 0.16)",
    tagline: "Continuous anomaly triggers and automated remediation across 80 IoT growing zones.",
    items: [
      {
        id: "act-1",
        name: "Rule 01: Thermal Runaway",
        meta: "Canopy Temperature Spike > 32°C",
        desc: "Operational trigger when ambient temperature exceeds critical 32°C threshold.",
        image: "/assets/alerts/hook1_activator_alert.png",
      },
      {
        id: "act-2",
        name: "Rule 02: Nutrient pH Imbalance",
        meta: "Drift Outside 5.5 - 6.5",
        desc: "Automated dosing dispatch when substrate pH drifts beyond biological nutrient absorption range.",
        image: "/assets/alerts/hook2_activator_alert.png",
      },
      {
        id: "act-3",
        name: "Rule 03: Pump Cavitation Spike",
        meta: "Vibration FFT > 1.8 mm/s",
        desc: "High-frequency accelerometer trigger alerting maintenance engineers before catastrophic pump failure.",
        image: "/assets/alerts/hook3_activator_alert.png",
      },
      {
        id: "act-4",
        name: "Rule 04: Chiller Inverter Surge",
        meta: "Current Spike > 45A Electrical",
        desc: "Protective electrical threshold cut-off to prevent HVAC compressor burnout in high heat index.",
        image: "/assets/alerts/hook4_activator_alert.png",
      },
      {
        id: "act-5",
        name: "Rule 05: Biological Stress",
        meta: "Canopy VPD Transpiration Deficit",
        desc: "Triggers automated alert when canopy temperature differential indicates biological transpiration stress.",
        image: "/assets/alerts/hook5_activator_alert.png",
      },
      {
        id: "act-6",
        name: "Rule 06: Work Order SLA Breach",
        meta: "Emergency Resolution Escalation",
        desc: "Escalates unresolved equipment maintenance tickets exceeding operational SLA resolution windows.",
        image: "/assets/alerts/hook6_activator_alert.png",
      },
      {
        id: "act-7",
        name: "Rule 07: Stream Processing Lag",
        meta: "Update Policy SLA Delayed",
        desc: "DataOps trigger alerting engineering when Eventstream consumer lag exceeds the 15-second SLA.",
        image: "/assets/alerts/hook7_activator_alert.png",
      },
      {
        id: "act-8",
        name: "Rule 08: Missing Primary Key",
        meta: "Critical Ingress Data Integrity",
        desc: "High-priority incident trigger when events arrive with null facility, zone, or equipment identifiers.",
        image: "/assets/alerts/hook8_activator_alert.png",
      },
      {
        id: "act-9",
        name: "Rule 09: DLQ Burst Rate",
        meta: "Quarantine Volume Surge",
        desc: "Detects sudden bursts of quarantined payloads indicating upstream telemetry format shifts.",
        image: "/assets/alerts/hook9_activator_alert.png",
      },
      {
        id: "act-10",
        name: "Rule 10: Ingress Schema Drift",
        meta: "Automated Quarantine Dead-Letter",
        desc: "Alerts data engineers when malformed telemetry fields exceed 5% of raw stream throughput.",
        image: "/assets/alerts/hook10_activator_alert.png",
      },
    ],
  },
];

export default function ExploreGlassFolders() {
  // Dedicated folder browsing state (null = main repository view)
  const [selectedCategoryId, setSelectedCategoryId] = useState<string | null>(null);

  // Lightbox modal inspection state
  const [modalArtifact, setModalArtifact] = useState<{
    category: FolderCategory;
    itemIndex: number;
  } | null>(null);

  // Exact scroll position retention ref
  const scrollYRef = useRef<number>(0);
  const lastTriggerRef = useRef<HTMLElement | null>(null);
  const sectionRef = useRef<HTMLElement | null>(null);

  // Zoom & Pan state for the modal preview
  const [zoomScale, setZoomScale] = useState(1);
  const [panPos, setPanPos] = useState({ x: 0, y: 0 });
  const [isPanning, setIsPanning] = useState(false);
  const panStartRef = useRef<{ startX: number; startY: number; initX: number; initY: number }>({
    startX: 0,
    startY: 0,
    initX: 0,
    initY: 0,
  });

  const handleOpenFolder = (categoryId: string) => {
    scrollYRef.current = window.scrollY || document.documentElement.scrollTop;
    setSelectedCategoryId(categoryId);
    // Smoothly scroll to the repository section header for consistent orientation
    if (sectionRef.current) {
      sectionRef.current.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  };

  const handleReturnToRepo = () => {
    setSelectedCategoryId(null);
    requestAnimationFrame(() => {
      window.scrollTo({
        top: scrollYRef.current,
        behavior: "instant" as ScrollBehavior,
      });
    });
  };

  const handleOpenArtifact = (
    category: FolderCategory,
    itemIndex: number,
    triggerEl?: HTMLElement | null
  ) => {
    scrollYRef.current = window.scrollY || document.documentElement.scrollTop;
    if (triggerEl) {
      lastTriggerRef.current = triggerEl;
    } else if (document.activeElement instanceof HTMLElement) {
      lastTriggerRef.current = document.activeElement;
    }

    setModalArtifact({ category, itemIndex });
    setZoomScale(1);
    setPanPos({ x: 0, y: 0 });
  };

  const handleCloseModal = useCallback(() => {
    setModalArtifact(null);
    setZoomScale(1);
    setPanPos({ x: 0, y: 0 });

    requestAnimationFrame(() => {
      window.scrollTo({
        top: scrollYRef.current,
        behavior: "instant" as ScrollBehavior,
      });
      if (lastTriggerRef.current && document.contains(lastTriggerRef.current)) {
        lastTriggerRef.current.focus({ preventScroll: true });
      }
    });
  }, []);

  const handleNextArtifact = useCallback(() => {
    if (!modalArtifact) return;
    const { category, itemIndex } = modalArtifact;
    const nextIndex = (itemIndex + 1) % category.items.length;
    setModalArtifact({ category, itemIndex: nextIndex });
    setZoomScale(1);
    setPanPos({ x: 0, y: 0 });
  }, [modalArtifact]);

  const handlePrevArtifact = useCallback(() => {
    if (!modalArtifact) return;
    const { category, itemIndex } = modalArtifact;
    const prevIndex = (itemIndex - 1 + category.items.length) % category.items.length;
    setModalArtifact({ category, itemIndex: prevIndex });
    setZoomScale(1);
    setPanPos({ x: 0, y: 0 });
  }, [modalArtifact]);

  // Clean body scroll lock during artifact inspection
  useEffect(() => {
    if (!modalArtifact) return;

    const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
    const origBodyOverflow = document.body.style.overflow;
    const origHtmlOverflow = document.documentElement.style.overflow;
    const origBodyPaddingRight = document.body.style.paddingRight;

    document.body.style.overflow = "hidden";
    document.documentElement.style.overflow = "hidden";
    if (scrollbarWidth > 0) {
      document.body.style.paddingRight = `${scrollbarWidth}px`;
    }

    return () => {
      document.body.style.overflow = origBodyOverflow;
      document.documentElement.style.overflow = origHtmlOverflow;
      document.body.style.paddingRight = origBodyPaddingRight;
    };
  }, [modalArtifact]);

  // Keyboard navigation for modal inspection
  useEffect(() => {
    if (!modalArtifact) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        e.preventDefault();
        e.stopPropagation();
        handleCloseModal();
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        handleNextArtifact();
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        handlePrevArtifact();
      }
    };
    window.addEventListener("keydown", handleKeyDown, { capture: true });
    return () => window.removeEventListener("keydown", handleKeyDown, { capture: true });
  }, [modalArtifact, handleCloseModal, handleNextArtifact, handlePrevArtifact]);

  // Pan event handlers for inspection image
  const handlePointerDown = (e: React.PointerEvent<HTMLImageElement>) => {
    if (zoomScale <= 1) return;
    setIsPanning(true);
    panStartRef.current = {
      startX: e.clientX,
      startY: e.clientY,
      initX: panPos.x,
      initY: panPos.y,
    };
    (e.target as HTMLElement).setPointerCapture(e.pointerId);
  };

  const handlePointerMove = (e: React.PointerEvent<HTMLImageElement>) => {
    if (!isPanning) return;
    const dx = e.clientX - panStartRef.current.startX;
    const dy = e.clientY - panStartRef.current.startY;
    setPanPos({
      x: panStartRef.current.initX + dx,
      y: panStartRef.current.initY + dy,
    });
  };

  const handlePointerUp = (e: React.PointerEvent<HTMLImageElement>) => {
    if (!isPanning) return;
    setIsPanning(false);
    try {
      (e.target as HTMLElement).releasePointerCapture(e.pointerId);
    } catch {
      // Ignore
    }
  };

  const selectedCategory = selectedCategoryId
    ? CATEGORIES.find((c) => c.id === selectedCategoryId) || null
    : null;

  const currentArtifact = modalArtifact
    ? modalArtifact.category.items[modalArtifact.itemIndex]
    : null;

  return (
    <section
      ref={sectionRef}
      id="platform-artifacts"
      className="explore-glass-folders-wrapper scroll-mt-24 py-16 sm:py-20 lg:py-24 max-w-7xl xl:max-w-[1440px] 2xl:max-w-[1520px] mx-auto px-4 sm:px-6 lg:px-8 relative z-10"
    >
      {/* ── STATE 1: MAIN REPOSITORY VIEW (Clean 4-Folder Overview) ─────────── */}
      {!selectedCategory ? (
        <div className="flex flex-col items-center w-full">
          {/* Header with clear separation */}
          <div className="w-full mb-12 sm:mb-16 pb-6 border-b border-white/10">
            <h3 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-[#FEFAE0]">
              Platform Artifact Repository
            </h3>
            <p className="text-sm sm:text-base text-white/60 max-w-2xl mt-2 leading-relaxed">
              Curated digital archive preserving the 26 production schematics, telemetry dashboards, Direct Lake reports, and Fabric Activator reflex rules. Select a folder to browse its documents.
            </p>
          </div>

          {/* Clean 4-Folder Collection (Spacious, closed at rest, no collisions) */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 lg:gap-x-16 gap-y-16 lg:gap-y-20 items-start justify-items-center w-full max-w-5xl mx-auto">
            {CATEGORIES.map((category) => {
              const folderFiles: FolderFile[] = category.items.slice(0, 4).map((it) => ({
                name: it.name,
                meta: it.meta,
                image: it.image,
              }));

              return (
                <div
                  key={category.id}
                  onClick={() => handleOpenFolder(category.id)}
                  className="group flex flex-col items-center cursor-pointer text-center select-none w-full max-w-sm"
                  role="button"
                  tabIndex={0}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                      e.preventDefault();
                      handleOpenFolder(category.id);
                    }
                  }}
                  aria-label={`Open ${category.label} collection, contains ${category.countLabel}`}
                >
                  {/* Folder Object — Closed at rest, tilts on hover */}
                  <div className="relative flex items-center justify-center pt-2 pb-2 transition-transform duration-300 group-hover:scale-[1.02]">
                    <GlassFolder
                      label={category.label}
                      meta={category.countLabel}
                      tone="dark"
                      art={category.art}
                      seed={category.seed}
                      width={310}
                      action="none"
                      labelPlacement="bottom-left"
                      files={folderFiles}
                      open={false}
                      className="pointer-events-none"
                    />
                  </div>

                  {/* Clean Label Group with Generous Spacing (44px explicit space from folder artwork) */}
                  <div
                    style={{ marginTop: "44px" }}
                    className="flex flex-col items-center max-w-xs text-center"
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-white/60 group-hover:text-[#FEFAE0] transition-colors">
                        {category.icon}
                      </span>
                      <h4 className="text-base sm:text-lg font-bold text-[#FEFAE0] tracking-tight group-hover:text-[#A3B872] transition-colors">
                        {category.label}
                      </h4>
                    </div>
                    <span className="text-xs text-white/50 mt-1 font-normal">
                      {category.countLabel}
                    </span>
                    <p className="text-xs text-white/55 mt-2 line-clamp-2 leading-relaxed">
                      {category.tagline}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        /* ── STATE 2: DEDICATED FOLDER-BROWSING VIEW ───────────────────────── */
        <div className="flex flex-col w-full animate-in fade-in duration-200">
          {/* Top Header & Return Action */}
          <div className="mb-10 pb-6 border-b border-white/10">
            <button
              type="button"
              onClick={handleReturnToRepo}
              className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/5 hover:bg-white/10 text-xs font-mono text-white/70 hover:text-white transition-colors mb-5 active:scale-95 border border-white/10 focus:outline-none focus-visible:ring-1 focus-visible:ring-white/40"
              aria-label="Return to Platform Repository"
            >
              <ArrowLeft size={14} />
              <span>← Return to all collections</span>
            </button>

            <div className="flex flex-col gap-4">
              <div className="flex items-center gap-2.5">
                <span className="p-2 rounded-xl bg-white/5 border border-white/10 text-[#FEFAE0]">
                  {selectedCategory.icon}
                </span>
                <div>
                  <div className="flex items-baseline gap-2">
                    <h3 className="text-2xl sm:text-3xl font-extrabold text-[#FEFAE0] tracking-tight">
                      {selectedCategory.label}
                    </h3>
                    <span className="text-xs font-mono text-[#A3B872]">
                      ({selectedCategory.countLabel})
                    </span>
                  </div>
                </div>
              </div>

              <p className="text-xs sm:text-sm text-white/65 max-w-2xl leading-relaxed">
                {selectedCategory.tagline}
              </p>

              {/* Quick collection switcher strip */}
              <div className="flex items-center gap-2 pt-2 flex-wrap">
                <span className="text-xs font-mono text-white/40 mr-1">Switch collection:</span>
                {CATEGORIES.map((cat) => (
                  <button
                    key={cat.id}
                    type="button"
                    onClick={() => setSelectedCategoryId(cat.id)}
                    className={`px-3 py-1 rounded-full text-xs font-mono transition-all active:scale-95 ${
                      cat.id === selectedCategory.id
                        ? "bg-[#A3B872]/20 border border-[#A3B872]/50 text-[#FEFAE0] font-semibold"
                        : "bg-white/5 border border-white/10 text-white/60 hover:text-white hover:bg-white/10"
                    }`}
                  >
                    {cat.label}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Dedicated Folder Content: Balanced side-by-side on desktop */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-14 items-start pt-6">
            {/* Left Column: Focused Folder Artwork with generous top headroom */}
            <div
              className="lg:col-span-5 flex flex-col items-center justify-start pb-10 px-4 rounded-2xl bg-white/[0.02]"
              style={{ paddingTop: "110px" }}
            >
              <div className="relative">
                <GlassFolder
                  key={selectedCategory.id}
                  label={selectedCategory.label}
                  meta={selectedCategory.countLabel}
                  tone="dark"
                  art={selectedCategory.art}
                  seed={selectedCategory.seed}
                  width={310}
                  action="none"
                  labelPlacement="bottom-left"
                  files={selectedCategory.items.map((it) => ({
                    name: it.name,
                    meta: it.meta,
                    image: it.image,
                  }))}
                  defaultOpen={true}
                  onFileSelect={(_, fileIdx) => {
                    handleOpenArtifact(selectedCategory, fileIdx);
                  }}
                />
              </div>
              <span className="text-[11px] font-mono text-white/40 mt-8 text-center">
                Click any sheet in the folder or select from the document list
              </span>
            </div>

            {/* Right Column: Clean, Readable Document List */}
            <div className="lg:col-span-7 flex flex-col">
              <div className="text-[11px] font-mono uppercase tracking-wider text-white/40 mb-3 px-2">
                Documents in collection ({selectedCategory.items.length})
              </div>
              <div className="flex flex-col divide-y divide-white/[0.06]">
                {selectedCategory.items.map((item, idx) => (
                  <button
                    key={item.id}
                    type="button"
                    onClick={(e) => handleOpenArtifact(selectedCategory, idx, e.currentTarget)}
                    className="group flex items-start justify-between gap-4 py-3.5 px-3 rounded-xl hover:bg-white/[0.04] transition-colors text-left focus:outline-none focus-visible:ring-1 focus-visible:ring-white/40"
                  >
                    <div className="flex items-start gap-3 min-w-0">
                      <span className="text-xs font-mono text-white/30 pt-0.5 shrink-0 group-hover:text-[#A3B872] transition-colors">
                        {String(idx + 1).padStart(2, "0")}
                      </span>
                      <div className="min-w-0">
                        <div className="text-sm font-semibold text-[#FEFAE0] group-hover:text-[#A3B872] transition-colors truncate">
                          {item.name}
                        </div>
                        <div className="text-xs text-white/55 mt-0.5 line-clamp-1">
                          {item.desc}
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 shrink-0 pt-0.5">
                      <span className="text-[11px] font-mono text-white/40 group-hover:text-white/70 transition-colors">
                        {item.meta}
                      </span>
                      <ExternalLink size={13} className="text-white/30 group-hover:text-white/80 transition-colors" />
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* ── STATE 3: IMMERSIVE FULL-SCREEN ARTIFACT INSPECTION ─────────────── */}
      {modalArtifact && currentArtifact && (
        <div
          role="dialog"
          aria-modal="true"
          aria-label={`Inspecting ${currentArtifact.name}`}
          className="fixed inset-0 z-[3000] flex flex-col items-center justify-between bg-black/94 backdrop-blur-2xl p-4 sm:p-6 animate-in fade-in zoom-in-[0.98] duration-200 select-none"
          onClick={handleCloseModal}
        >
          {/* Top Bar: Minimal Understated Context & Close Control */}
          <div
            className="w-full max-w-6xl flex items-center justify-between text-white/80 z-20 pb-2"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center gap-2.5 text-xs font-mono">
              <span className="font-semibold text-white/90">
                {modalArtifact.category.label}
              </span>
              <span className="text-white/30">•</span>
              <span className="text-white/50">
                {modalArtifact.itemIndex + 1} of {modalArtifact.category.items.length}
              </span>
            </div>

            <div className="flex items-center gap-3">
              <a
                href={currentArtifact.image}
                target="_blank"
                rel="noopener noreferrer"
                className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-white/10 hover:bg-white/15 text-xs text-white/80 transition-colors"
                title="Open high-resolution asset in new tab"
              >
                <span>Full Asset</span>
                <ExternalLink size={12} />
              </a>

              <button
                type="button"
                onClick={handleCloseModal}
                aria-label="Close inspection view"
                className="w-9 h-9 rounded-full bg-white/10 hover:bg-white/20 active:scale-95 text-white/80 hover:text-white flex items-center justify-center transition-all focus:outline-none focus-visible:ring-2 focus-visible:ring-white/50"
                title="Close (Escape)"
              >
                <X size={18} />
              </button>
            </div>
          </div>

          {/* Center Stage: The Artifact Itself is the Hero */}
          <div
            className="relative flex-1 w-full max-w-6xl flex items-center justify-center overflow-hidden my-2"
            onClick={(e) => e.stopPropagation()}
            onWheel={(e) => {
              e.preventDefault();
              if (e.deltaY < 0) {
                setZoomScale((s) => Math.min(3.5, Number((s + 0.25).toFixed(2))));
              } else {
                setZoomScale((s) => Math.max(0.6, Number((s - 0.25).toFixed(2))));
              }
            }}
          >
            {/* Previous Arrow */}
            <button
              type="button"
              onClick={handlePrevArtifact}
              aria-label="Previous artifact"
              className="absolute left-2 sm:left-4 z-20 w-11 h-11 rounded-full bg-black/60 hover:bg-black/85 border border-white/10 text-white/70 hover:text-white flex items-center justify-center backdrop-blur-md transition-all active:scale-95 shadow-xl focus:outline-none focus-visible:ring-2 focus-visible:ring-white/40"
              title="Previous (Left Arrow)"
            >
              <ChevronLeft size={22} />
            </button>

            {/* The Document Image */}
            <img
              src={currentArtifact.image}
              alt={currentArtifact.name}
              draggable={false}
              onPointerDown={handlePointerDown}
              onPointerMove={handlePointerMove}
              onPointerUp={handlePointerUp}
              onPointerCancel={handlePointerUp}
              style={{
                transform: `translate(${panPos.x}px, ${panPos.y}px) scale(${zoomScale})`,
                cursor: zoomScale > 1 ? (isPanning ? "grabbing" : "grab") : "default",
                transition: isPanning ? "none" : "transform 0.18s cubic-bezier(0.16, 1, 0.3, 1)",
                maxHeight: "78vh",
                maxWidth: "88vw",
                objectFit: "contain",
              }}
              className="rounded-xl shadow-[0_24px_80px_rgba(0,0,0,0.85)] border border-white/10"
            />

            {/* Next Arrow */}
            <button
              type="button"
              onClick={handleNextArtifact}
              aria-label="Next artifact"
              className="absolute right-2 sm:right-4 z-20 w-11 h-11 rounded-full bg-black/60 hover:bg-black/85 border border-white/10 text-white/70 hover:text-white flex items-center justify-center backdrop-blur-md transition-all active:scale-95 shadow-xl focus:outline-none focus-visible:ring-2 focus-visible:ring-white/40"
              title="Next (Right Arrow)"
            >
              <ChevronRight size={22} />
            </button>

            {/* Micro Zoom Controls Indicator (visible when zoomed) */}
            {zoomScale > 1 && (
              <div className="absolute bottom-3 left-4 flex items-center gap-1.5 bg-black/75 backdrop-blur-md px-3 py-1.5 rounded-full border border-white/15 text-[11px] font-mono text-white/70 shadow-lg">
                <button
                  type="button"
                  onClick={() => setZoomScale((s) => Math.max(0.6, s - 0.25))}
                  className="p-0.5 hover:text-white"
                  title="Zoom Out"
                >
                  <ZoomOut size={13} />
                </button>
                <span>{Math.round(zoomScale * 100)}%</span>
                <button
                  type="button"
                  onClick={() => setZoomScale((s) => Math.min(3.5, s + 0.25))}
                  className="p-0.5 hover:text-white"
                  title="Zoom In"
                >
                  <ZoomIn size={13} />
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setZoomScale(1);
                    setPanPos({ x: 0, y: 0 });
                  }}
                  className="p-0.5 hover:text-white ml-1 text-white/50"
                  title="Reset Zoom"
                >
                  <RotateCcw size={12} />
                </button>
              </div>
            )}
          </div>

          {/* Bottom Bar: Document Title, Meta, and Technical Context */}
          <div
            className="z-20 flex flex-col items-center text-center max-w-2xl px-5 py-2.5 rounded-2xl bg-black/60 backdrop-blur-md border border-white/10 shadow-xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex flex-wrap items-center justify-center gap-2 mb-0.5">
              <span className="text-sm sm:text-base font-bold text-[#FEFAE0]">
                {currentArtifact.name}
              </span>
              <span className="text-xs font-mono text-[#DDA15E] font-medium">
                • {currentArtifact.meta}
              </span>
            </div>
            <p className="text-xs text-white/70 leading-relaxed max-w-xl">
              {currentArtifact.desc}
            </p>
          </div>
        </div>
      )}
    </section>
  );
}
