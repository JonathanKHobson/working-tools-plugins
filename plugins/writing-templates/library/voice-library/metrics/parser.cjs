'use strict';

const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { pathToFileURL } = require('node:url');
const { MARKED_VERSION } = require('./constants.cjs');

function inspectPackage(target) {
  const resolved = fs.realpathSync(path.resolve(target));
  let packageDir = fs.statSync(resolved).isDirectory() ? resolved : path.dirname(resolved);
  let manifest;
  while (true) {
    const file = path.join(packageDir, 'package.json');
    if (fs.existsSync(file)) {
      const candidate = JSON.parse(fs.readFileSync(file, 'utf8'));
      if (candidate.name === 'marked') { manifest = candidate; break; }
    }
    const parent = path.dirname(packageDir);
    if (parent === packageDir) throw new Error('Configured parser is not inside a marked package');
    packageDir = parent;
  }
  if (manifest.version !== MARKED_VERSION) throw new Error(`Writing Voice Lab requires marked ${MARKED_VERSION}; resolved marked ${manifest.version || 'unknown'}`);
  const entry = fs.statSync(resolved).isDirectory() ? path.resolve(packageDir, manifest.module || manifest.main || 'lib/marked.esm.js') : resolved;
  if (!fs.statSync(entry).isFile()) throw new Error('Resolved marked entry is not a file');
  return { entry, packageDir, version: manifest.version };
}

function resolveMarked(env = process.env) {
  if (env.VOICE_LAB_MARKED) {
    try { return { ...inspectPackage(env.VOICE_LAB_MARKED), resolution: 'VOICE_LAB_MARKED' }; }
    catch (error) { throw new Error(`VOICE_LAB_MARKED resolution failed: ${error.message}`); }
  }
  let entry;
  try { entry = require.resolve('marked'); }
  catch (error) { if (error.code !== 'MODULE_NOT_FOUND') throw error; }
  if (entry) return { ...inspectPackage(entry), resolution: 'node_module_resolution' };
  const bundled = path.join(__dirname, '..', 'validation', 'vendor', 'marked');
  if (fs.existsSync(bundled)) return { ...inspectPackage(bundled), resolution: 'package_bundled_parser' };
  throw new Error(`marked ${MARKED_VERSION} is unavailable. Set VOICE_LAB_MARKED to its package folder or entry file, or make that version available through Node module resolution.`);
}

async function loadMarked() {
  const resolved = resolveMarked();
  const imported = await import(pathToFileURL(resolved.entry).href);
  if (typeof imported.marked?.lexer !== 'function') throw new Error('Resolved marked entry does not expose marked.lexer');
  return { marked: imported.marked, version: resolved.version, resolution: resolved.resolution };
}
module.exports = { resolveMarked, loadMarked };
