// Parses every ```mermaid block in the repository against the real Mermaid parser.
// Exists because docs/ARCHITECTURE.md shipped a diagram that silently failed to render:
// an unquoted "()" inside a [] node label. A human reading the diff cannot catch that.
import { JSDOM } from 'jsdom';
import fs from 'fs';
import path from 'path';

const dom = new JSDOM('<!DOCTYPE html><body></body>', { pretendToBeVisual: true });
global.window = dom.window;
global.document = dom.window.document;
global.HTMLElement = dom.window.HTMLElement;
Object.defineProperty(globalThis, 'navigator', { value: dom.window.navigator, configurable: true });

const mermaid = (await import('mermaid')).default;
mermaid.initialize({ startOnLoad: false, securityLevel: 'strict' });

const SKIP = new Set(['.git', 'node_modules', '.venv', '_site', '.ipynb_checkpoints']);
const files = [];
(function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (SKIP.has(entry.name)) continue;
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(p);
    else if (/\.(md|mmd)$/.test(entry.name)) files.push(p);
  }
})(process.argv[2] || '.');

let bad = 0, total = 0;
for (const file of files) {
  const src = fs.readFileSync(file, 'utf8');
  const blocks = file.endsWith('.mmd')
    ? [[src, 1]]
    : [...src.matchAll(/```mermaid\n([\s\S]*?)```/g)]
        .map(m => [m[1], src.slice(0, m.index).split('\n').length]);
  for (const [code, line] of blocks) {
    total++;
    try {
      await mermaid.parse(code);
    } catch (err) {
      bad++;
      const msg = String(err.message || err).split('\n').filter(Boolean)[0];
      console.error(`FAIL ${file}:${line}\n     ${msg}`);
    }
  }
}
console.log(`${total - bad}/${total} mermaid blocks parse`);
process.exit(bad ? 1 : 0);
