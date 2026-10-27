// Reproducible conversion of the reviewed, pure TypeScript geometry only.
// No upstream package scripts, dependency installation, or arbitrary code execution.
import { readFile, writeFile } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { stripTypeScriptTypes } from 'node:module';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const source = path.join(here, 'vendor-src');
const chosen = ['presets.ts', ...['braid','core','index','lattice','morph','orbits','profiles','registry','ribbon','types','web'].map(x => `engine/${x}.ts`)];
const hash = s => createHash('sha256').update(s).digest('hex');
const manifest = {};
for (const rel of chosen) {
  const input = await readFile(path.join(source, 'src', rel));
  let output = stripTypeScriptTypes(input.toString('utf8'), { mode: 'strip' });
  output = output.replace(/(from\s*['"])(\.{1,2}\/[^'"]+)(['"])/g, (_m, a, b, c) => `${a}${b}.mjs${c}`);
  const outRel = rel.replace(/\.ts$/, '.mjs');
  await writeFile(path.join(here, outRel), output);
  manifest[`src/${rel}`] = { sha256: hash(input), output: outRel, outputSha256: hash(output) };
}
await writeFile(path.join(here, 'input-output-sha256.json'), JSON.stringify(manifest, null, 2) + '\n');
