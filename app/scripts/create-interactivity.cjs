const fs = require('fs');
const path = require('path');

const srcAppJsPath = path.resolve(__dirname, '../../site/app.js');
const outInteractivityPath = path.resolve(__dirname, '../src/originalSiteInteractivity.js');

let code = fs.readFileSync(srcAppJsPath, 'utf8');

// Replace document.addEventListener('DOMContentLoaded', () => { ... });
// with an exported function initOriginalSiteInteractivity()
const domContentRegex = /document\.addEventListener\('DOMContentLoaded',\s*\(\)\s*=>\s*\{([\s\S]*?)\}\);/;

code = code.replace(domContentRegex, (match, body) => {
  return `export function initOriginalSiteInteractivity() {
${body}
  return () => {
    // Cleanup if needed
  };
}
`;
});

fs.writeFileSync(outInteractivityPath, code, 'utf8');
console.log('Successfully created originalSiteInteractivity.js');
