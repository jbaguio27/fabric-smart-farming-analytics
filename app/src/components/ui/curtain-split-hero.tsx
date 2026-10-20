"use client";

import {
    motion,
    useTransform,
    useReducedMotion,
    useMotionValue,
    useSpring,
    useMotionValueEvent,
    MotionValue,
} from "framer-motion";
import { useEffect, useRef, useState } from "react";
import { ArrowUpRight, ExternalLink, Sparkles } from "lucide-react";

// Grounded agricultural photography and architecture diagrams (100% verified local assets)
const IMAGES = [
    { src: "/assets/images/hero-greenhouse-bg.jpg", alt: "Benguet Highland Strawberry Canopy (1,500m elevation)" },
    { src: "/assets/images/farm-greenhouse-controls.jpg", alt: "Facility IoT Dosing & Whiteboard Logs" },
    { src: "/assets/images/farm-origin-inspection.jpg", alt: "Field Sensor Inspection & Canopy Probes" },
    { src: "/assets/diagrams/streaming-architecture.png", alt: "Microsoft Fabric Eventstream & KQL Architecture" },
    { src: "/assets/diagrams/medallion-architecture.png", alt: "OneLake Medallion Lakehouse Flow" },
    { src: "/assets/diagrams/microsoft-fabric-solution-architecture.png", alt: "End-to-End Enterprise Solution Topology" },
    { src: "/assets/diagrams/gold_star_schema_erd.png", alt: "Kimball Dimensional Star Schema ERD" },
    { src: "/assets/diagrams/batch-architecture.png", alt: "Scheduled Batch Ingestion Pipeline" },
];

const SPRING_CONFIG = { stiffness: 80, damping: 24, mass: 0.6 };

interface StageDimensions {
    width: number;
    height: number;
    isMobile: boolean;
}

interface CurtainCardProps {
    item: { src: string; alt: string };
    index: number;
    total: number;
    progress: MotionValue<number>;
    pointer: { x: MotionValue<number>; y: MotionValue<number> };
    isSpreadActive: boolean;
    stage: StageDimensions;
}

function CurtainCard({
    item,
    index,
    total,
    progress,
    pointer,
    isSpreadActive,
    stage,
}: CurtainCardProps) {
    const half = total / 2;
    const isLeft = index % 2 === 0;
    const wingIndex = Math.floor(index / 2); // 0 to 3
    const norm = wingIndex / (half - 1) - 0.5; // -0.5 to 0.5
    const sideMult = isLeft ? -1 : 1;

    const cardWidth = stage.isMobile ? 64 : 115;
    const cardHeight = stage.isMobile ? 86 : 155;

    // Curved parabolic wing coordinates
    const archCurve = Math.cos(norm * Math.PI) * (stage.width * 0.03);
    const targetX = sideMult * (stage.width * (stage.isMobile ? 0.42 : 0.38) + archCurve);
    const targetY = norm * (stage.height * 0.65);
    const targetRotate = sideMult * (norm * 16);

    const initialX = sideMult * (wingIndex * 6);
    const initialY = norm * 12;
    const initialRotate = sideMult * (wingIndex * 2);

    const translate = useTransform(
        [progress, pointer.x, pointer.y],
        ([p, px, py]: number[]) => {
            const easeP = 1 - Math.pow(1 - p, 3);
            const tx = initialX + (targetX - initialX) * easeP;
            const ty = initialY + (targetY - initialY) * easeP;

            const maxParallaxX = stage.isMobile ? 6 : 14;
            const maxParallaxY = stage.isMobile ? 4 : 10;

            const dx = tx + px * (isLeft ? -maxParallaxX : maxParallaxX) * easeP;
            const dy = ty + py * maxParallaxY * easeP;

            return `calc(-50% + ${dx}px) calc(-50% + ${dy}px)`;
        }
    );

    const rotate = useTransform(
        progress,
        [0, 0.45, 1],
        [initialRotate, isLeft ? -12 : 12, targetRotate]
    );

    const scale = useTransform(progress, [0, 0.5, 1], [0.92, 0.98, 1]);

    return (
        <motion.div
            className="absolute left-1/2 top-1/2 will-change-transform cursor-pointer select-none"
            style={{
                width: cardWidth,
                height: cardHeight,
                zIndex: isLeft ? index + 1 : total - index,
                translate,
                rotate,
                scale,
            }}
            whileHover={
                isSpreadActive
                    ? {
                        scale: 1.08,
                        zIndex: 50,
                        rotate: 0,
                        transition: SPRING_CONFIG,
                    }
                    : { scale: 0.98 }
            }
            whileTap={{ scale: 1.04, zIndex: 50 }}
        >
            <div className="relative h-full w-full overflow-hidden rounded-xl bg-[#12190E] shadow-2xl ring-1 ring-white/15 transition-all duration-300 hover:ring-[#BC6C25]/60">
                <img
                    src={item.src}
                    alt={item.alt}
                    draggable={false}
                    className="h-full w-full object-cover transition-transform duration-700 ease-out hover:scale-108"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/50 via-transparent to-white/10 pointer-events-none" />
            </div>
        </motion.div>
    );
}

export default function CurtainSplitHero() {
    const stageRef = useRef<HTMLDivElement>(null);
    const reduce = useReducedMotion();

    const [stage, setStage] = useState<StageDimensions>({
        width: 1100,
        height: 600,
        isMobile: false,
    });

    // Starts parted and unveiled by default so content is instantly readable
    const rawProgress = useMotionValue(1);
    const progress = useSpring(rawProgress, SPRING_CONFIG);

    const [isSpreadActive, setIsSpreadActive] = useState(true);
    useMotionValueEvent(progress, "change", (p) => setIsSpreadActive(p > 0.4));

    // Pointer parallax
    const rawX = useMotionValue(0);
    const rawY = useMotionValue(0);
    const pointerX = useSpring(rawX, SPRING_CONFIG);
    const pointerY = useSpring(rawY, SPRING_CONFIG);

    useEffect(() => {
        const el = stageRef.current;
        if (!el) return;

        const updateDimensions = () => {
            const rect = el.getBoundingClientRect();
            setStage({
                width: rect.width,
                height: rect.height,
                isMobile: rect.width < 768,
            });
        };

        updateDimensions();
        const observer = new ResizeObserver(updateDimensions);
        observer.observe(el);
        return () => observer.disconnect();
    }, []);

    const handlePointerMove = (e: React.PointerEvent<HTMLDivElement>) => {
        if (reduce) return;
        const rect = e.currentTarget.getBoundingClientRect();
        rawX.set(((e.clientX - rect.left) / rect.width - 0.5) * 2);
        rawY.set(((e.clientY - rect.top) / rect.height - 0.5) * 2);
    };

    const handlePointerLeave = () => {
        rawX.set(0);
        rawY.set(0);
    };

    const toggleCurtain = () => {
        rawProgress.set(rawProgress.get() > 0.5 ? 0 : 1);
    };

    return (
        <section className="relative w-full flex flex-col items-center justify-center my-6">
            <div
                ref={stageRef}
                onPointerMove={handlePointerMove}
                onPointerLeave={handlePointerLeave}
                className="relative h-[560px] sm:h-[620px] md:h-[680px] w-full overflow-hidden rounded-2xl sm:rounded-3xl bg-[#080B07] text-[#FEFAE0] border border-white/10 shadow-2xl flex items-center justify-center transition-colors duration-300"
            >
                {/* Subtle Botanical / Atmospheric Pattern */}
                <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(rgba(104,121,65,0.18)_1px,transparent_1px)] [background-size:28px_28px] [mask-image:radial-gradient(ellipse_75%_75%_at_50%_50%,#000_50%,transparent_100%)] opacity-80" />

                {/* Center Editorial Headline */}
                <div className="z-[5] flex flex-col items-center text-center px-4 max-w-sm sm:max-w-2xl">
                    <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-[#283618]/60 border border-[#606C38]/30 text-[10px] sm:text-[11px] font-sans font-medium tracking-wide text-[#606C38] backdrop-blur-md mb-3 sm:mb-4 shadow-sm">
                        <Sparkles size={12} className="text-[#DDA15E]" />
                        <span>Microsoft Fabric Platform Architecture · 8 Facilities · 80 IoT Zones</span>
                    </span>
                    <h1 className="text-2xl sm:text-4xl md:text-5xl font-extrabold tracking-tight leading-[1.10] text-[#FEFAE0] drop-shadow-md">
                        Real-time farm telemetry,
                        <br />
                        orchestrated into OneLake intelligence.
                    </h1>
                    <div className="my-3 sm:my-4 h-px w-20 sm:w-28 bg-[#BC6C25] origin-center" />
                    <p className="max-w-[54ch] text-xs sm:text-sm font-normal text-white/80 leading-relaxed mb-5 bg-black/40 backdrop-blur-md p-3 sm:p-4 rounded-xl border border-white/10">
                        An enterprise data platform proof of concept engineered natively on Microsoft Fabric—demonstrating 
                        real-time streaming ingestion, medallion lakehouse architecture, Kimball dimensional modeling, 
                        automated dead-letter queue remediation, and sub-second Power BI Direct Lake analytics.
                    </p>

                    {/* Architecture Navigation Actions */}
                    <div className="flex items-center gap-3 flex-wrap justify-center">
                        <a
                            href="#platform"
                            className="inline-flex items-center gap-1.5 px-5 py-2.5 rounded-full bg-[#BC6C25] hover:bg-[#a35c1d] text-[#FEFAE0] text-xs font-bold shadow-lg transition-transform active:scale-95"
                        >
                            <span>Explore Architecture</span>
                            <ArrowUpRight size={13} />
                        </a>
                        <button
                            type="button"
                            onClick={toggleCurtain}
                            className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-full bg-white/10 hover:bg-white/15 text-[#FEFAE0] text-xs font-semibold backdrop-blur-md border border-white/15 transition-transform active:scale-95"
                        >
                            <span>{isSpreadActive ? "Close Curtain" : "Part Wings"}</span>
                        </button>
                        <a
                            href="https://github.com/jbaguio27/fabric-smart-farming-analytics"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-full bg-white/5 hover:bg-white/10 text-white/80 text-xs font-medium border border-white/10 transition-colors"
                        >
                            <span>GitHub</span>
                            <ExternalLink size={12} />
                        </a>
                    </div>
                </div>

                {/* Bilateral Curtain Cards */}
                <div className="absolute inset-0 z-10 pointer-events-auto">
                    {IMAGES.map((item, i) => (
                        <CurtainCard
                            key={i}
                            item={item}
                            index={i}
                            total={IMAGES.length}
                            progress={progress}
                            pointer={{ x: pointerX, y: pointerY }}
                            isSpreadActive={isSpreadActive}
                            stage={stage}
                        />
                    ))}
                </div>

                {/* Bottom Status Pill Indicator */}
                <div className="pointer-events-none absolute bottom-4 z-30 flex items-center gap-2 rounded-full bg-black/60 backdrop-blur-md px-4 py-1.5 border border-white/10 text-[11px] font-medium text-white/80">
                    <span
                        className={`h-2 w-2 rounded-full transition-colors duration-300 ${
                            isSpreadActive ? "bg-emerald-500 shadow-[0_0_8px_#22c55e]" : "bg-amber-500"
                        }`}
                    />
                    <span>{isSpreadActive ? "Curtain parted · Hover cards to inspect" : "Curtain closed · Tap button to unveil"}</span>
                </div>
            </div>
        </section>
    );
}
