import React from 'react';
import { CardHandGallery } from '@/components/ui/card-hand-gallery';

const STORY_CARDS = [
  {
    id: "the-problem",
    src: "/assets/images/farm-origin-inspection.jpg",
    title: "The data was all over the place.",
    description:
      "I started with a simple question. How do you keep track of eight growing facilities when sensor readings, farm records, and operational data live in different places? I wanted to see what it would take to bring those pieces together.",
  },
  {
    id: "the-idea",
    src: "/assets/images/farm-greenhouse-controls.jpg",
    title: "I wanted data that actually moves.",
    description:
      "I didn't want another demo that loads a static file and calls it a pipeline. I built a Python simulator to generate farm telemetry and send events into Microsoft Fabric, so I could work with data as it arrives.",
  },
  {
    id: "the-pipeline",
    src: "/assets/images/streaming-architecture.png",
    title: "Not every event should get through.",
    description:
      "I routed incoming events across eight facilities and gave invalid or deprecated events their own dead letter path. The goal was simple. Make it clear where the data goes, and make failures visible instead of letting them disappear.",
  },
  {
    id: "the-data",
    src: "/assets/images/medallion-architecture.png",
    title: "From raw readings to useful data.",
    fit: "contain",
    description:
      "I used Eventhouse and KQL for event analysis, then organized historical data into Bronze, Silver, and Gold layers. Each stage has a purpose, from preserving what arrived to preparing data for reporting.",
  },
  {
    id: "the-outcome",
    src: "/assets/images/page_1_executive_operations.png",
    title: "Numbers are useful when someone can act on them.",
    fit: "cover",
    description:
      "I connected the engineering work to farm monitoring and operational reporting. The idea is to help people spot unusual conditions, understand what's happening, and know when something needs a closer look.",
  },
  {
    id: "the-takeaway",
    src: "/assets/images/microsoft-fabric-solution-architecture.png",
    title: "I built this to solve the whole problem.",
    fit: "cover",
    description:
      "This is an independent proof of concept, not a live farm deployment. I built it to explore ingestion, event routing, data quality, historical modeling, and monitoring in one project. For me, the interesting part is how all those pieces work together.",
  },
];

export default function OriginSection() {
  return (
    <section id="origin" className="section py-16 sm:py-24 lg:py-32">
      <div className="origin-expanded-container w-full max-w-7xl xl:max-w-[1440px] 2xl:max-w-[1560px] mx-auto px-4 sm:px-6 lg:px-8 xl:px-12">
        {/* Section Header */}
        <div className="section-header text-center mb-12 sm:mb-16 lg:mb-20">
          <h2 className="section-title text-4xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-[4.75rem] font-extrabold tracking-tight text-[#FEFAE0] leading-[1.05]">
            Why I Built This
          </h2>
          <p className="section-lead max-w-4xl mx-auto text-[#FEFAE0]/85 text-lg sm:text-xl lg:text-2xl xl:text-[1.5rem] mt-6 leading-relaxed font-normal">
            From observing fragmented farm records on-site to engineering an end-to-end streaming intelligence platform in Microsoft Fabric.
          </p>
        </div>

        {/* Scaled Center Image Showcase & Hand Gallery */}
        <div className="my-8 sm:my-12 flex justify-center w-full">
          <CardHandGallery
            cards={STORY_CARDS}
            cardWidth={740}
            defaultActiveId="the-outcome"
            className="w-full"
          />
        </div>

        {/* Enriched & Enlarged Bottom Disclosure Box */}
        <div className="nda-callout-expanded w-full max-w-5xl xl:max-w-6xl 2xl:max-w-7xl mx-auto mt-16 sm:mt-24 p-6 sm:p-8 lg:p-10 xl:p-12 rounded-2xl sm:rounded-3xl border border-[#DDA15E]/30 bg-[#141C0D]/95 backdrop-blur-xl shadow-2xl relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1.5 h-full bg-[#DDA15E]" />
          <div className="flex items-center gap-3 text-xs sm:text-sm lg:text-base xl:text-lg font-bold uppercase tracking-wider text-[#DDA15E]">
            <svg
              className="w-5 h-5 sm:w-6 sm:h-6 text-[#DDA15E] shrink-0"
              fill="none"
              viewBox="0 0 24 24"
              strokeWidth="2"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"
              />
            </svg>
            <span>Independent Proof of Concept • Synthetic Data Foundation</span>
          </div>
          <p className="mt-4 text-base sm:text-lg lg:text-xl xl:text-[1.15rem] text-[#FEFAE0]/85 leading-relaxed font-normal">
            <strong className="text-[#FEFAE0] font-semibold">Important Distinction:</strong> This platform is an independent technical proof of concept inspired by real operational observations—it was not deployed at the local farm, nor was it formally commissioned or approved by them. All telemetry, facility counts, equipment readings, and sensor streams are synthetically generated using Python to demonstrate architectural design without proprietary dependencies.
          </p>
        </div>
      </div>
    </section>
  );
}
