const fs = require('fs');
const path = require('path');

const targetPath = path.resolve(__dirname, '../src/components/OriginalSections.jsx');
let content = fs.readFileSync(targetPath, 'utf8');

content = content.replace(/poster="assets\//g, 'poster="/assets/');
content = content.replace(/href="assets\//g, 'href="/assets/');

fs.writeFileSync(targetPath, content, 'utf8');
console.log('Fixed poster and href attributes');
