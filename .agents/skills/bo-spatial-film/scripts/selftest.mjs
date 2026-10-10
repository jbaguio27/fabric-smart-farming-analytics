#!/usr/bin/env node
// End-to-end proof that bo-spatial-film works on this machine. Run after ANY edit to the skill.
// Usage: node <skill>/scripts/selftest.mjs [work dir]   (default: a fresh folder in the OS temp dir, kept for a look)
// Steps: new-film -> two scenes from the starter with a shared seam -> harness lint + snapshot -> assemble ->
//        hyperframes check -> seam-check (one seam + the loop) -> render (hardware GPU) -> ffprobe 60 fps -> web encode.
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const work = process.argv[2] || fs.mkdtempSync(path.join(os.tmpdir(), "bo-spatial-film-selftest-"));
const film = path.join(work, "film");
const PY = process.platform === "win32" ? "python" : "python3";
const results = [];
const check = (name, ok, detail = "") => results.push(`${ok ? "PASS" : "FAIL"}  ${name}${detail ? "  -- " + detail : ""}`);
// On Windows a bare "bash" can resolve to WSL - use Git Bash's bash.exe when it is there.
const gitBash = path.join(process.env.ProgramFiles || "C:\\Program Files", "Git", "bin", "bash.exe");
const BASH = process.platform === "win32" && fs.existsSync(gitBash) ? gitBash : "bash";
// npx is a .cmd shim on Windows, so it needs a shell; node, python and bash must not get one (paths with spaces)
const sh = (cmd, a, cwd = film) => spawnSync(cmd === "bash" ? BASH : cmd, a, { cwd, encoding: "utf8", maxBuffer: 1 << 28,
  shell: process.platform === "win32" && cmd === "npx" });
const tail = (r) => (r.error ? r.error.message : `${r.stdout || ""}${r.stderr || ""}`).trim().split("\n").slice(-6).join(" | ");
fs.mkdirSync(work, { recursive: true });

try {
  let r = sh(process.execPath, [path.join(here, "new-film.mjs"), film, "--name", "selftest"], work);
  check("new-film scaffolds the template", r.status === 0 && fs.existsSync(path.join(film, "film.json")), tail(r));

  const cfg = JSON.parse(fs.readFileSync(path.join(film, "film.json"), "utf8"));
  Object.assign(cfg, { scenes: [["s01-open", 2], ["s02-close", 2]], sfx: {}, cues: [] });
  delete cfg.bgm;
  fs.writeFileSync(path.join(film, "film.json"), JSON.stringify(cfg, null, 2));
  const dur = +(2 * 4 * 60 / cfg.bpm).toFixed(4);
  const starter = fs.readFileSync(path.join(film, "references", "scene-starter.html"), "utf8")
    .replace(/^<!--[\s\S]*?-->\s*/, "");
  for (const id of ["s01-open", "s02-close"])
    fs.writeFileSync(path.join(film, "compositions", `${id}.html`), starter.replaceAll("SCENE", id).replaceAll("DUR", String(dur)));

  r = sh(PY, [path.join(here, "make-harness.py")]);
  check("make-harness builds one test project per scene", r.status === 0, tail(r));
  r = sh("bash", [path.join(here, "test-scene.sh"), "s01-open", `0.5,${dur - 0.05}`]);
  const snaps = path.join(film, ".hyperframes", "test", "s01-open", "snaps");
  check("harness: scene lints with 0 errors and snapshots", /0 errors/.test(r.stdout) &&
    fs.existsSync(snaps) && fs.readdirSync(snaps).filter((f) => f.endsWith(".png")).length === 2, tail(r));

  r = sh(PY, [path.join(here, "assemble.py")]);
  check("assemble writes index.html from film.json", r.status === 0 && fs.existsSync(path.join(film, "index.html")), tail(r));
  r = sh("npx", ["--yes", `hyperframes@${cfg.hyperframes}`, "check"]);
  check("hyperframes check passes", r.status === 0 && /Check passed/.test(r.stdout + r.stderr), tail(r));
  r = sh(PY, [path.join(here, "seam-check.py")]);
  check("seam-check: seam + loop match by pixels", r.status === 0 && /2\/2 seams match/.test(r.stdout), tail(r));

  r = sh("bash", [path.join(here, "render-final.sh"), "selftest"]);
  const out = r.stdout + r.stderr;
  check("render on the hardware GPU path", r.status === 0 && /gpu mode: hardware/.test(out), tail(r));
  check("render is 1920x1080 at 60 fps", /width=1920/.test(out) && /height=1080/.test(out) && /r_frame_rate=60\/1/.test(out));

  const mp4 = path.join(film, "renders", "selftest.mp4");
  if (fs.existsSync(mp4)) {
    r = sh(process.execPath, [path.join(here, "encode-web.mjs"), mp4, path.join(film, "web"), "--name", "selftest", "--poster", "1", "--silent"]);
    check("web encode + poster", r.status === 0 && fs.existsSync(path.join(film, "web", "selftest-poster.jpg")), tail(r));
  }
} catch (e) {
  check("selftest ran without throwing", false, e.message);
}
console.log(results.join("\n"));
const failed = results.filter((l) => l.startsWith("FAIL")).length;
console.log(failed ? `FAIL (${failed})  work dir: ${work}` : `PASS  work dir: ${work}`);
process.exit(failed ? 1 : 0);
