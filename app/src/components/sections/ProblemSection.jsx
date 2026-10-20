import React from 'react';
import PhysicalProblemCarousel from '../PhysicalProblemCarousel';

export default function ProblemSection() {
  return (
    <section id="problem" className="section section-quiet">
      <div className="container">
        <h2 className="section-title">The Physical Problem</h2>
        <p className="section-lead">
          In farming environments, biological health depends on continuous environmental stability. During my exposure to the local farm, I observed how physical variables—microclimate drift, nutrient balance, and equipment wear—were tracked across manual records and isolated systems. In this proof of concept, those challenges are modeled into core operational failure scenarios:
        </p>

        {/* 21st.dev Hanging Polaroid Image Carousel & Diagnostic Telemetry */}
        <PhysicalProblemCarousel />

        {/* Problem Context & Engineering Question Row */}
        <div className="problem-context-row">
          <div className="engineering-question-card">
            <div className="engineering-question-tag">The Core Engineering Question</div>
            <div className="engineering-question-text">
              How do you build a data platform that can observe thousands of sensor streams continuously, detect anomalies within seconds, protect downstream analytical models from malformed packets, and provide clean business reporting—all within a single unified architecture?
            </div>
          </div>

          <div className="photo-card">
            <img 
              src="/assets/images/farm-greenhouse-controls.jpg" 
              alt="Hydroponic greenhouse with manual irrigation controls, EC/pH monitoring log whiteboard, and tiered growing tables" 
              className="photo-image"
              loading="lazy"
             />
            <div className="photo-caption">Observed environment: Manual logging whiteboard (pH/EC levels and watering intervals) alongside pump control panels in the greenhouse facility, illustrating the fragmented, manual records that inspired this modernization proof of concept.</div>
          </div>
        </div>
      </div>
    </section>
  );
}
