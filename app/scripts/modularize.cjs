const fs = require('fs');
const path = require('path');

const srcFile = path.resolve(__dirname, '../src/components/OriginalSections.jsx');
// We need to read from the original content or rebuild from lines
// Let's read from the sections directory or the backup if needed
// Actually, let's read the full OriginalSections from site/index.html via convert-sections, or read the sections
const sectionsDir = path.resolve(__dirname, '../src/components/sections');

function extractCleanSection(filePath, startTag, endTag) {
  let content = fs.readFileSync(filePath, 'utf8');
  const sIdx = content.indexOf(startTag);
  if (sIdx === -1) {
    console.error(`Could not find startTag ${startTag} in ${filePath}`);
    return;
  }
  const eIdx = content.lastIndexOf(endTag);
  if (eIdx === -1) {
    console.error(`Could not find endTag ${endTag} in ${filePath}`);
    return;
  }
  const sectionContent = content.slice(sIdx, eIdx + endTag.length);
  return sectionContent;
}

// 1. ProblemSection
const problemBody = extractCleanSection(path.join(sectionsDir, 'ProblemSection.jsx'), '<section id="problem"', '</section>');
fs.writeFileSync(path.join(sectionsDir, 'ProblemSection.jsx'), `import React from 'react';
import PhysicalProblemCarousel from '../PhysicalProblemCarousel';

export default function ProblemSection() {
  return (
    ${problemBody}
  );
}
`, 'utf8');

// 2. SimulatorSection
const simBody = extractCleanSection(path.join(sectionsDir, 'SimulatorSection.jsx'), '<section id="build"', '</section>');
fs.writeFileSync(path.join(sectionsDir, 'SimulatorSection.jsx'), `import React from 'react';

export default function SimulatorSection() {
  return (
    ${simBody}
  );
}
`, 'utf8');

// 3. PlatformSection
const platBody = extractCleanSection(path.join(sectionsDir, 'PlatformSection.jsx'), '<section id="platform"', '</section>');
fs.writeFileSync(path.join(sectionsDir, 'PlatformSection.jsx'), `import React from 'react';

export default function PlatformSection() {
  return (
    ${platBody}
  );
}
`, 'utf8');

// 4. ResultsSection
const resBody = extractCleanSection(path.join(sectionsDir, 'ResultsSection.jsx'), '<section id="results"', '</section>');
fs.writeFileSync(path.join(sectionsDir, 'ResultsSection.jsx'), `import React from 'react';

export default function ResultsSection() {
  return (
    ${resBody}
  );
}
`, 'utf8');

// 5. ExploreSection
const expBody = extractCleanSection(path.join(sectionsDir, 'ExploreSection.jsx'), '<section id="explore"', '</section>');
fs.writeFileSync(path.join(sectionsDir, 'ExploreSection.jsx'), `import React from 'react';

export default function ExploreSection() {
  return (
    ${expBody}
  );
}
`, 'utf8');

// 6. NotesSection and AuthorSection
const notesFull = fs.readFileSync(path.join(sectionsDir, 'NotesSection.jsx'), 'utf8');
const notesStart = notesFull.indexOf('<section id="notes"');
const notesEnd = notesFull.indexOf('</section>', notesStart) + '</section>'.length;
const notesBody = notesFull.slice(notesStart, notesEnd);

const authorStart = notesFull.indexOf('<section id="author"');
const authorEnd = notesFull.indexOf('</section>', authorStart) + '</section>'.length;
const authorBody = notesFull.slice(authorStart, authorEnd);

fs.writeFileSync(path.join(sectionsDir, 'NotesSection.jsx'), `import React from 'react';

export default function NotesSection() {
  return (
    ${notesBody}
  );
}
`, 'utf8');

fs.writeFileSync(path.join(sectionsDir, 'AuthorSection.jsx'), `import React from 'react';

export default function AuthorSection() {
  return (
    ${authorBody}
  );
}
`, 'utf8');

console.log('Cleaned and extracted all 7 modular sections including AuthorSection!');
