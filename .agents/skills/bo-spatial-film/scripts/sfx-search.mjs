// Searches the HeyGen sound-effects catalog and downloads the top hit per query.
// Usage: node <skill>/scripts/sfx-search.mjs "<name>=<query>" ["<name>=<query>" ...]   -> assets/audio/sfx/<name>.mp3
import { mkdirSync } from 'node:fs';
import { join } from 'node:path';
// media-use's vendored REST helper reads ~/.heygen/credentials (written by `npx hyperframes auth login`);
// no heygen CLI needed, so this works on Windows. media-use sits beside this skill in ~/.claude/skills/.
const { heygenAuthHeaders, searchSounds, downloadTo } = await import(
  new URL('../../media-use/audio/scripts/lib/heygen.mjs', import.meta.url).href);

const headers = heygenAuthHeaders();
if (!headers) { console.error('no HeyGen credential'); process.exit(1); }
const out = join(process.cwd(), 'assets', 'audio', 'sfx');
mkdirSync(out, { recursive: true });
for (const arg of process.argv.slice(2)) {
  const [name, query] = arg.split('=');
  const res = await searchSounds(query, 'sound_effects', headers, { limit: 3 });
  res.forEach((r, i) => console.log(`${name} #${i + 1} ${r.duration}s ${r.description || r.name}`));
  if (res[0]?.audio_url) {
    await downloadTo(res[0].audio_url, join(out, `${name}.mp3`));
    console.log('  saved', name);
  }
}
