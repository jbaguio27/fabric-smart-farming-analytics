import React from 'react';
import FeaturesAlternating from '../ui/features-alternating';

export default function ExploreSection() {
  return (
    <section id="explore" className="section">
      <div className="container">
        <div className="section-eyebrow">EXPLORE THE SYSTEM</div>
        <p className="section-lead">
          From edge IoT sensor noise to trusted operational clarity: examine how Microsoft Fabric intercepts corrupted packets, self-heals schema drift, and delivers sub-second Direct Lake intelligence across a unified OneLake architecture.
        </p>

        {/* Alternating Rows With Stats Component */}
        <FeaturesAlternating />
      </div>
    </section>
  );
}
