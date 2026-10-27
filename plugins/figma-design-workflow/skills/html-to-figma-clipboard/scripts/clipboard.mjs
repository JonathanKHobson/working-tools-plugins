import { execFile } from 'node:child_process';
import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);
const JXA = join(dirname(fileURLToPath(import.meta.url)), 'pasteboard.jxa');
const MAX_HTML_BYTES = 64 * 1024 * 1024;
const TIMEOUT_MS = 20_000;

function requireMacOS() {
  if (process.platform !== 'darwin') {
    throw new Error('Native rich clipboard is unavailable on this platform; use local Copy for Figma.');
  }
}

function validateEnvelope(html) {
  if (typeof html !== 'string' || html.length === 0) {
    throw new TypeError('Expected a nonempty HTML clipboard envelope');
  }
  if (!/^\s*<meta\b[^>]*charset\s*=\s*["']?utf-8["']?[^>]*>/i.test(html) ||
      !/<span\b[^>]*\bdata-metadata\s*=/i.test(html) ||
      !/<span\b[^>]*\bdata-buffer\s*=/i.test(html) ||
      !/<\/div\s*>\s*$/i.test(html)) {
    throw new Error('Malformed Figma HTML clipboard envelope');
  }
  if (!/<!--\(figmeta\)[\s\S]*?\(\/figmeta\)-->/i.test(html) ||
      !/<!--\(figma\)[\s\S]*?\(\/figma\)-->/i.test(html)) {
    throw new Error('Clipboard envelope must contain figma and figmeta markers');
  }
  const bytes = Buffer.byteLength(html, 'utf8');
  if (bytes > MAX_HTML_BYTES) {
    throw new RangeError(`HTML clipboard envelope exceeds ${MAX_HTML_BYTES} bytes`);
  }
  return bytes;
}

async function runJxa(args) {
  try {
    const { stdout } = await execFileAsync('/usr/bin/osascript', ['-l', 'JavaScript', JXA, ...args], {
      encoding: 'utf8',
      timeout: TIMEOUT_MS,
      maxBuffer: MAX_HTML_BYTES * 2,
      windowsHide: true,
    });
    return JSON.parse(stdout.trim());
  } catch (error) {
    const detail = error.stderr?.trim() || error.message;
    throw new Error(`Native rich clipboard failed: ${detail}`, { cause: error });
  }
}

export async function writeRichClipboard(html) {
  requireMacOS();
  const htmlBytes = validateEnvelope(html);
  const directory = await mkdtemp(join(tmpdir(), 'figma-rich-clipboard-'));
  const payloadPath = join(directory, 'payload.html');
  try {
    await writeFile(payloadPath, html, { encoding: 'utf8', mode: 0o600, flag: 'wx' });
    const result = await runJxa(['write', payloadPath]);
    if (result.written !== true || result.verified !== true ||
        !Array.isArray(result.types) || !result.types.includes('public.html') ||
        result.htmlBytes !== htmlBytes) {
      throw new Error('Native rich clipboard returned an invalid verification receipt');
    }
    return result;
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
}

export async function inspectRichClipboard() {
  requireMacOS();
  return runJxa(['inspect']);
}
