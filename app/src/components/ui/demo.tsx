// This is a file with a demo for your component
// That's what users will see in the preview
// Create new files in this directory to add more demos

import { ImageStreamHero } from "@/components/ui/image-stream-hero";

// Farm-related photography only (no software diagrams, no author portraits)
const IMAGES = [
  { src: "/assets/images/farm-vertical-towers.jpg", alt: "Vertical hydroponic growing towers" },
  { src: "/assets/images/hero-greenhouse-bg.jpg", alt: "Highland strawberry greenhouse canopy" },
  { src: "/assets/images/farm-nft-channels.jpg", alt: "NFT nutrient film growing channels" },
  { src: "/assets/images/images (1).jpg", alt: "Hydroponic leafy lettuce harvesting" },
  { src: "/assets/images/farm-greenhouse-controls.jpg", alt: "Greenhouse environmental controls and logs" },
  { src: "/assets/images/pexels-bulat843-1243575272-37861016.jpg", alt: "Vertical farming tiers with LED grow lighting" },
  { src: "/assets/images/farm-crop-canopy.jpg", alt: "Lush crop canopy growth" },
  { src: "/assets/images/images (2).jpg", alt: "Germination nursery seedling plugs" },
  { src: "/assets/images/farm-tunnel-structure.png", alt: "High-tunnel greenhouse structural framework" },
  { src: "/assets/images/images (3).jpg", alt: "Greenhouse hydroponic irrigation lines" },
  { src: "/assets/images/farm-tunnel-exterior.png", alt: "Commercial greenhouse tunnel exterior" },
  { src: "/assets/images/images.jpg", alt: "Hydroponic floating raft cultivation system" },
  { src: "/assets/images/istockphoto-1447011226-612x612.jpg", alt: "Automated greenhouse robotic lettuce inspection" },
];

// Inline colours: the legacy global `a { color }` rule outranks Tailwind
// text utilities, which is what blanked out the old buttons.
const linkBase =
  "inline-flex items-center gap-1.5 rounded-full px-3.5 py-1.5 text-xs sm:text-[12.5px] font-medium leading-none tracking-wide transition-all duration-150 hover:opacity-90 active:scale-95";

// ONLY DEFAULT EXPORT WILL BE TREATED AS A DEMO
export default function DemoOne() {
  return (
    <ImageStreamHero
      images={IMAGES}
      cards={IMAGES.length}
      speed={24}
      respectReducedMotion={false}
      axis={50}
      className="h-[620px] sm:h-[680px] lg:h-[760px] xl:h-[800px] w-full rounded-2xl sm:rounded-3xl border border-[#606C38]/25 bg-[#FEFAE0] shadow-[0_20px_50px_rgba(40,54,24,0.12)]"
    >
      <div className="relative z-10 flex h-full flex-col items-center justify-between py-12 sm:py-16 lg:py-20 text-center">
        <div className="px-6">
          <h1 className="text-balance text-4xl font-extrabold tracking-tight text-[#283618] sm:text-5xl md:text-6xl lg:text-[3.85rem] xl:text-[4.25rem] leading-[1.06]">
            Smart Farming Telemetry,
            <br />
            Live in Microsoft Fabric.
          </h1>
        </div>

        <div className="flex flex-col items-center gap-4 px-6">
          <p className="max-w-xl text-balance text-sm sm:text-base lg:text-lg text-[#283618]/85 font-medium leading-relaxed">
            An end-to-end telemetry platform streaming IoT sensor data from 8 facilities
            and 80 commercial hydroponic zones into Microsoft Fabric for sub-second
            analytics and automated anomaly alerts.
          </p>
          <div className="flex flex-wrap items-center justify-center gap-2.5">
            <a
              href="#platform"
              className={linkBase}
              style={{ backgroundColor: "#BC6C25", color: "#FEFAE0" }}
            >
              Explore Architecture →
            </a>
            <a
              href="#origin"
              className={`${linkBase} border`}
              style={{ backgroundColor: "rgba(40, 54, 24, 0.08)", color: "#283618", borderColor: "rgba(40, 54, 24, 0.25)" }}
            >
              Read the Story
            </a>
            <a
              href="https://github.com/jbaguio27/fabric-smart-farming-analytics"
              target="_blank"
              rel="noopener noreferrer"
              className={`${linkBase} border`}
              style={{ backgroundColor: "rgba(40, 54, 24, 0.08)", color: "#283618", borderColor: "rgba(40, 54, 24, 0.25)" }}
            >
              GitHub ↗
            </a>
          </div>
        </div>
      </div>
    </ImageStreamHero>
  );
}
