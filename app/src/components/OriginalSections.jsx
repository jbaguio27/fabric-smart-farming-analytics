import React from 'react';
import OriginSection from './sections/OriginSection';
import ProblemSection from './sections/ProblemSection';
import SimulatorSection from './sections/SimulatorSection';
import PlatformSection from './sections/PlatformSection';
import ResultsSection from './sections/ResultsSection';
import ExploreSection from './sections/ExploreSection';
import ArtifactsSection from './sections/ArtifactsSection';
import NotesSection from './sections/NotesSection';
import AuthorSection from './sections/AuthorSection';

export default function OriginalSections() {
  return (
    <>
      <OriginSection />
      <ProblemSection />
      <SimulatorSection />
      <PlatformSection />
      <ResultsSection />
      <ExploreSection />
      <ArtifactsSection />
      <NotesSection />
      <AuthorSection />
    </>
  );
}
