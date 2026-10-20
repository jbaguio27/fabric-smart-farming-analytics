const fs = require('fs');
const html = fs.readFileSync('../site/index.html', 'utf8');
const lines = html.split('\n').slice(442, 2160).join('\n');
const styles = [...lines.matchAll(/style="([^"]*)"/g)].map(m => m[1]);
console.log('Unique inline styles found:', Array.from(new Set(styles)));
