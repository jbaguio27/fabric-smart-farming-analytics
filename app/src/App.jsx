import React, { useEffect } from 'react';
import DemoOne from '@/components/ui/demo';
import OriginalSections from '@/components/OriginalSections';
import OriginalFooter from '@/components/OriginalFooter';
import { initOriginalSiteInteractivity } from './originalSiteInteractivity';
import './App.css';

export default function App() {
  // Initialize original interactive handlers (KQL drawers, before/after slider, walkthrough theater, lightbox)
  useEffect(() => {
    const timer = setTimeout(() => {
      initOriginalSiteInteractivity();
    }, 50);
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="portfolio-root">
      <main>
        {/* Full Light Editorial Hero Section (#FEFAE0 Cream Background) */}
        <section id="hero" className="w-full bg-[#FEFAE0] border-b border-[#606C38]/25 py-8 sm:py-12 lg:py-16">
          <div className="w-full max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <DemoOne />
          </div>
        </section>

        {/* Existing Narrative & Interactive Chapters */}
        <OriginalSections />
      </main>

      <OriginalFooter />
    </div>
  );
}
